"""Compare, back up, stage and install the single director skill. Python 3.10+."""
import argparse
import hashlib
import json
import shutil
from datetime import datetime
from pathlib import Path


def digest_tree(root):
    if not root.exists():
        return {}
    return {str(p.relative_to(root)).replace('\\','/'): hashlib.sha256(p.read_bytes()).hexdigest() for p in sorted(root.rglob('*')) if p.is_file() and '__pycache__' not in p.parts and p.suffix != '.pyc'}


def main():
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--codex-dir', type=Path, default=Path.home()/'.codex')
    parser.add_argument('--apply', action='store_true')
    args = parser.parse_args()
    source = Path(__file__).resolve().parent/'skill'
    codex = args.codex_dir.expanduser().resolve()
    skills = codex/'skills'
    target = skills/'video-creation-director'
    if source.is_symlink() or target.is_symlink() or any(p.is_symlink() for p in source.rglob('*')):
        raise ValueError('Refusing linked skill roots or source entries')
    before, after = digest_tree(target), digest_tree(source)
    # Machine-specific paths belong to the user and survive future upgrades.
    preserved = [name for name in ('local-environment.json',) if name in before]
    for name in preserved:
        if (target/name).is_symlink():
            raise ValueError('Refusing linked personal configuration')
        after[name] = before[name]
    changed = sorted(k for k in set(before)|set(after) if before.get(k)!=after.get(k))
    result = {'target':str(target),'changed_files':changed,'preserved_local_files':preserved,'applied':False}
    if not args.apply or not changed:
        print(json.dumps(result,ensure_ascii=False,indent=2)); return
    stamp=datetime.now().strftime('%Y%m%d-%H%M%S-%f')
    backup=codex/'backups'/('video-director-upgrade-'+stamp)
    stage=skills/('video-creation-director-stage-'+stamp)
    skills.mkdir(parents=True,exist_ok=True)
    backup.mkdir(parents=True,exist_ok=False)
    # Resolve exact paths and retain all prior files in a recoverable backup.
    if target.resolve().parent != skills.resolve() or stage.resolve().parent != skills.resolve() or backup.resolve().parent != (codex/'backups').resolve():
        raise ValueError('Unexpected resolved destination')
    shutil.copytree(source,stage,ignore=shutil.ignore_patterns('__pycache__','*.pyc'))
    for name in preserved:
        shutil.copy2(target/name,stage/name)
    if digest_tree(stage)!=after:
        raise ValueError('Staging verification failed; target untouched')
    if digest_tree(target)!=before:
        raise ValueError('Existing skill changed during install; target untouched')
    if target.exists():
        target.rename(backup/'video-creation-director')
    try:
        stage.rename(target)
    except OSError:
        if (backup/'video-creation-director').exists() and not target.exists():
            (backup/'video-creation-director').rename(target)
        raise
    result.update({'applied':True,'backup':str(backup),'verified':digest_tree(target)==after})
    (backup/'installation.json').write_text(json.dumps(result,ensure_ascii=False,indent=2),encoding='utf-8')
    print(json.dumps(result,ensure_ascii=False,indent=2))


if __name__=='__main__':
    main()
