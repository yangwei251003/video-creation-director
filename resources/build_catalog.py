"""Merge reviewed references and exact upstream paths into a human/agent catalog."""
import json,collections,shutil
from pathlib import Path
repo=Path(__file__).resolve().parents[1]
def read(path):return json.loads((repo/path).read_text(encoding='utf-8'))
def build():
 entries=[]
 for x in read('resources/source-libraries.json')['libraries']:
  entries.append({'id':'library:'+x['id'],'title':x['title'],'categories':x['categories'],'kind':'source-library','source_url':x['url'],'api_template':x.get('api'),'license':x['license'],'license_url':x['license_url'],'availability':x['access'],'method':x['use'],'verified':'source or official policy reviewed; individual files checked when acquired'})
 for x in read('research/vincent/template-inventory.json')['records']:
  text=(x['category']+' '+x['title']).lower();cats=['template']
  for terms,cat in [('typography 字幕花字 文字 字卡','text-style'),('typography flyin reveal typewriter kinetic 文字','text-animation'),('transition 转场','transition'),('effects 光效 背景 backdrop','effect'),('data 关系 visual-relationship 图标 数据信息','component')]:
   if any(s in text for s in terms.split()):cats.append(cat)
  entries.append({'id':'vincent:'+x['id'],'title':x['title'],'categories':cats,'kind':x['kind'],'source_url':x['source_url'],'implementation_urls':x.get('implementation_urls',[]),'demo_url':x.get('demo_url'),'license':x['license'],'license_urls':x.get('license_urls',[]),'availability':'reference-or-adaptation','method':x.get('use_case_excerpt','')+'；读取镜头卡及指定实现，核对依赖/素材许可，转为frame(t)或内部渲染后接入。','tags':x.get('tags',[])+[x['category'],x['repository']],'verified':x.get('visual_validation')+' / '+x.get('motion_validation')+' / '+x.get('audio_validation'),'commit':x['commit']})
 for x in read('skill/references/catalogs/adu-templates.json')['templates']:
  entries.append({'id':'adu:'+x['slug'],'title':x['title_zh'],'categories':['template','text-style','effect'],'kind':'motiongit-template','source_url':x['url'],'demo_url':x.get('demo',{}).get('url'),'license':'Per-package code/font/media; current package license not fully read','availability':x['availability'],'method':x['purpose']+'；'+x['constraints'],'tags':[x.get('family',''),x['aspect_ratio']],'verified':'overview/file inventory and demo sampled; not full run','version':x['current_version']})
 entries+=read('resources/starter-pack/index.json')
 if (repo/'resources/upstream-index.json').exists():entries+=read('resources/upstream-index.json')['entries']
 kenney=repo/'resources/kenney-index.json'
 if kenney.exists():entries+=json.loads(kenney.read_text(encoding='utf-8'))
 d={'schema_version':1,'checked_date':'2026-10-30','count':len(entries),'counts_by_kind':dict(collections.Counter(e['kind'] for e in entries)),'counting_note':'Entries include libraries, cards, child variants, demo records, individual assets and recipes. They are not all independent videos/templates. 554 Vincent records retain their hierarchy.','entries':entries}
 for e in entries:
  if e['kind']=='openfilm-page':
   poster=repo/'resources/starter-pack'/e['bundle_relative']/'poster.jpg'
   if poster.exists():
    dest=repo/'docs'/e['preview'];dest.parent.mkdir(parents=True,exist_ok=True);shutil.copy2(poster,dest)
   shutil.copytree(repo/'resources/starter-pack'/e['bundle_relative']/'files',repo/'docs/Starter'/e['bundle_relative']/'files',dirs_exist_ok=True)
 out=repo/'skill/references/catalogs/resource-library.json';out.write_text(json.dumps(d,ensure_ascii=False,indent=2),encoding='utf-8')
 template=(repo/'resources/catalog-shell.html').read_text(encoding='utf-8');html=template.replace('__CATALOG_JSON__',json.dumps(d,ensure_ascii=False).replace('</','<\\/'))
 (repo/'docs/resources.html').write_text(html,encoding='utf-8')
 print(json.dumps({'entries':len(entries),'counts':d['counts_by_kind']},ensure_ascii=False))
if __name__=='__main__':build()
