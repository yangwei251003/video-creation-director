"""Search exact video resource records without loading a giant catalog into context."""
import argparse,hashlib,json,sys,urllib.request
from pathlib import Path

def main():
 p=argparse.ArgumentParser(description=__doc__);p.add_argument('query',nargs='?',default='');p.add_argument('--category');p.add_argument('--id');p.add_argument('--limit',type=int,default=8);p.add_argument('--fetch-to',type=Path)
 a=p.parse_args();root=Path(__file__).resolve().parents[1];d=json.loads((root/'references/catalogs/resource-library.json').read_text(encoding='utf-8'))
 terms=[a.query.lower()];aliases={'阿杜':'adu:','音效':'audio','贴纸':'sticker','字体':'font','花字':'text-style','文字动画':'text-animation','转场':'transition','滤镜':'filter','视频':'video','图片':'image'}
 if a.query in aliases:terms.append(aliases[a.query])
 result=[e for e in d['entries'] if (not a.id or a.id==e['id']) and (not a.category or a.category in e['categories']) and (not a.query or any(t in json.dumps(e,ensure_ascii=False).lower() for t in terms))]
 if a.fetch_to:
  if not a.id or len(result)!=1:p.error('fetch requires one exact --id')
  e=result[0];url=e.get('fetch_url');license=e.get('license','')
  if not url or not url.startswith('https://'):p.error('No verified direct file endpoint: use the record acquisition instructions')
  if license not in ('OFL-1.1','ISC / retained Feather MIT notice','CC0','MIT','Apache-2.0'):p.error('Read and verify this item license before obtaining it; fetch not enabled')
  dest=a.fetch_to.resolve()
  if dest.exists():p.error('Destination exists; keep original and use a fresh destination')
  req=urllib.request.Request(url,headers={'User-Agent':'VideoDirector/2.1'})
  with urllib.request.urlopen(req,timeout=45) as r:
   if not r.url.startswith('https://'):raise ValueError('Insecure redirect rejected')
   raw=r.read(45*1024*1024+1)
  if len(raw)>45*1024*1024:raise ValueError('Asset too large for this bounded fetch')
  sha=hashlib.sha256(raw).hexdigest()
  if e.get('sha256') and e['sha256']!=sha:raise ValueError('Hash differs from reviewed asset')
  dest.parent.mkdir(parents=True,exist_ok=True);dest.write_bytes(raw)
  dest.with_suffix(dest.suffix+'.source.json').write_text(json.dumps({'record':e,'sha256':sha,'bytes':len(raw),'note':'Inspect decoded content and save the license before use'},ensure_ascii=False,indent=2),encoding='utf-8')
  print(json.dumps({'file':str(dest),'sha256':sha,'bytes':len(raw)},ensure_ascii=False));return
 print(json.dumps({'total_matches':len(result),'counting_note':d['counting_note'],'records':result[:max(1,min(a.limit,50))]},ensure_ascii=False,indent=2))
if __name__=='__main__':main()
