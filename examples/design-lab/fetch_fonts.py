"""Fetch official OFL fonts into this example, with reproducible Git blob checks."""
import hashlib
import json
import urllib.request
from pathlib import Path

root = Path(__file__).resolve().parent / 'public' / 'fonts'
root.mkdir(parents=True, exist_ok=True)
items = [
    ('NotoSansSC.ttf','notosanssc/NotoSansSC%5Bwght%5D.ttf','fb0637bafbcd804fe32152370a1225990745b4bc'),
    ('NotoSerifSC.ttf','notoserifsc/NotoSerifSC%5Bwght%5D.ttf','eab063faf229160a52d3760f5555150e4eb9e5bf'),
    ('NotoSansSC-OFL.txt','notosanssc/OFL.txt','1c9f43281b8f216c5461fe9ac729afbade7724e4'),
    ('NotoSerifSC-OFL.txt','notoserifsc/OFL.txt','94d1bf7b52481343e2983fb7751e8b7abe1ea07b')
]
records=[]
for name,tail,blob in items:
    url='https://raw.githubusercontent.com/google/fonts/main/ofl/'+tail
    data=urllib.request.urlopen(url,timeout=90).read()
    actual=hashlib.sha1(b'blob '+str(len(data)).encode()+b'\0'+data).hexdigest()
    if actual!=blob:
        raise ValueError('Upstream changed; review version before updating '+name)
    (root/name).write_bytes(data)
    records.append({'file':name,'source':url,'git_blob':blob,'sha256':hashlib.sha256(data).hexdigest(),'licence':'OFL-1.1'})
(root/'manifest.json').write_text(json.dumps(records,indent=2),encoding='utf-8')
print('Verified official font files and licences:',len(records))
