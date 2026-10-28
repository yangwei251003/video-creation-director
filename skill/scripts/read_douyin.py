"""Read public Douyin videos, matched by ID, without user cookies or keys.

Feed-first approach informed by vangie/douyin-transcriber (MIT, BabelCloud).
Only the requested public item's media is retained. No watermark rewriting,
authentication bypass, browser profile reading or third-party parsing service.
"""
import argparse
import hashlib
import json
import math
import re
import urllib.parse
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

UA='Mozilla/5.0 (iPhone; CPU iPhone OS 17_2 like Mac OS X) AppleWebKit/605.1.15 (KHTML, like Gecko) EdgiOS/121.0.2277.107 Version/17.0 Mobile/15E148 Safari/604.1'
DOMAINS=('douyin.com','iesdouyin.com','snssdk.com','amemv.com','365yg.com','douyinvod.com','bytecdn.cn','bytecdn.com','bytedance.com','bytedance.net')
SHARE_DOMAINS=('douyin.com','iesdouyin.com')


def allowed(url,domains=DOMAINS):
    if not isinstance(url,str): return False
    try:
        u=urllib.parse.urlsplit(url)
        host=(u.hostname or '').lower()
        # Even an empty username can carry a password in a URL.
        return u.scheme in ('http','https') and u.username is None and u.password is None and any(host==d or host.endswith('.'+d) for d in domains)
    except ValueError:
        return False


class PlatformRedirect(urllib.request.HTTPRedirectHandler):
    def redirect_request(self,req,fp,code,msg,headers,newurl):
        if not allowed(newurl):
            raise ValueError('Unexpected redirect host; review before proceeding')
        return super().redirect_request(req,fp,code,msg,headers,newurl)


OPENER=urllib.request.build_opener(PlatformRedirect())


def request(url,limit=32*1024*1024):
    if not allowed(url): raise ValueError('URL outside supported platform domains')
    req=urllib.request.Request(url,headers={'User-Agent':UA,'Referer':'https://www.douyin.com/','Accept-Encoding':'identity'})
    with OPENER.open(req,timeout=30) as response:
        if not allowed(response.url): raise ValueError('Unexpected response host')
        data=response.read(limit+1)
        if len(data)>limit: raise ValueError('Response exceeds size limit')
        return data,response.url


def resolve(text):
    match=re.search(r'https?://[^\s<>]+',text)
    if not match: raise ValueError('A public Douyin URL is required')
    url=match.group(0).rstrip('，。；;')
    if not allowed(url,SHARE_DOMAINS): raise ValueError('Not a supported Douyin share URL')
    # Parse only the complete path: query strings and digit prefixes are not IDs.
    match=re.fullmatch(r'/(?:share/)?(?:video|note)/([0-9]+)/?',urllib.parse.urlsplit(url).path)
    if not match:
        _,url=request(url,2*1024*1024)
        if not allowed(url,SHARE_DOMAINS): raise ValueError('Redirect is not a supported Douyin share URL')
        match=re.fullmatch(r'/(?:share/)?(?:video|note)/([0-9]+)/?',urllib.parse.urlsplit(url).path)
    if not match: raise ValueError('No video ID in public redirect')
    return match.group(1)


def acquire(video_id,out,max_mb):
    if not isinstance(video_id,str) or not re.fullmatch(r'[0-9]+',video_id): raise ValueError('A complete numeric video ID is required')
    if not isinstance(max_mb,int) or isinstance(max_mb,bool) or max_mb<=0: raise ValueError('max-mb must be a positive integer')
    media=out/'source.mp4'
    old=out/'source-info.json'
    # Verify cached identity before any network call; a valid cache works offline.
    if media.is_file() and old.is_file():
        previous=json.loads(old.read_text(encoding='utf-8'))
        if not isinstance(previous,dict): raise ValueError('Existing identity record is invalid')
        with media.open('rb') as file:
            same=previous.get('id')==video_id and previous.get('sha256')==hashlib.file_digest(file,'sha256').hexdigest()
        if same: return media,previous
        raise ValueError('Existing media does not match saved identity/hash; choose a new output directory')
    if media.exists(): raise ValueError('Existing media has no identity record; choose a new output directory')
    endpoint='https://aweme.snssdk.com/aweme/v1/feed/?'+urllib.parse.urlencode({'aweme_id':video_id,'version_code':'270800','app_name':'aweme'})
    raw,_=request(endpoint)
    data=json.loads(raw)
    if data.get('status_code')!=0: raise ValueError('Platform did not return a successful public feed')
    item=next((x for x in data.get('aweme_list',[]) if str(x.get('aweme_id'))==video_id),None)
    if not item: raise ValueError('Requested ID absent; refusing unrelated recommended video')
    video=item.get('video',{})
    urls=video.get('play_addr_h264',{}).get('url_list',[]) or video.get('play_addr',{}).get('url_list',[])
    urls=[u for u in urls if allowed(u)]
    if not urls: raise ValueError('No supported media URL')
    info={'source':'https://www.douyin.com/video/'+video_id,'id':video_id,'title':item.get('desc'),'author':item.get('author',{}).get('nickname'),'duration_hint_seconds':video.get('duration',0)/1000,'created_utc':datetime.now(timezone.utc).isoformat(),'acquisition':'public feed exact-ID match','credentials_used':False,'complete_video_viewed':False,'audio_listened':False}
    last=''
    for url in urls[:2]:
        try:
            req=urllib.request.Request(url,headers={'User-Agent':UA,'Referer':'https://www.douyin.com/','Accept-Encoding':'identity'})
            digest=hashlib.sha256(); size=0
            with OPENER.open(req,timeout=60) as response, (out/'source.part').open('wb') as dest:
                if not allowed(response.url): raise ValueError('Unexpected media response host')
                length=response.headers.get('Content-Length')
                if length and int(length)>max_mb*1024*1024: raise ValueError('Media exceeds size budget')
                while block:=response.read(1024*1024):
                    size+=len(block)
                    if size>max_mb*1024*1024: raise ValueError('Media exceeds size budget')
                    digest.update(block);dest.write(block)
            (out/'source.part').replace(media)
            info.update({'bytes':size,'sha256':digest.hexdigest(),'media_file':media.name})
            old.write_text(json.dumps(info,ensure_ascii=False,indent=2),encoding='utf-8')
            return media,info
        except (OSError,ValueError) as exc:
            last=type(exc).__name__
    raise RuntimeError('Public media download failed: '+last)


def transcribe(media,out,model_path):
    from faster_whisper import WhisperModel
    model=WhisperModel(model_path,device='cpu',compute_type='int8',cpu_threads=4,num_workers=1)
    segments,info=model.transcribe(str(media),language='zh',beam_size=5,vad_filter=True,word_timestamps=True,condition_on_previous_text=False)
    result=[]
    for seg in segments:
        result.append({'start':round(seg.start,3),'end':round(seg.end,3),'text':seg.text.strip(),'avg_logprob':seg.avg_logprob,'words':[{'start':w.start,'end':w.end,'word':w.word,'probability':w.probability} for w in (seg.words or [])]})
        if len(result)%30==0: print('ASR processed through %.1f seconds'%seg.end,flush=True)
    data={'type':'automatic_local_speech_recognition','model':Path(model_path).name,'language':info.language,'duration_seconds':info.duration,'segments':result,'human_audio_review':False,'warning':'ASR can mishear names, code and punctuation; cross-check frames and sources.'}
    (out/'transcript.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    (out/'transcript.txt').write_text('\n'.join(f"[{s['start']:.2f}–{s['end']:.2f}] {s['text']}" for s in result),encoding='utf-8')
    return len(result)


def inspect_frames(media,out,count,times,ocr):
    import cv2
    cap=cv2.VideoCapture(str(media))
    try:
        if not cap.isOpened(): raise ValueError('Cannot decode local video')
        fps=cap.get(cv2.CAP_PROP_FPS);total=cap.get(cv2.CAP_PROP_FRAME_COUNT)
        if not math.isfinite(fps) or not math.isfinite(total) or fps<=0 or total<=0: raise ValueError('Invalid duration or frame rate')
        duration=total/fps
        if not isinstance(count,int) or isinstance(count,bool) or not 0<=count<=120 or len(times)>120: raise ValueError('Use at most 120 samples per run')
        if any(not isinstance(t,(int,float)) or isinstance(t,bool) or not math.isfinite(t) or not 0<=t<duration for t in times): raise ValueError('Requested time outside video')
        selected=sorted(set([round(i*max(0,duration-1)/max(1,count-1),3) for i in range(count)]+times))
        if len(selected)>120: raise ValueError('Use at most 120 combined samples per run')
        engine=None
        if ocr:
            from rapidocr import RapidOCR
            engine=RapidOCR()
        dest=out/'frames';dest.mkdir(exist_ok=True)
        records=[]
        for index,t in enumerate(selected):
            cap.set(cv2.CAP_PROP_POS_MSEC,t*1000)
            ok,frame=cap.read()
            if not ok: raise ValueError('Frame extraction failed at '+str(t))
            # Record the decoder position separately from the requested seek time.
            decoded_time=cap.get(cv2.CAP_PROP_POS_MSEC)/1000
            decoded_index=cap.get(cv2.CAP_PROP_POS_FRAMES)-1
            name='frame-%03d-%013.6f.jpg'%(index,t)
            ok,encoded=cv2.imencode('.jpg',frame,[cv2.IMWRITE_JPEG_QUALITY,92])
            if not ok: raise ValueError('Frame encoding failed')
            encoded.tofile(str(dest/name))
            entry={'requested_time_seconds':t,'file':'frames/'+name,
                   'decoded_time_seconds':decoded_time if math.isfinite(decoded_time) and decoded_time>=0 else None,
                   'decoded_frame_index':int(decoded_index) if math.isfinite(decoded_index) and decoded_index>=0 else None}
            if engine:
                result=engine(frame)
                entry['ocr_text']=list(result.txts) if result.txts is not None else []
                entry['ocr_confidence']=[float(x) for x in result.scores] if result.scores is not None else []
            records.append(entry)
    finally:
        cap.release()
    data={'type':'sampled_frames','duration_seconds':duration,'fps':fps,'frames':records,'continuous_video_review':False,'warning':'OCR may misread text. Frame sampling cannot establish motion quality or full visual coverage.'}
    (out/'frames.json').write_text(json.dumps(data,ensure_ascii=False,indent=2),encoding='utf-8')
    return len(records)


def main():
    p=argparse.ArgumentParser()
    p.add_argument('source')
    p.add_argument('--out',required=True,type=Path)
    p.add_argument('--max-mb',type=int,default=400)
    p.add_argument('--transcribe',action='store_true')
    p.add_argument('--model',default='small')
    p.add_argument('--frames',type=int,default=0,help='Evenly sampled frames, maximum 120')
    p.add_argument('--time',type=float,action='append',default=[],help='Additional exact sample time in seconds')
    p.add_argument('--ocr',action='store_true',help='Recognise text on sampled frames')
    a=p.parse_args()
    a.out.mkdir(parents=True,exist_ok=True)
    vid=resolve(a.source);media,info=acquire(vid,a.out,a.max_mb)
    print(json.dumps({k:v for k,v in info.items() if k not in ('sha256',)},ensure_ascii=False,indent=2),flush=True)
    if a.frames or a.time:
        print('Saved frames:',inspect_frames(media,a.out,a.frames,a.time,a.ocr),flush=True)
    if a.transcribe:
        count=transcribe(media,a.out,a.model)
        print('Saved timed ASR segments:',count,flush=True)


if __name__=='__main__': main()
