"""Search the research index without loading every card into the agent context."""
import argparse
import json
from pathlib import Path


def main():
    p=argparse.ArgumentParser()
    p.add_argument('query',nargs='?',default='')
    p.add_argument('--library',choices=['adu','vincent','all'],default='all')
    p.add_argument('--kind',default='')
    p.add_argument('--licence',default='')
    p.add_argument('--limit',type=int,default=5)
    a=p.parse_args()
    root=Path(__file__).resolve().parents[1]/'references'/'catalogs'
    records=[]
    for library,filename,key in [('adu','adu-templates.json','templates'),('vincent','vincent-shots.json','records')]:
        if a.library not in ('all',library): continue
        data=json.loads((root/filename).read_text(encoding='utf-8'))
        records.extend({'library':library,**r} for r in data[key])
    terms=a.query.casefold().split()
    hits=[]
    for r in records:
        hay=json.dumps(r,ensure_ascii=False).casefold()
        if terms and not all(t in hay for t in terms): continue
        if a.kind and r.get('kind','template')!=a.kind: continue
        if a.licence and a.licence.casefold() not in json.dumps(r.get('license',''),ensure_ascii=False).casefold(): continue
        hits.append(r)
    print(json.dumps({'matches':len(hits),'returned':hits[:max(1,min(a.limit,20))],'notice':'Research snapshot; verify source, version, access and licence before use. Kinds overlap; do not sum into a template count.'},ensure_ascii=False,indent=2))


if __name__=='__main__': main()
