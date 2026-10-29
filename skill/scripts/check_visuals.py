"""Trace repeated shots and flag multi-frame similarity. Never certifies full viewing."""
import argparse
import hashlib
import itertools
import json
import math
import subprocess
from html.parser import HTMLParser
from urllib.parse import urlsplit, unquote
from pathlib import Path


def sha(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()


def span(v):
    return isinstance(v, list) and len(v) == 2 and all(isinstance(x, (int, float)) and not isinstance(x, bool) and math.isfinite(x) for x in v) and 0 <= v[0] < v[1]


def fingerprints(path, times, ffmpeg):
    """Sample 3 moments, whole/central 75% crops, with mirrored variants. Candidate detection only."""
    result = []
    for t in times:
        variants = []
        for crop in ('', 'crop=iw*0.75:ih*0.75,'):
            p = subprocess.run([ffmpeg, '-v', 'error', '-ss', str(t), '-i', str(path), '-frames:v', '1', '-vf', crop+'scale=17:16,format=gray', '-f', 'rawvideo', '-'], capture_output=True, check=True)
            if len(p.stdout) != 272:
                raise ValueError('Could not sample frame: '+str(path))
            for mirror in (False, True):
                bits = 0
                for row in range(16):
                    line = p.stdout[row*17:(row+1)*17]
                    if mirror:
                        line = line[::-1]
                    for a, b in zip(line, line[1:]):
                        bits = (bits << 1) | int(a > b)
                variants.append(bits)
        result.append(variants)
    return result


class MediaParser(HTMLParser):
    def __init__(self):
        super().__init__(); self.media=[]; self.pages=[]
    def handle_starttag(self, tag, attrs):
        d=dict(attrs)
        if tag in ('video','img'): self.media.append((tag,d))
        if tag=='iframe': self.pages.append(d)


def audit_timeline(m, base, timeline):
    errors, gaps = [], []
    parser=MediaParser(); parser.feed(timeline.read_text(encoding='utf-8-sig'))
    assets={x['id']:x for x in m.get('assets',[])}
    segments={x['id']:x for x in m.get('segments',[])}
    by_clip={u.get('timeline_clip_id'):u for u in m.get('uses',[])}
    found=set()
    for tag,d in parser.media:
        ident=d.get('id')
        u=by_clip.get(ident)
        if not ident or not u:
            gaps.append('unmapped timeline media: '+str(ident or d.get('src')));continue
        found.add(u['id']);s=segments.get(u.get('segment_id'),{});a=assets.get(s.get('asset_id'),{})
        src=urlsplit(d.get('src',''))
        if src.scheme or src.netloc:
            errors.append('uncached remote timeline media: '+ident);continue
        path=(timeline.parent/unquote(src.path)).resolve()
        if path!=(base/a.get('local_original','__missing__')).resolve():
            errors.append('timeline source differs from manifest: '+ident)
        try:
            if not src.fragment.startswith('t='): raise ValueError('Explicit source range required')
            bounds=list(map(float,src.fragment[2:].split(',')))
            if not span(bounds): raise ValueError('Explicit source in/out required')
            expected=s.get('local_range',s.get('source_range'))
            speed=float(d.get('speed',1));at=float(d.get('at',0))
            if not expected or any(abs(x-y)>.002 for x,y in zip(bounds,expected)):
                errors.append('timeline source range differs: '+ident)
            actual=[at,at+(bounds[1]-bounds[0])/speed]
            if not span(u.get('output')) or any(abs(x-y)>.002 for x,y in zip(actual,u['output'])) or abs(speed-u.get('speed',1))>.000001:
                errors.append('timeline placement/speed differs: '+ident)
        except (ValueError,TypeError,ZeroDivisionError):
            errors.append('invalid or unbounded timeline range: '+ident)
    for u in m.get('uses',[]):
        s=segments.get(u.get('segment_id'),{});a=assets.get(s.get('asset_id'),{})
        if a.get('kind') in ('video','image') and u['id'] not in found:
            gaps.append('manifest use not located in timeline: '+u['id'])
    page_files=[]
    for d in parser.pages:
        p=(timeline.parent/unquote(urlsplit(d.get('src','')).path)).resolve()
        if not p.is_file():gaps.append('missing page: '+str(p));continue
        page_files.append(p)
        nested=MediaParser();nested.feed(p.read_text(encoding='utf-8-sig'))
        if nested.media or nested.pages:
            gaps.append('nested media requires explicit expansion into timeline: '+p.name)
    return errors,gaps,page_files


def evaluate(m, base, ffmpeg=None, timeline=None):
    errors, gaps, failures, suspects = [], [], [], []
    assets = {x['id']: x for x in m.get('assets', [])}
    segments = {x['id']: x for x in m.get('segments', [])}
    uses = m.get('uses', [])
    if m.get('schema_version') != 2:
        errors.append('schema_version must be 2')
    if timeline:
        te,tg,_=audit_timeline(m,base,timeline);errors.extend(te);gaps.extend(tg)
    else:
        gaps.append('actual timeline not audited')
    if len(assets) != len(m.get('assets', [])) or len(segments) != len(m.get('segments', [])) or len({u['id'] for u in uses}) != len(uses):
        errors.append('duplicate identifiers')
    rows, prints = [], {}
    for u in uses:
        s = segments.get(u.get('segment_id'), {})
        a = assets.get(s.get('asset_id'), {})
        if not s or not a or not span(u.get('output')) or not span(s.get('source_range')):
            errors.append('invalid mapping: '+u['id']); continue
        if a.get('kind') not in ('video', 'image') or (a.get('kind')=='image' and u.get('role') in ('brand_mark', 'decorative_pattern')):
            continue
        if not s.get('source_asset_id') or not s.get('source_shot_id'):
            gaps.append('source identity missing: '+u['id'])
        derived = s.get('derived_from')
        seen = {s['id']}
        while derived:
            if derived in seen or derived not in segments:
                errors.append('invalid derivation: '+u['id']); break
            parent = segments[derived]; seen.add(derived)
            if parent.get('source_asset_id') != s.get('source_asset_id') or parent.get('source_shot_id') != s.get('source_shot_id'):
                errors.append('derivation changed source identity: '+u['id'])
            derived = parent.get('derived_from')
        speed = u.get('speed', 1)
        if not isinstance(speed, (int, float)) or isinstance(speed, bool) or not math.isfinite(speed) or speed <= 0:
            errors.append('invalid speed: '+u['id']); continue
        if a.get('kind') == 'video' and (u.get('loop') is True or (u['output'][1]-u['output'][0])*speed > s['source_range'][1]-s['source_range'][0]+0.05):
            failures.append('loop/insufficient source duration: '+u['id'])
        p = base/a.get('local_original', '__missing__')
        if not p.is_file():
            gaps.append('missing local source: '+u['id'])
        elif not a.get('sha256') or sha(p) != a['sha256']:
            errors.append('source hash mismatch: '+u['id'])
        rows.append((u, s, a))
        if ffmpeg and p.is_file():
            try:
                lo, hi = s['source_range']
                # Fingerprint the actual local file. Derived files require local time mapping.
                lo, hi = s.get('local_range', [lo, hi])
                prints[u['id']] = fingerprints(p, [lo+(hi-lo)*f for f in (0.15, 0.5, 0.85)], ffmpeg)
            except (ValueError, OSError, subprocess.CalledProcessError) as exc:
                gaps.append('fingerprint failed: '+u['id']+' '+str(exc)[:140])
    for (u, s, a), (v, t, b) in itertools.combinations(rows, 2):
        same_asset = s.get('source_asset_id') == t.get('source_asset_id') or (a.get('sha256') and a.get('sha256') == b.get('sha256'))
        same_shot = same_asset and s.get('source_shot_id') == t.get('source_shot_id')
        overlap = same_asset and max(s['source_range'][0], t['source_range'][0]) < min(s['source_range'][1], t['source_range'][1])-1e-6
        pair = '|'.join(sorted([u['id'], v['id']]))
        if same_shot or overlap:
            if a['kind'] == 'video' and b['kind'] == 'video':
                failures.append('repeated shot/source span: '+pair)
            else:
                suspects.append({'pair': pair, 'reason': 'repeated narrative image'})
        elif u['id'] in prints and v['id'] in prints:
            distances = [min((x^y).bit_count() for x in pa for y in pb) for pa, pb in zip(prints[u['id']], prints[v['id']])]
            if max(distances) <= 20:
                suspects.append({'pair': pair, 'reason': 'multi-frame similarity', 'distances': distances})
    resolutions = m.get('similarity_resolutions', {})
    for suspect in suspects:
        r = resolutions.get(suspect['pair'], {})
        if r.get('result') == 'duplicate':
            failures.append('observed duplicate: '+suspect['pair'])
        elif r.get('result') != 'distinct' or not r.get('reason') or not r.get('evidence') or not (base/r['evidence']).is_file():
            gaps.append('unresolved similarity: '+suspect['pair'])
    if rows and not ffmpeg:
        gaps.append('multi-frame sampling not run')
    for slot in m.get('slots', []):
        ids = slot.get('candidate_segment_ids', [])
        backups = slot.get('backup_segment_ids', [])
        def identity(i):
            s = segments.get(i, {})
            return (s.get('source_asset_id'), s.get('source_shot_id'))
        need = 2 if slot.get('important') else 1
        if any(i not in segments for i in ids+backups+[slot.get('primary_segment_id')]):
            errors.append('unknown pool segment: '+slot.get('id','?')); continue
        unique = set(map(identity, ids))
        primary = identity(slot['primary_segment_id'])
        backups_unique = set(map(identity, backups))-{primary}
        if len(unique) < 3 or len(backups_unique) < need:
            gaps.append('insufficient candidates/backups: '+slot['id']+' '+slot.get('shortage_reason',''))
        for i in backups:
            a = assets.get(segments[i]['asset_id'], {})
            p=base/a.get('local_original','__missing__')
            if identity(i) in {(s.get('source_asset_id'),s.get('source_shot_id')) for _,s,_ in rows}:
                gaps.append('backup already used in film: '+i)
            if not p.is_file() or not a.get('rights',{}).get('may_include_in_video'):
                gaps.append('backup unavailable or rights unverified: '+i)
            elif not a.get('sha256') or sha(p)!=a['sha256']:
                errors.append('backup hash mismatch: '+i)
    primaries={x.get('primary_segment_id') for x in m.get('slots',[])}
    for u,s,a in rows:
        if s['id'] not in primaries:
            gaps.append('material slot missing: '+u['id'])
    coverage = m.get('coverage', {})
    for key in ('final_timeline_checked', 'nested_media_checked', 'visual_comparison_complete'):
        if coverage.get(key) is not True:
            gaps.append('coverage:'+key)
    if not coverage.get('evidence') or not (base/coverage['evidence']).is_file():
        gaps.append('coverage evidence missing')
    return {'status': 'INVALID' if errors else 'FAIL' if failures else 'UNVERIFIED' if gaps else 'PASS_RECORD_ONLY', 'errors':errors, 'failures':failures, 'unverified':gaps, 'suspects':suspects, 'fingerprinted_uses':len(prints), 'notice':'Source mapping and sampled similarity only. Full-film review is separate.'}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    p.add_argument('manifest', type=Path); p.add_argument('--timeline', type=Path, required=True)
    p.add_argument('--ffmpeg'); p.add_argument('--out', type=Path, required=True)
    args = p.parse_args()
    try:
        m = json.loads(args.manifest.read_text(encoding='utf-8-sig'))
        base=args.manifest.resolve().parent
        result = evaluate(m, base, args.ffmpeg,args.timeline.resolve())
        files={args.manifest.resolve(),args.timeline.resolve()}
        files.update((base/a['local_original']).resolve() for a in m.get('assets',[]) if a.get('local_original') and (base/a['local_original']).is_file())
        _,_,pages=audit_timeline(m,base,args.timeline.resolve());files.update(pages)
        for directory in {p.parent for p in pages}:
            files.update(p.resolve() for p in directory.rglob('*') if p.is_file())
        result['inputs'] = [{'file':str(f), 'sha256':sha(f)} for f in sorted(files)]
        result['timeline_audited']=True
    except (ValueError, KeyError, TypeError, OSError) as exc:
        result = {'status':'INVALID', 'errors':[str(exc)]}
    args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False, indent=2))
    return 0 if result['status'] == 'PASS_RECORD_ONLY' else 2


if __name__ == '__main__':
    raise SystemExit(main())
