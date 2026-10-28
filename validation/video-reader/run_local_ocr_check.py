"""One-frame local OCR smoke test. Private frame/text are excluded from Git."""
from pathlib import Path
import hashlib
import json
import math
import socket
import types
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent
PROJECT = ROOT.parents[1]
SCRIPT = PROJECT/'skill/scripts/read_douyin.py'
SOURCE = PROJECT/'.research-sources/tutorials/xiaofeng/source.mp4'
OUT = ROOT/'private-ocr'
OUT.mkdir(exist_ok=True)
def digest(path):
    with path.open('rb') as f: return hashlib.file_digest(f,'sha256').hexdigest()
before = digest(SOURCE)
reader = types.ModuleType('local_reader')
reader.__file__ = str(SCRIPT)
exec(compile(SCRIPT.read_text(encoding='utf-8'),str(SCRIPT),'exec'),reader.__dict__)
with patch.object(socket.socket,'connect',side_effect=RuntimeError('Network disabled during local validation')):
    import cv2
    cap=cv2.VideoCapture(str(SOURCE))
    duration=cap.get(cv2.CAP_PROP_FRAME_COUNT)/cap.get(cv2.CAP_PROP_FPS)
    cap.release()
    chosen=min(12.0,duration/2)
    count=reader.inspect_frames(SOURCE,OUT,0,[chosen],True)
data=json.loads((OUT/'frames.json').read_text(encoding='utf-8'))
entry=data['frames'][0]
scores=entry['ocr_confidence']
checks={
    'single_frame':count==1 and len(data['frames'])==1,
    'sampled_type':data['type']=='sampled_frames',
    'not_continuous_review':data['continuous_video_review'] is False,
    'warning_present':bool(data.get('warning')),
    'requested_time_preserved':entry['requested_time_seconds']==chosen,
    'decoded_time_present':isinstance(entry.get('decoded_time_seconds'),(int,float)),
    'decoded_frame_present':isinstance(entry.get('decoded_frame_index'),int),
    'image_exists':(OUT/entry['file']).is_file(),
    'ocr_arrays_aligned':len(entry['ocr_text'])==len(scores),
    'ocr_text_detected':bool(entry['ocr_text']),
    'scores_finite_in_unit_interval':all(math.isfinite(x) and 0<=x<=1 for x in scores),
    'source_unchanged':digest(SOURCE)==before,
}
report={'type':'local_ocr_contract_test','third_party_content_included':False,
    'source_sha256_before_and_after':before,'script_sha256':digest(SCRIPT),
    'network':'disabled during test','new_media_downloaded':False,'installed_dependencies':False,
    'sampled_frame_count':count,'requested_time_seconds':chosen,
    'decoded_time_seconds':entry.get('decoded_time_seconds'),'decoded_frame_index':entry.get('decoded_frame_index'),
    'ocr_text_item_count':len(entry['ocr_text']),'confidence_min':min(scores) if scores else None,
    'confidence_max':max(scores) if scores else None,'checks':checks,'passed':all(checks.values()),
    'scope_notice':'One automated frame OCR only; no full viewing, listening, OCR accuracy certification or public redistribution.'}
(ROOT/'local-ocr-check.json').write_text(json.dumps(report,ensure_ascii=False,indent=2),encoding='utf-8')
print(json.dumps(report,ensure_ascii=False,indent=2))
raise SystemExit(0 if report['passed'] else 1)
