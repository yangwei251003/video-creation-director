#!/usr/bin/env python3
"""Read/edit a running local OpenFilm project without foreground input.

Uses the v0.2.6 Studio API and its own local credential; never prints it.
Apply requires an explicit revision and operation file. No implicit retry on writes.
"""
import argparse
import json
import shutil
import sys
from pathlib import Path
from urllib.error import HTTPError
from urllib.parse import urlsplit, quote
from urllib.request import Request, urlopen

def request(base, credential, path, body=None):
    parsed=urlsplit(base)
    if parsed.scheme!='http' or parsed.hostname not in ('127.0.0.1','localhost','::1') or parsed.username or parsed.password or parsed.query:
        raise ValueError('Only a local HTTP Studio address is accepted')
    headers={'x-studio-key':credential,'Content-Type':'application/json'}
    data=None if body is None else json.dumps(body).encode('utf-8')
    req=Request(base.rstrip('/')+'/api/'+path,headers=headers,data=data,method='GET' if body is None else 'POST')
    with urlopen(req,timeout=120) as r:return json.load(r)

def main():
    p=argparse.ArgumentParser(description=__doc__)
    p.add_argument('action',choices=['inspect','history','save','apply','restore'])
    p.add_argument('--project',required=True,help='Studio project ID, not a path')
    p.add_argument('--studio',default='http://127.0.0.1:4747')
    p.add_argument('--key-file',type=Path,default=Path.home()/'.openfilm/key')
    p.add_argument('--output',type=Path)
    p.add_argument('--revision');p.add_argument('--ops',type=Path)
    p.add_argument('--message',default='Director checkpoint');p.add_argument('--commit')
    a=p.parse_args()
    credential=a.key_file.read_text(encoding='utf-8').strip()
    root='projects/'+quote(a.project,safe='')
    def api(suffix='',body=None):return request(a.studio,credential,root+suffix,body)
    if a.action=='inspect':
        r=api();out={k:r.get(k) for k in ('project','rev','value','doc','problems')}
    elif a.action=='history':out=api('/history')
    elif a.action=='save':out=api('/history/save',{'message':a.message})
    elif a.action=='apply':
        if not a.revision or not a.ops:p.error('apply requires --revision and --ops')
        ops=json.loads(a.ops.read_text(encoding='utf-8-sig'))
        if not isinstance(ops,list):p.error('operations must be a JSON list')
        before=api()
        if before.get('rev')!=a.revision:raise ValueError('Revision changed: read the latest project before editing')
        root_path=Path(before['project']['path']).resolve()
        backup=root_path/'.film'/'director-backups';backup.mkdir(parents=True,exist_ok=True)
        from datetime import datetime
        shutil.copy2(root_path/'film.html',backup/(datetime.now().strftime('%Y%m%d-%H%M%S-%f')+'-film.html'))
        r=api('/edit',{'base':a.revision,'ops':ops});out={k:r.get(k) for k in ('rev','value','doc','problems')}
    else:
        if not a.commit:p.error('restore requires --commit; save current work first')
        # Native server refuses dirty restoration; never silently discard user edits.
        r=api('/history/checkout',{'commit':a.commit,'discard':False})
        out={k:r.get(k) for k in ('rev','value','doc','missing')}
    rendered=json.dumps(out,ensure_ascii=False,indent=2)
    if a.output:
        a.output.parent.mkdir(parents=True,exist_ok=True);a.output.write_text(rendered+'\n',encoding='utf-8')
        print(json.dumps({'saved':str(a.output),'action':a.action},ensure_ascii=False))
    else:print(rendered)

if __name__=='__main__':
    try:main()
    except HTTPError as e:
        print(json.dumps({'error':'Studio request failed','status':e.code}),file=sys.stderr);sys.exit(1)
    except Exception as e:
        print(str(e),file=sys.stderr);sys.exit(1)
