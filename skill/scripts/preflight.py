"""Read-only runtime checks. No installs, credentials or global configuration changes."""
import argparse
import json
import shutil
import subprocess
from pathlib import Path


def probe(name, directory=None):
    candidate = str(Path(directory) / (name + ('.exe' if __import__('os').name == 'nt' else ''))) if directory else shutil.which(name)
    if not candidate or not Path(candidate).is_file():
        return {'status': 'MISSING', 'name': name}
    flag = '-version' if name in ('ffmpeg', 'ffprobe') else '--version'
    try:
        run = subprocess.run([candidate, flag], capture_output=True, text=True, encoding='utf-8', errors='replace', timeout=20)
        return {'status': 'PASS' if run.returncode == 0 else 'FAIL', 'name': name, 'version': (run.stdout or run.stderr).splitlines()[0]}
    except (OSError, subprocess.TimeoutExpired) as exc:
        return {'status': 'FAIL', 'name': name, 'reason': type(exc).__name__}


def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('--ffmpeg-dir')
    parser.add_argument('--font', action='append', default=[])
    parser.add_argument('--out', type=Path)
    args = parser.parse_args()
    result = {'runtime': [probe(n, args.ffmpeg_dir if n in ('ffmpeg', 'ffprobe') else None) for n in ('node', 'python', 'ffmpeg', 'ffprobe')], 'fonts': [], 'not_checked': ['MCP host loading/authentication', 'Remotion project dependencies', 'perceptual quality', 'font licence']}
    for path in args.font:
        p = Path(path)
        entry = {'file': p.name, 'exists': p.is_file()}
        if p.is_file():
            try:
                from fontTools.ttLib import TTFont
                with TTFont(p) as font:
                    entry['family'] = font['name'].getDebugName(1)
                    entry['axes'] = [{'tag': a.axisTag, 'min': a.minValue, 'max': a.maxValue} for a in font['fvar'].axes] if 'fvar' in font else []
            except ImportError:
                entry['metadata'] = 'NOT_TESTED: optional fontTools not installed'
        result['fonts'].append(entry)
    text = json.dumps(result, ensure_ascii=False, indent=2)
    if args.out:
        args.out.parent.mkdir(parents=True, exist_ok=True)
        args.out.write_text(text, encoding='utf-8')
    print(text)


if __name__ == '__main__':
    main()
