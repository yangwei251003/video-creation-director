"""Non-destructive technical inspection and frame sampling; no aesthetic scoring."""
import argparse
import hashlib
import json
import shutil
import subprocess
from fractions import Fraction
from pathlib import Path


def command(binary, args, timeout=300):
    return subprocess.run([binary, *map(str, args)], capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=timeout)


def main():
    p = argparse.ArgumentParser()
    p.add_argument('video', type=Path)
    p.add_argument('--out', required=True, type=Path)
    p.add_argument('--ffmpeg-dir', type=Path)
    p.add_argument('--width', type=int)
    p.add_argument('--height', type=int)
    p.add_argument('--fps', type=float)
    p.add_argument('--audio', choices=['required', 'silent', 'unspecified'], default='unspecified')
    p.add_argument('--transition', type=float, action='append', default=[])
    args = p.parse_args()
    video = args.video.resolve(strict=True)
    out = args.out.resolve()
    if out == video or out in video.parents:
        raise ValueError('Use a dedicated output directory, not an ancestor of the input video')
    out.mkdir(parents=True, exist_ok=True)
    def locate(name):
        suffix = '.exe' if __import__('os').name == 'nt' else ''
        found = str(args.ffmpeg_dir / (name + suffix)) if args.ffmpeg_dir else shutil.which(name)
        if not found or not Path(found).is_file():
            raise FileNotFoundError(name + ' unavailable; pass --ffmpeg-dir')
        return found
    ffmpeg, ffprobe = locate('ffmpeg'), locate('ffprobe')
    probe = command(ffprobe, ['-v','error','-show_format','-show_streams','-of','json',video])
    if probe.returncode:
        raise RuntimeError('ffprobe failed: ' + probe.stderr[-2000:])
    metadata = json.loads(probe.stdout)
    streams = metadata['streams']
    vs = next((s for s in streams if s['codec_type'] == 'video'), None)
    if not vs:
        raise ValueError('No video stream')
    duration = float(vs.get('duration') or metadata['format']['duration'])
    fps = float(Fraction(vs.get('avg_frame_rate') or vs['r_frame_rate']))
    failures = []
    for key in ('width','height'):
        if getattr(args, key) is not None and vs[key] != getattr(args, key):
            failures.append(key + ' mismatch')
    if args.fps and abs(args.fps - fps) > 0.01:
        failures.append('fps mismatch')
    audio = [s for s in streams if s['codec_type'] == 'audio']
    if args.audio == 'required' and not audio:
        failures.append('required audio missing')
    if args.audio == 'silent' and audio:
        failures.append('audio present in silent specification')
    decode = command(ffmpeg, ['-v','error','-xerror','-i',video,'-f','null','-'], timeout=600)
    if decode.returncode or decode.stderr.strip():
        failures.append('decode error')
    times = {0.0, duration * .25, duration * .5, duration * .75, max(0, duration-1/fps)}
    for t in args.transition:
        times.update((max(0,t-.15),t,min(duration-1/fps,t+.15)))
    samples = []
    for i,t in enumerate(sorted(times)):
        if not 0 <= t < duration:
            continue
        path = out / f'frame-{i:03d}.jpg'
        res = command(ffmpeg, ['-v','error','-y','-ss',f'{t:.6f}','-i',video,'-frames:v','1','-vf','scale=480:-2','-q:v','2',path])
        samples.append({'time':round(t,4),'file':path.name,'success':res.returncode==0 and path.is_file()})
    if not all(s['success'] for s in samples):
        failures.append('sample extraction failed')
    if samples and all(s['success'] for s in samples):
        command(ffmpeg, ['-v','error','-y','-framerate','1','-i',out/'frame-%03d.jpg','-vf',f'tile=3x{(len(samples)+2)//3}','-frames:v','1',out/'contact-sheet.jpg'])
    report = {'input_name':video.name,'sha256':hashlib.file_digest(video.open('rb'),'sha256').hexdigest(),'duration_seconds':duration,'width':vs['width'],'height':vs['height'],'fps':fps,'video_codec':vs['codec_name'],'audio':[{'codec':s.get('codec_name'),'sample_rate':s.get('sample_rate'),'channels':s.get('channels')} for s in audio],'decode_passed':decode.returncode==0 and not decode.stderr.strip(),'failures':failures,'samples':samples,'status':'TECHNICAL_PASS' if not failures else 'TECHNICAL_FAIL','not_verified':['continuous motion','audio listening','semantic accuracy','font glyph coverage','licences','aesthetic/reference parity']}
    (out/'media-report.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(report,ensure_ascii=False,indent=2))
    return 0 if not failures else 1


if __name__ == '__main__':
    raise SystemExit(main())
