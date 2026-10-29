"""Install curated resources into OpenFilm Saved without foreground control.
Compares existing files and backs up different ones; does not delete user files.
"""
import argparse,hashlib,json,shutil
from datetime import datetime
from pathlib import Path
def digest(p):return hashlib.sha256(p.read_bytes()).hexdigest()
def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('--resources',type=Path,required=True);p.add_argument('--saved',type=Path,required=True);p.add_argument('--apply',action='store_true');a=p.parse_args()
 source=a.resources.resolve();saved=a.saved.resolve();target=saved/'Director 2.1';backup=saved/('.director-backup-'+datetime.now().strftime('%Y%m%d-%H%M%S'))
 if target.resolve().parent!=saved:raise ValueError('Unexpected target')
 changed=[];same=0
 for folder in ('Starter','Audio','Stickers','Fonts','Video','Images'):
  base=source/folder
  if not base.is_dir():continue
  for f in base.rglob('*'):
   if not f.is_file():continue
   if f.is_symlink():raise ValueError('Refusing linked asset')
   rel=f.relative_to(source);dest=target/rel
   if not f.resolve().is_relative_to(source) or not dest.resolve().is_relative_to(target.resolve()):raise ValueError('Asset path leaves selected roots')
   if dest.exists() and digest(dest)==digest(f):same+=1;continue
   changed.append(str(rel))
   if a.apply:
    if dest.exists():b=backup/rel;b.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(dest,b)
    dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(f,dest)
 print(json.dumps({'applied':a.apply,'target':str(target),'changed_files':len(changed),'unchanged_files':same,'backup':str(backup) if backup.exists() else None},ensure_ascii=False))
if __name__=='__main__':main()
