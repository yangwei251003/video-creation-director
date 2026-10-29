"""Independent, keyless Freesound public-page adapter. No proxy changes or browser credentials."""
import argparse
import hashlib
import html
import json
import re
import urllib.parse
import urllib.request
import urllib.error
import time
from datetime import datetime, timezone
from pathlib import Path


def get(url, binary=False):
    req = urllib.request.Request(url, headers={'User-Agent': 'VideoCreationDirector/2.1 (public asset research)'})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=40) as r:
                data = r.read(30*1024*1024+1)
                if len(data) > 30*1024*1024:
                    raise ValueError('Asset exceeds 30 MB per-request bound')
            break
        except (urllib.error.URLError, TimeoutError):
            if attempt == 2: raise
            time.sleep(1+attempt)
    return data if binary else data.decode('utf-8')


def metadata(url):
    p = urllib.parse.urlparse(url)
    if p.scheme != 'https' or p.hostname != 'freesound.org' or not re.fullmatch(r'/people/[^/]+/sounds/\d+/', p.path):
        raise ValueError('Expected canonical https Freesound sound page')
    page = get(url)
    lm = re.search(r'href="(https?://creativecommons.org/(?:publicdomain/zero|licenses/by)/[^" ]+)"', page)
    if not lm:
        raise ValueError('Only explicitly identified CC0 or CC BY licenses supported')
    license_url = html.unescape(lm[1]).replace('http:', 'https:')
    preview = re.search(r'data-static-file-url="(https://cdn.freesound.org/previews/[^" ]+-hq.mp3)"', page)
    if not preview:
        raise ValueError('Public HQ preview not found; page format may have changed')
    title = re.search(r'<meta property="og:title" content="([^"]+)"', page)
    duration = re.search(r'data-duration="([\d.]+)"', page)
    return {'source_page':url, 'title':html.unescape(title[1]) if title else p.path, 'author':urllib.parse.unquote(p.path.split('/')[2]), 'license':'CC0-1.0' if '/zero/' in license_url else 'CC-BY', 'license_url':license_url, 'download_url':html.unescape(preview[1]), 'source_quality':'HQ MP3 public preview, not original WAV', 'duration_seconds':float(duration[1]) if duration else None, 'accessed_at':datetime.now(timezone.utc).isoformat()}


def main():
    p = argparse.ArgumentParser(description=__doc__)
    sub = p.add_subparsers(dest='command', required=True)
    s = sub.add_parser('search'); s.add_argument('query'); s.add_argument('--out', type=Path, required=True)
    f = sub.add_parser('fetch'); f.add_argument('url'); f.add_argument('--out', type=Path, required=True); f.add_argument('--allow-by', action='store_true')
    args = p.parse_args()
    if args.command == 'search':
        url = 'https://freesound.org/search/?'+urllib.parse.urlencode({'q':args.query,'f':'license:"Creative Commons 0"'})
        page = get(url)
        paths = list(dict.fromkeys(re.findall(r'href="(/people/[^"/]+/sounds/\d+/)"', page)))
        result = {'query':args.query, 'source_page':url, 'license_filter':'CC0 (each download rechecked)', 'results':[{'source_page':'https://freesound.org'+x} for x in paths[:20]]}
        if not paths:
            raise ValueError('No results or page format changed; do not invent matches')
        args.out.write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
        print(json.dumps(result, ensure_ascii=False)); return
    result = metadata(args.url)
    if result['license'] != 'CC0-1.0' and not args.allow_by:
        raise ValueError('CC BY requires explicit --allow-by and attribution in the project')
    payload = get(result.pop('download_url'), binary=True)
    if not (payload.startswith(b'ID3') or payload[:1] == b'\xff'):
        raise ValueError('Preview response is not recognizable MP3')
    args.out.mkdir(parents=True, exist_ok=True)
    asset_id = urllib.parse.urlparse(args.url).path.split('/')[-2]
    target = args.out/('freesound-'+asset_id+'.mp3')
    if target.exists() and target.read_bytes() != payload:
        raise ValueError('Existing asset differs; use a separate output folder')
    target.write_bytes(payload)
    result.update({'file':target.name,'sha256':hashlib.sha256(payload).hexdigest(), 'attribution':f"{result['title']} — {result['author']} — {result['source_page']} — {result['license_url']}; modifications: record in project", 'listened':False})
    target.with_suffix('.source.json').write_text(json.dumps(result, ensure_ascii=False, indent=2), encoding='utf-8')
    print(json.dumps(result, ensure_ascii=False))


if __name__ == '__main__':
    main()
