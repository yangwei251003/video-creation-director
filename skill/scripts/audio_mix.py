"""Render explicit sound cues to separate PCM stems and a mix. Does not certify listening."""
import argparse
import hashlib
import json
import math
import subprocess
from pathlib import Path


def num(v, low, high, name):
    if not isinstance(v, (int, float)) or isinstance(v, bool) or not math.isfinite(v) or not low <= v <= high:
        raise ValueError('invalid '+name)
    return v


def placement(cue, duration):
    src = cue['source_range']
    start, end = num(src[0],0,86400,'source start'), num(src[1],0,86400,'source end')
    if end <= start:
        raise ValueError('nonpositive cue duration')
    transient = num(cue.get('transient_offset', start), start, end, 'transient')
    anchor = num(cue['anchor_seconds'],0,duration,'anchor')
    at = anchor-(transient-start)
    if at < 0 or at+end-start > duration+0.001:
        raise ValueError('cue starts before film or tail exceeds film; trim/fade intentionally')
    return start, end, at


def render(spec, base, out, ffmpeg):
    duration = num(spec['duration_seconds'],0.001,86400,'duration')
    cues = spec['cues']
    if not cues:
        raise ValueError('No audio cues; explicitly silent projects do not need mixing')
    if len({c['id'] for c in cues}) != len(cues):
        raise ValueError('Duplicate cue IDs')
    out.mkdir(parents=True, exist_ok=True)
    stems, schedule = [], []
    tracks = ('voice','music','ambience','sfx')
    if any(c.get('track') not in tracks for c in cues):
        raise ValueError('Unknown audio track')
    for track in tracks:
        selected = [c for c in cues if c['track'] == track]
        if not selected:
            continue
        inputs, chains, labels = [], [], []
        for i, c in enumerate(selected):
            src = base/c['file']
            if not src.is_file(): raise ValueError('Missing audio: '+str(src))
            lo, hi, at = placement(c, duration)
            probe = str(Path(ffmpeg).with_name('ffprobe'+Path(ffmpeg).suffix)) if Path(ffmpeg).name != 'ffmpeg' else 'ffprobe'
            info = json.loads(subprocess.check_output([probe,'-v','error','-show_format','-show_streams','-of','json',str(src)]))
            if not any(s.get('codec_type') == 'audio' for s in info.get('streams', [])):
                raise ValueError('Source has no audio stream: '+str(src))
            actual_duration = float(info['format']['duration'])
            if hi > actual_duration+0.001:
                raise ValueError('Cue range exceeds actual audio duration: '+c['id'])
            gain = num(c.get('gain',1),0,8,'gain')
            fi = num(c.get('fade_in',0),0,hi-lo,'fade_in')
            fo = num(c.get('fade_out',0),0,hi-lo-fi,'fade_out')
            pan = num(c.get('pan',0),-1,1,'pan')
            expression = str(gain)
            for envelope in c.get('gain_envelopes',[]):
                a = num(envelope['from'],0,hi-lo,'envelope start')
                b = num(envelope['to'],a,hi-lo,'envelope end')
                level = num(envelope['gain'],0,1,'envelope gain')
                expression += f'*if(between(t,{a},{b}),{level},1)'
            inputs += ['-i',str(src)]
            chain = f'[{i}:a]atrim=start={lo}:end={hi},asetpts=PTS-STARTPTS,aresample=48000,aformat=channel_layouts=stereo,volume=\'{expression}\':eval=frame'
            chain += f',afade=t=in:d={fi},afade=t=out:st={hi-lo-fo}:d={fo}' if fi or fo else ''
            # Cross-feed moves a left-only signal right instead of silencing it.
            chain += f',pan=stereo|c0={1-max(0,pan)}*c0+{max(0,-pan)}*c1|c1={max(0,pan)}*c0+{1-max(0,-pan)}*c1'
            label = f'c{i}'; labels.append('['+label+']')
            chains.append(chain+f',adelay={round(at*48000)}S:all=1[{label}]')
            schedule.append({'id':c['id'],'shot_id':c.get('shot_id'),'start_seconds':at,'scheduled_transient_seconds':at+c.get('transient_offset',lo)-lo,'anchor_seconds':c['anchor_seconds'],'measured_sync_error_seconds':None,'input_sha256':hashlib.sha256(src.read_bytes()).hexdigest()})
        chains.append(''.join(labels)+f'amix=inputs={len(labels)}:normalize=0,apad,atrim=duration={duration}[out]')
        target = out/(track+'.wav')
        subprocess.run([ffmpeg,'-v','error','-y',*inputs,'-filter_complex',';'.join(chains),'-map','[out]','-c:a','pcm_f32le',str(target)],check=True)
        stems.append(target)
    inputs = [arg for s in stems for arg in ('-i',str(s))]
    chain = ''.join(f'[{i}:a]' for i in range(len(stems)))+f'amix=inputs={len(stems)}:normalize=0,alimiter=limit=0.95:level=false:latency=true[out]'
    mixed = out/'mix.wav'
    subprocess.run([ffmpeg,'-v','error','-y',*inputs,'-filter_complex',chain,'-map','[out]','-c:a','pcm_s24le',str(mixed)],check=True)
    analysis = subprocess.run([ffmpeg,'-hide_banner','-i',str(mixed),'-af','ebur128=peak=true','-f','null','-'],capture_output=True,text=True,check=True).stderr
    (out/'loudness.txt').write_text(analysis,encoding='utf-8')
    result = {'status':'RENDERED_NOT_LISTENED','schedule':schedule,'stems':[s.name for s in stems],'mix':mixed.name,'listened_full':False,'notice':'Sync is scheduled, not measured from perceptual listening. Verify actual transients and export.'}
    (out/'audio-report.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    return result


def main():
    p = argparse.ArgumentParser(description=__doc__); p.add_argument('cues',type=Path); p.add_argument('--ffmpeg',default='ffmpeg'); p.add_argument('--out',type=Path,required=True)
    a = p.parse_args(); print(json.dumps(render(json.loads(a.cues.read_text(encoding='utf-8-sig')),a.cues.resolve().parent,a.out,a.ffmpeg),ensure_ascii=False,indent=2))


if __name__ == '__main__': main()
