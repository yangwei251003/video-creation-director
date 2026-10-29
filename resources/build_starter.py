"""Original MIT OpenFilm pages. Rebuild only the generated source pack, never user projects."""
import json,hashlib
from pathlib import Path
ROOT=Path(__file__).resolve().parent/'starter-pack'
SPECS=[
('ink-serif','纸墨宋体','text-style','serif'),('bold-outline','硬朗描边','text-style','outline'),('gold-foil','柔金字面','text-style','gold'),('neon-line','霓虹轮廓','text-style','neon'),('magazine-cutout','编辑拼贴','text-style','cutout'),('comic-burst','漫画强调','text-style','comic'),
('rise','错位升起','text-animation','rise'),('stagger','逐字节奏','text-animation','stagger'),('blur','聚焦显字','text-animation','blur'),('tracking','字距收束','text-animation','tracking'),('clip','遮罩揭示','text-animation','clip'),('count','数字增长','text-animation','count'),
('orbit','轨道关系线','effect','orbit'),('sweep','流动光带','effect','sweep'),('glass','玻璃信息卡','effect','glass'),('particles','确定性粒子','effect','particles'),
('wipe','方向遮挡转场','transition','wipe'),('iris','圆形开合转场','transition','iris'),('shutter','百叶遮挡转场','transition','shutter'),('dip','白场闪切转场','transition','dip'),
('warm','暖调滤镜示例','filter','warm'),('cool','冷调滤镜示例','filter','cool'),('mono','黑白滤镜示例','filter','mono'),('film','复古滤镜示例','filter','film'),
('chapter','章节开场','template','chapter'),('compare','双项对比','template','compare'),('evidence','证据卡片','template','evidence')]
HTML='''<!doctype html><html lang="zh-CN"><head><meta charset="utf-8"><meta name="viewport" content="width=1920,height=1080"><style>
*{box-sizing:border-box}body{margin:0;width:1920px;height:1080px;overflow:hidden;background:transparent;font-family:"Microsoft YaHei","Noto Sans SC",sans-serif;color:#fff4dc}#stage{position:relative;width:1920px;height:1080px;background:#112a32;overflow:hidden}.guide{position:absolute;inset:80px;border:1px solid #c1d6c033;border-radius:3px}.eyebrow{position:absolute;left:130px;top:122px;font-size:25px;letter-spacing:7px;color:#dbd2aa}#title{position:absolute;left:130px;top:310px;margin:0;font-size:116px;font-weight:800;line-height:1.35;letter-spacing:-3px;z-index:3;max-width:1660px}#subtitle{position:absolute;left:138px;top:532px;font-size:34px;line-height:1.7;color:#bdcfc8;z-index:3}.line{position:absolute;left:138px;top:684px;width:1020px;height:3px;background:#bda465;transform-origin:left}.number{position:absolute;right:150px;top:720px;font-family:Georgia,serif;font-size:130px;color:#d3bd77}#ornament{position:absolute;left:1080px;top:300px;width:540px;height:540px;border:1px solid #bda46588;border-radius:50%;transform:rotate(-28deg) scaleY(.55)}#fx{position:absolute;inset:0;pointer-events:none;z-index:5}.dot{position:absolute;width:7px;height:7px;background:#d3bd77;border-radius:50%}.panel{position:absolute;top:0;bottom:0;background:#d5b76a;width:100%}.sheet{position:absolute;top:0;bottom:0;width:20%;background:#bda465}#sample{position:absolute;inset:0;width:100%;height:100%;object-fit:cover}.card{position:absolute;background:#fff4dc;color:#142c30;border-radius:20px;padding:50px;width:720px;top:365px;font-size:48px}.card p{font-size:29px;line-height:1.6}.credit{position:absolute;left:138px;bottom:108px;font-size:22px;letter-spacing:3px;color:#a8bab2}b{font-weight:800}#title span{display:inline-block}
</style></head><body><div id="stage"><div class="guide"></div><div class="eyebrow">VIDEO DIRECTOR / EDITABLE STUDY</div><h1 id="title">让信息被看见</h1><p id="subtitle">一个明确焦点，一段恰当节奏。</p><div class="line"></div><div id="ornament"></div><div class="number">01</div><div class="credit">__NAME__ · 原创可编辑组件</div><div id="fx"></div></div><script>
const kind=__KIND__;const title=document.querySelector('#title'),sub=document.querySelector('#subtitle'),fx=document.querySelector('#fx'),stage=document.querySelector('#stage');
const clamp=x=>Math.max(0,Math.min(1,x)),ease=x=>1-Math.pow(1-clamp(x),3);
if(kind==='serif'){title.style.fontFamily='"Noto Serif SC",SimSun,serif';stage.style.background='#f1ebdc';title.style.color='#202b27';sub.style.color='#506258';document.querySelector('.eyebrow').style.color='#6b654e';document.querySelector('.credit').style.color='#506258';document.querySelector('.number').style.color='#8a6b36';}
if(kind==='outline'){title.style.color='#112a32';title.style.webkitTextStroke='3px #fff4dc';title.style.textShadow='8px 8px 0 #ba805b';}
if(kind==='gold'){title.style.background='linear-gradient(110deg,#927443,#f8e3a9,#aa8449)';title.style.backgroundClip='text';title.style.color='transparent';}
if(kind==='neon'){title.style.color='#d8fff1';title.style.textShadow='0 0 6px #a9dbbe,0 0 30px #4c9670';}
if(kind==='cutout'){title.style.background='#ecddbe';title.style.color='#1c3134';title.style.padding='10px 35px';title.style.transform='rotate(-3deg)';}
if(kind==='comic'){title.style.color='#f6d879';title.style.webkitTextStroke='2px #13282f';title.style.textShadow='9px 10px 0 #b35b46';}
if(kind==='glass'){stage.style.background='radial-gradient(ellipse at 80% 20%,#456968,#172d3d 60%)';title.style.padding='30px 45px';title.style.background='#ffffff12';title.style.border='1px solid #d9e3d530';title.style.borderRadius='35px';}
if(kind==='stagger'){title.textContent='';for(const c of '让信息被看见'){const s=document.createElement('span');s.textContent=c;title.append(s);}}
if(kind==='count'){title.textContent='更清晰';title.style.top='460px';title.style.fontSize='74px';sub.style.top='595px';const value=document.createElement('div');value.id='value';value.style.cssText='position:absolute;left:130px;top:230px;font-size:180px;font-weight:800;color:#e4cc85';stage.append(value);}
if(kind==='particles'){for(let i=0;i<40;i++){const e=document.createElement('i');e.className='dot';e.dataset.n=i;fx.append(e);}}
if(kind==='sweep'){fx.style.background='linear-gradient(110deg,transparent 30%,#eedca621 50%,transparent 70%)';}
if(['wipe','iris','shutter','dip'].includes(kind)){stage.style.background='transparent';[...stage.children].filter(e=>e!==fx).forEach(e=>e.style.display='none');fx.innerHTML=kind==='shutter'?Array.from({length:5},(_,i)=>'<div class="sheet" style="left:'+i*20+'%"></div>').join(''):'<div class="panel"></div>';if(kind==='dip')fx.firstChild.style.background='#fffdf3';}
if(['warm','cool','mono','film'].includes(kind)){const img=document.createElement('img');img.id='sample';img.src='sample.svg';stage.prepend(img);img.style.filter={warm:'sepia(.28) saturate(.85) contrast(1.06)',cool:'hue-rotate(18deg) saturate(.75) contrast(1.08)',mono:'grayscale(1) contrast(1.15)',film:'sepia(.35) saturate(.65) contrast(.94) brightness(1.05)'}[kind];const shade=document.createElement('div');shade.style.cssText='position:absolute;inset:0;background:linear-gradient(90deg,#10262be8,#10262b99 68%,#10262b33)';img.after(shade);title.style.fontSize='100px';title.textContent='替换图片后应用滤镜';sub.textContent='示例仅影响本页图片，不是跨轨道全片滤镜。';}
if(kind==='chapter'){title.innerHTML='01 / 进入主题';sub.textContent='章节名可编辑，层级与阅读时间先确定。';}
if(kind==='compare'){title.style.top='210px';title.style.fontSize='70px';title.textContent='让比较一眼清楚';sub.style.display='none';for(const [i,txt] of ['方案 A','方案 B'].entries()){const d=document.createElement('div');d.id='card-'+i;d.className='card';d.style.left=(138+i*850)+'px';d.innerHTML='<b>'+txt+'</b><p>比较维度与事实<br>用真实数据替换示例</p>';stage.append(d);}}
if(kind==='evidence'){title.style.fontSize='85px';title.style.top='180px';title.textContent='观点，需要证据';sub.style.top='360px';sub.innerHTML='观察：填写可核验事实<br>来源：填写原始来源与日期<br>结论：避免超出证据';}
window.film={duration:4,ready:Promise.all([document.fonts.ready,...[...document.images].map(i=>i.decode())]),frame(t){
 const u=clamp(t/4),e=ease(t/.7);document.querySelector('.line').style.transform='scaleX('+clamp(t/3)+')';
 if(['rise','chapter','evidence'].includes(kind)){title.style.opacity=e;title.style.transform='translateY('+(1-e)*50+'px)';}
 if(kind==='stagger')[...title.children].forEach((s,i)=>{let q=ease((t-i*.085)/.45);s.style.opacity=q;s.style.transform='translateY('+(1-q)*55+'px)';});
 if(kind==='blur'){title.style.filter='blur('+(1-e)*20+'px)';title.style.opacity=e;}
 if(kind==='tracking'){title.style.letterSpacing=(20*(1-e)-3)+'px';title.style.opacity=e;}
 if(kind==='clip')title.style.clipPath='inset(0 '+(1-e)*100+'% 0 0)';
 if(kind==='count')document.querySelector('#value').textContent=Math.round(ease(t/1.7)*100)+'%';
 if(kind==='orbit')document.querySelector('#ornament').style.transform='rotate('+(-28+u*80)+'deg) scaleY(.55)';
 if(kind==='sweep')fx.style.transform='translateX('+(-100+u*200)+'%)';
 if(kind==='particles')[...fx.children].forEach((d,i)=>{d.style.left=((i*149.37+41)%1920)+'px';d.style.top=((i*197.13-t*(13+i%7)*14)%1080+1080)%1080+'px';d.style.opacity=.15+.5*(.5+.5*Math.sin(t+i));});
 if(kind==='wipe')fx.firstChild.style.transform='translateX('+(-100+200*u)+'%)';
 if(kind==='iris')fx.firstChild.style.clipPath='circle('+(Math.sin(Math.PI*u)*78)+'% at 50% 50%)';
 if(kind==='shutter')[...fx.children].forEach((d,i)=>d.style.transform='scaleY('+Math.max(0,Math.sin(Math.PI*clamp((u-i*.025)/.9)))+')');
 if(kind==='dip')fx.firstChild.style.opacity=Math.pow(Math.sin(Math.PI*u),5);
}};
window.addEventListener('message',async event=>{if(event.source!==parent||event.data?.type!=='director-preview-frame'||!Number.isFinite(event.data.t))return;await window.film.ready;window.film.frame(Math.max(0,Math.min(4,event.data.t)));});
</script></body></html>'''
SVG='<svg xmlns="http://www.w3.org/2000/svg" width="1920" height="1080" viewBox="0 0 1920 1080"><defs><linearGradient id="g" x2="0" y2="1"><stop stop-color="#bad0c3"/><stop offset="1" stop-color="#376b62"/></linearGradient></defs><path fill="url(#g)" d="M0 0h1920v1080H0z"/><circle cx="1450" cy="240" r="125" fill="#f0cf7c"/><path d="M0 810L550 370l320 270 390-330 660 620v150H0" fill="#235e58"/><path d="M0 910l500-230 470 210 550-130 400 150v170H0" fill="#173d3a"/></svg>'
def build():
 entries=[]
 for id,name,cat,kind in SPECS:
  dest=ROOT/cat/id;files=dest/'files';files.mkdir(parents=True,exist_ok=True)
  page=HTML.replace('__NAME__',name).replace('__KIND__',json.dumps(kind))
  (files/'index.html').write_text(page,encoding='utf-8')
  if cat=='filter':(files/'sample.svg').write_text(SVG,encoding='utf-8')
  fields=[{'name':'标题','type':'text','at':'#title'},{'name':'副标题','type':'text','at':'#subtitle'}]
  if kind=='compare':fields=[fields[0]]+[{'name':label,'type':'text','at':selector} for label,selector in [('左标题','#card-0 b'),('左内容','#card-0 p'),('右标题','#card-1 b'),('右内容','#card-1 p')]]
  if cat=='transition':fields=[]
  props=json.dumps(fields,ensure_ascii=False)
  bundle={'version':2,'savedAt':'2026-10-29T00:00:00Z','kind':'clip','clip':{'src':'index.html','time':[0,4],'attrs':{'data-props':props}},'durationMs':4000,'w':1920,'h':1080}
  (dest/'saved.json').write_text(json.dumps(bundle,ensure_ascii=False,indent=2),encoding='utf-8')
  (dest/'LICENSE.txt').write_text((ROOT.parent.parent/'LICENSE').read_text(encoding='utf-8'),encoding='utf-8')
  entries.append({'id':'starter:'+id,'title':name,'categories':[cat],'kind':'openfilm-page','source_url':'https://github.com/yangwei251003/video-creation-director/tree/main/resources/starter-pack/'+cat+'/'+id,'license':'MIT','availability':'native-saved','bundle_relative':cat+'/'+id,'preview':'resource-previews/'+id+'.jpg','method':('复制滤镜CSS到具体媒体元素；页面是可编辑示例，不改变其他轨道' if cat=='filter' else 'OpenFilm Saved插入透明覆盖页，放在两片段交界；按事件重定时frame(t)，不要只裁短后丢失出场半程' if cat=='transition' else 'OpenFilm Saved原生插入，文字保留DOM，可编辑；frame(t)确定性驱动'),'verified':'headless frame seeking tested; native import/render recorded separately'})
 (ROOT/'index.json').write_text(json.dumps(entries,ensure_ascii=False,indent=2),encoding='utf-8')
 print(json.dumps({'original_bundles':len(entries)}))
if __name__=='__main__':build()
