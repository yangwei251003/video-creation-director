"""Build an editable 30 s OpenFilm integration lab using locally acquired NASA footage.
Not a finished-client template or a claim of aesthetic/audio approval.
"""
import argparse
import array
import json
import math
import shutil
import subprocess
import wave
from pathlib import Path

def build(root, fonts, kenney, ffmpeg):
    src=root/'assets/source';pages=root/'pages';pages.mkdir(parents=True,exist_ok=True)
    (root/'assets/fonts').mkdir(parents=True,exist_ok=True)
    for file in fonts.glob('Noto*'):shutil.copy2(file,root/'assets/fonts'/file.name)
    for name in ['click_001.ogg','confirmation_002.ogg','transition_001.ogg']:
        p=kenney/'Audio'/name
        if p.is_file():shutil.copy2(p,src/name)
    shutil.copy2(kenney/'License.txt',src/'Kenney-CC0.txt')
    # Original quiet harmonic bed, explicitly synthetic; no external music rights implied.
    rate=48000;values=array.array('h')
    chords=[(130.81,164.81,196),(110,130.81,164.81),(87.31,130.81,174.61),(98,146.83,196)]
    for i in range(30*rate):
        t=i/rate;section=min(3,int(t/7.5));local=t-section*7.5
        env=min(1,local/0.6,max(0,(7.5-local)/0.8))*min(1,t/1.5,(30-t)/2)
        chord=chords[section]
        tone=sum(math.sin(2*math.pi*f*t)+0.18*math.sin(2*math.pi*2*f*t) for f in chord)/3
        pulse=(0.82+0.18*math.cos(2*math.pi*1.6*t))
        v=int(32767*0.12*tone*env*pulse);values.extend([v,v])
    with wave.open(str(src/'original-orbit-bed.wav'),'wb') as w:w.setnchannels(2);w.setsampwidth(2);w.setframerate(rate);w.writeframes(values.tobytes())
    css='''@font-face{font-family:Noto;src:url('../assets/fonts/NotoSansSC.ttf')}@font-face{font-family:Serif;src:url('../assets/fonts/NotoSerifSC.ttf')}*{box-sizing:border-box}body{margin:0;background:transparent;color:#f5f1e8;font-family:Noto,sans-serif}#shell{position:absolute;inset:0}.label{position:absolute;left:100px;top:68px;font-size:23px;letter-spacing:5px;color:#8dbab6}.rule{position:absolute;left:100px;top:120px;width:1720px;height:2px;background:#38505c}.num{position:absolute;right:100px;top:64px;font-size:25px;color:#a6b9c2}h1{position:absolute;left:100px;top:186px;margin:0;font-family:Serif;font-size:116px;line-height:1.35;font-weight:700;letter-spacing:-4px}h2{position:absolute;left:100px;top:225px;margin:0;font-family:Serif;font-size:86px;line-height:1.4}p{position:absolute;left:106px;top:410px;font-size:30px;line-height:1.8;color:#b3c6cd}.footer{position:absolute;left:100px;bottom:64px;font-size:22px;color:#90a4af}.tag{display:inline-block;padding:12px 24px;border:1px solid #59716b;color:#e6db9c;font-size:24px}.orbit{position:absolute;border:2px solid #477a82;border-radius:50%;width:760px;height:760px;right:100px;top:160px;transform:rotate(-25deg) scaleY(.48)}.dot{position:absolute;width:20px;height:20px;background:#e0cf86;border-radius:50%;top:50%;left:-10px}.big{position:absolute;right:270px;top:370px;font-size:110px;color:#e0cf86;font-family:Serif}.bottom{position:absolute;left:100px;bottom:110px;width:1720px;height:3px;background:#e0cf86;transform-origin:left}'''
    (pages/'style.css').write_text(css,encoding='utf-8')
    scenes=[
        ('opening',4,'<div class="orbit"><i class="dot"></i></div><div class="big">01</div><h1 id="title">看见地球</h1><p id="subtitle">从观察，到理解。<br>一段可以继续编辑的影像实验。</p><div class="footer">VIDEO DIRECTOR 2.1 × OPENFILM / INTEGRATION STUDY</div>'),
        ('observe',8,'<h2 id="title">每一眼，<br>都有新信息。</h2><p style="top:510px">Landsat 8 轨道可视化<br><span class="tag">01 / 观察</span></p><div class="footer">素材：NASA / Goddard · 轨道动画示意</div>'),
        ('connect',8,'<h2 id="title">把动作，<br>放在节奏里。</h2><p style="top:510px">OCSD 双星协同机动示意<br><span class="tag">02 / 协同</span></p><div class="footer">素材：NASA / Ames · 动画，不是实拍</div>'),
        ('perspective',6,'<h2 id="title">换个视角，<br>继续向前。</h2><p style="top:510px">另一个真实镜头<br><span class="tag">03 / 视角</span></p><div class="footer">素材：NASA / Goddard · 卫星动画示意</div>'),
        ('closing',4,'<h1 id="title">让创作，继续。</h1><p id="subtitle">画面不复播 · 声音有落点 · 修改可保留</p><div class="footer">技术验证片 / 非优秀验收结论 · 音效：Kenney CC0 · 配乐：原创合成</div><div class="orbit"></div>')]
    for n,d,body in scenes:
        script=f'''window.film={{duration:{d},ready:Promise.all([document.fonts.load('700 116px Serif'),document.fonts.load('30px Noto')]),frame(t){{const e=1-Math.pow(1-Math.min(1,t/.7),3);document.querySelector('h1,h2').style.transform='translateY('+((1-e)*40)+'px)';document.querySelector('h1,h2').style.opacity=.08+.92*e;document.querySelector('.bottom').style.transform='scaleX('+Math.min(1,t/{d})+')';}}}};'''
        (pages/(n+'.html')).write_text(f'<!doctype html><html><head><meta charset="utf-8"><link rel="stylesheet" href="style.css"></head><body><div id="shell"><div class="label">ORBIT / A VISUAL STUDY</div><div class="rule"></div><div class="num">30s / 16:9</div>{body}<div class="bottom"></div></div><script>{script}</script></body></html>',encoding='utf-8')
    times=[0,4,12,20,26]; clips=[]
    for (n,d,_),t in zip(scenes,times):clips.append(f'<iframe id="{n}" src="pages/{n}.html#t=0,{d}" at="{t}" data-link="{n}-group"></iframe>')
    land='GSFC_20140211_LDCM_m11481_Orbit.mp4';ocs='ARC-20190801-AAV3211-OCSD-OrbitalManeuver-NASAWeb.mp4'
    videos=[('v-observe',land,7,15,4,'observe'),('v-connect',ocs,24,32,12,'connect'),('v-perspective',land,68,74,20,'perspective')]
    media=''.join(f'<video id="{n}" src="assets/source/{f}#t={a},{b}" at="{t}" muted data-link="{link}-group" style="left:820px;top:220px;width:1000px;height:600px;object-fit:contain;border-radius:20px"></video>' for n,f,a,b,t,link in videos)
    # Use a full-frame static page as background, allowing transparent editable overlays above footage.
    (pages/'background.html').write_text('<!doctype html><body style="margin:0;background:#071c2c"><script>window.film={duration:30,frame(t){}};</script></body>',encoding='utf-8')
    cues=[]
    for n,t,file in [('opening',0.7,'click_001.ogg'),('observe',4.7,'click_001.ogg'),('connect',12.7,'confirmation_002.ogg'),('perspective',20.7,'click_001.ogg'),('closing',26.7,'confirmation_002.ogg')]:
        raw=subprocess.check_output([ffmpeg,'-v','error','-i',str(src/file),'-ar','48000','-ac','1','-f','s16le','-'])
        samples=array.array('h');samples.frombytes(raw);peak=max(abs(x) for x in samples)
        onset=next(i for i,x in enumerate(samples) if abs(x)>=peak*.25)/48000
        length=math.floor(len(samples)/48000*1000)/1000
        cues.append({'id':'sfx-'+n,'shot_id':n,'track':'sfx','file':'assets/source/'+file,'source_range':[0,length],'transient_offset':onset,'anchor_seconds':t,'gain':0.35,'fade_out':min(.03,length/4),'onset_method':'first crossing of 25% sample peak, not perceptual listening'})
    cues.append({'id':'bed','shot_id':None,'track':'music','file':'assets/source/original-orbit-bed.wav','source_range':[0,30],'anchor_seconds':0,'transient_offset':0,'gain':0.7,'fade_in':.4,'fade_out':1.5})
    (root/'audio-cues.json').write_text(json.dumps({'schema_version':1,'duration_seconds':30,'fps':30,'cues':cues},ensure_ascii=False,indent=2),encoding='utf-8')
    sounds=''.join(f'<audio id="{c["id"]}" src="{c["file"]}#t=0,{c["source_range"][1]}" at="{round(c["anchor_seconds"]-c["transient_offset"],3)}" volume="{c["gain"]}" data-link="{c["shot_id"]}-group" overrides=\'[{json.dumps({"fade":[c.get("fade_in",0),c["fade_out"]]})}]\'></audio>' for c in cues if c['track']=='sfx')
    film='<!doctype html><html><head><meta charset="utf-8"><meta name="viewport" content="width=1920, height=1080"></head><body><section>'+''.join(clips)+'</section><section>'+media+'</section><section><iframe id="background" src="pages/background.html#t=0,30"></iframe></section><section>'+sounds+'</section><section><audio id="music" src="assets/source/original-orbit-bed.wav#t=0,30" volume="0.7" overrides=\'[{"fade":[0.4,1.5]}]\'></audio></section></body></html>'
    (root/'film.html').write_text(film,encoding='utf-8')
    (root/'SOURCE-NOTES.md').write_text('''# Sources and limits
NASA footage from images.nasa.gov (Landsat Orbit Swath, OCSD Orbital Maneuver), informational local integration study; credit NASA/Goddard and NASA/Ames. Original audio muted. NASA media guidelines: https://www.nasa.gov/nasa-brand-center/images-and-media/ . No NASA endorsement or logo recreation.
Kenney Interface Sounds: https://kenney.nl/assets/interface-sounds and author's OpenGameArt upload https://opengameart.org/content/interface-sounds ; CC0 license retained. Freesound Wooden Click by BenjaminNelan is a downloaded backup, CC0, HQ MP3 preview.
Music: original procedural harmonic bed, not a recording. Fonts: Noto Sans SC and Noto Serif SC, OFL license retained. Original/alternate media retained privately; raw research videos/transcripts are not public.
This is an integration test, not a claim of full listening or aesthetic approval.
''',encoding='utf-8')

if __name__=='__main__':
    p=argparse.ArgumentParser();p.add_argument('project',type=Path);p.add_argument('--fonts',type=Path,required=True);p.add_argument('--kenney',type=Path,required=True);p.add_argument('--ffmpeg',default='ffmpeg');a=p.parse_args();build(a.project,a.fonts,a.kenney,a.ffmpeg)
