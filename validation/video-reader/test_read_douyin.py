"""Offline reader contract tests. No real network calls or third-party content."""
import hashlib
import io
import json
from pathlib import Path
import sys
import types
import unittest
import uuid
from unittest.mock import patch

ROOT = Path(__file__).resolve().parent
FIXTURE_RUN = ROOT/'fixtures'/uuid.uuid4().hex[:10]
SCRIPT = ROOT.parents[1] / 'skill/scripts/read_douyin.py'
reader = types.ModuleType('tested_douyin_reader')
reader.__file__ = str(SCRIPT)
exec(compile(SCRIPT.read_text(encoding='utf-8'), str(SCRIPT), 'exec'), reader.__dict__)

class FakeResponse(io.BytesIO):
    def __init__(self, data=b'synthetic video', url='https://v1.douyinvod.com/public.mp4'):
        super().__init__(data)
        self.url = url
        self.headers = {'Content-Length': str(len(data))}

class FakeOpener:
    def __init__(self, url='https://v1.douyinvod.com/public.mp4'):
        self.urls = []
        self.final_url = url
    def open(self, req, timeout):
        self.urls.append(req.full_url)
        return FakeResponse(url=self.final_url)

class FakeCapture:
    def __init__(self): self.pos = 0; self.released = False
    def isOpened(self): return True
    def get(self, prop):
        return {5:30,7:9000,0:self.pos,1:self.pos/1000*30+1}.get(prop,0)
    def set(self, prop, value): self.pos=value; return True
    def read(self): return True, object()
    def release(self): self.released=True

def fake_cv(cap):
    return types.SimpleNamespace(VideoCapture=lambda _:cap,CAP_PROP_FPS=5,CAP_PROP_FRAME_COUNT=7,
        CAP_PROP_POS_MSEC=0,CAP_PROP_POS_FRAMES=1,IMWRITE_JPEG_QUALITY=1,
        imencode=lambda *args:(True,types.SimpleNamespace(tofile=lambda name:Path(name).write_bytes(b'synthetic frame'))))

def feed(ids=('unrelated','123')):
    return json.dumps({'status_code':0,'aweme_list':[{'aweme_id':i,'desc':'Synthetic item '+i,
        'author':{'nickname':'Fixture'},'video':{'duration':1000,'play_addr':{'url_list':['https://v1.douyinvod.com/'+i+'.mp4']}}} for i in ids]}).encode()

class ReaderTests(unittest.TestCase):
    def setUp(self):
        self.out = FIXTURE_RUN/self._testMethodName
        self.out.mkdir(parents=True,exist_ok=True)
    def assertRejected(self, fn):
        with self.assertRaises(ValueError): fn()
    def cached(self, video_id='123', valid=True):
        media=self.out/'source.mp4'; media.write_bytes(b'Synthetic cached media')
        digest=hashlib.sha256(media.read_bytes()).hexdigest()
        info={'id':video_id,'sha256':digest if valid else 'bad','complete_video_viewed':False,'audio_listened':False}
        (self.out/'source-info.json').write_text(json.dumps(info),encoding='utf-8')
        return media
    def test_allowed_domains(self):
        self.assertTrue(reader.allowed('https://v1.douyinvod.com/a'))
        for url in ['https://douyin.com.evil.invalid/a','https://evil.invalid/douyin.com','file:///a','https://u:p@douyin.com/a']:
            self.assertFalse(reader.allowed(url),url)
    def test_empty_username_password_rejected(self):
        self.assertFalse(reader.allowed('https://:secret@douyin.com/video/123'))
    def test_canonical_and_share_exact_id(self):
        for u in ['https://www.douyin.com/video/123?x=1','https://www.iesdouyin.com/share/video/123/','https://www.douyin.com/note/123']:
            self.assertEqual(reader.resolve(u),'123')
    def test_query_id_not_video_identity(self):
        with patch.object(reader,'request',return_value=(b'', 'https://www.douyin.com/search?redirect=/video/123')):
            self.assertRejected(lambda:reader.resolve('https://www.douyin.com/search?redirect=/video/123'))
    def test_partial_digit_path_rejected(self):
        with patch.object(reader,'request',return_value=(b'', 'https://www.douyin.com/video/123abc')):
            self.assertRejected(lambda:reader.resolve('https://www.douyin.com/video/123abc'))
    def test_cdn_is_not_share_entry(self):
        self.assertRejected(lambda:reader.resolve('https://v1.douyinvod.com/video/123'))
    def test_short_redirect_canonical(self):
        with patch.object(reader,'request',return_value=(b'', 'https://www.iesdouyin.com/share/video/123/?r=1')):
            self.assertEqual(reader.resolve('分享 https://v.douyin.com/abc/ 复制链接'),'123')
    def test_short_redirect_external_rejected(self):
        with patch.object(reader,'request',return_value=(b'', 'https://outside.invalid/video/123')):
            self.assertRejected(lambda:reader.resolve('https://v.douyin.com/abc/'))
    def test_redirect_handler_external_rejected(self):
        req=reader.urllib.request.Request('https://v.douyin.com/a')
        self.assertRejected(lambda:reader.PlatformRedirect().redirect_request(req,None,302,'Found',{},'https://outside.invalid/a'))
    def test_request_final_domain_rechecked(self):
        with patch.object(reader,'OPENER',FakeOpener('https://outside.invalid/a')):
            self.assertRejected(lambda:reader.request('https://www.douyin.com/a'))
    def test_feed_exact_id(self):
        op=FakeOpener()
        with patch.object(reader,'request',return_value=(feed(), 'https://aweme.snssdk.com/a')),patch.object(reader,'OPENER',op):
            path,info=reader.acquire('123',self.out,1)
        self.assertEqual(info['id'],'123')
        self.assertEqual(op.urls,['https://v1.douyinvod.com/123.mp4'])
        self.assertFalse(info['complete_video_viewed']); self.assertFalse(info['audio_listened'])
        self.assertEqual(info['sha256'],hashlib.sha256(path.read_bytes()).hexdigest())
    def test_feed_prefix_match_rejected(self):
        with patch.object(reader,'request',return_value=(feed(('1234',)),'')),patch.object(reader,'OPENER',FakeOpener()) as op:
            self.assertRejected(lambda:reader.acquire('123',self.out,1))
            self.assertEqual(op.urls,[])
    def test_cache_reuses_offline(self):
        existing=self.cached()
        with patch.object(reader,'request',side_effect=RuntimeError('NETWORK_FORBIDDEN')) as request:
            media,info=reader.acquire('123',self.out,1)
        self.assertEqual(media,existing); request.assert_not_called()
    def test_cache_bad_hash_rejected_before_network(self):
        existing=self.cached(valid=False); before=existing.read_bytes()
        with patch.object(reader,'request',side_effect=RuntimeError('NETWORK_FORBIDDEN')) as request:
            self.assertRejected(lambda:reader.acquire('123',self.out,1))
        self.assertEqual(existing.read_bytes(),before); request.assert_not_called()
    def test_cache_wrong_id_rejected_before_network(self):
        self.cached(video_id='1234')
        with patch.object(reader,'request',side_effect=RuntimeError('NETWORK_FORBIDDEN')) as request:
            self.assertRejected(lambda:reader.acquire('123',self.out,1))
        request.assert_not_called()
    def test_max_mb_must_be_positive(self):
        with patch.object(reader,'request',side_effect=RuntimeError('NETWORK_FORBIDDEN')) as request:
            for value in [0,-1,float('nan'),float('inf'),True]:
                self.assertRejected(lambda:reader.acquire('123',self.out,value))
        request.assert_not_called()
    def test_combined_sample_limit(self):
        with patch.dict(sys.modules,{'cv2':fake_cv(FakeCapture())}):
            self.assertRejected(lambda:reader.inspect_frames(Path('fixture.mp4'),self.out,120,[i+.123 for i in range(120)],False))
    def test_sample_names_do_not_collide(self):
        with patch.dict(sys.modules,{'cv2':fake_cv(FakeCapture())}):
            self.assertEqual(reader.inspect_frames(Path('fixture.mp4'),self.out,0,[1.0001,1.0002],False),2)
        data=json.loads((self.out/'frames.json').read_text(encoding='utf-8'))
        self.assertEqual(len({x['file'] for x in data['frames']}),2)
        self.assertFalse(data['continuous_video_review'])
    def test_nan_time_rejected(self):
        with patch.dict(sys.modules,{'cv2':fake_cv(FakeCapture())}):
            self.assertRejected(lambda:reader.inspect_frames(Path('fixture.mp4'),self.out,0,[float('nan')],False))
    def test_capture_released_on_failure(self):
        cap=FakeCapture()
        with patch.dict(sys.modules,{'cv2':fake_cv(cap)}):
            self.assertRejected(lambda:reader.inspect_frames(Path('fixture.mp4'),self.out,0,[-1],False))
        self.assertTrue(cap.released)

if __name__=='__main__':
    report=ROOT/('results-'+(sys.argv[1] if len(sys.argv)>1 else 'current')+'.json')
    suite=unittest.defaultTestLoader.loadTestsFromTestCase(ReaderTests)
    result=unittest.TextTestRunner(verbosity=2).run(suite)
    report.write_text(json.dumps({'script_sha256':hashlib.sha256(SCRIPT.read_bytes()).hexdigest(),
        'tests':result.testsRun,'failures':[{'test':str(t),'traceback':e} for t,e in result.failures],
        'errors':[{'test':str(t),'traceback':e} for t,e in result.errors],
        'passed':result.testsRun-len(result.failures)-len(result.errors),'network':'mocked; no download'},ensure_ascii=False,indent=2),encoding='utf-8')
    raise SystemExit(0 if result.wasSuccessful() else 1)
