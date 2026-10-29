import copy
import hashlib
import json
import sys
import tempfile
import unittest
from pathlib import Path
sys.path.insert(0,str(Path(__file__).resolve().parents[1]/'skill/scripts'))
from check_visuals import evaluate
from audio_mix import placement
from check_review import evaluate as review

class DirectorTests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory(); self.base=Path(self.tmp.name)
        (self.base/'a.mp4').write_bytes(b'fixture'); (self.base/'evidence.txt').write_text('fixture')
        self.m={'schema_version':2,'assets':[{'id':'a','kind':'video','local_original':'a.mp4','sha256':hashlib.sha256(b'fixture').hexdigest()}], 'segments':[{'id':'s1','asset_id':'a','source_asset_id':'a','source_shot_id':'shot1','source_range':[10,14]}, {'id':'s2','asset_id':'a','source_asset_id':'a','source_shot_id':'shot2','source_range':[80,84]}], 'uses':[{'id':'u1','segment_id':'s1','output':[0,4]},{'id':'u2','segment_id':'s2','output':[4,8]}], 'coverage':{'final_timeline_checked':True,'nested_media_checked':True,'visual_comparison_complete':True,'evidence':'evidence.txt'}}
    def tearDown(self): self.tmp.cleanup()
    def test_distinct_same_file_not_failed(self): self.assertFalse(evaluate(self.m,self.base)['failures'])
    def test_same_shot_disjoint_span_fails(self):
        self.m['segments'][1]['source_shot_id']='shot1'; self.assertTrue(evaluate(self.m,self.base)['failures'])
    def test_partial_source_overlap(self):
        self.m['segments'][1]['source_range']=[13,17]; self.assertTrue(evaluate(self.m,self.base)['failures'])
    def test_crop_mirror_speed_cannot_launder(self):
        for transform in ('crop','mirror','reencode','speed'):
            m=copy.deepcopy(self.m);m['uses'][1].update(segment_id='s1',transform=transform,speed=2,output=[4,6]);self.assertTrue(evaluate(m,self.base)['failures'])
    def test_fake_derivative_identity_rejected(self):
        self.m['segments'][1]['derived_from']='s1';self.assertEqual(evaluate(self.m,self.base)['status'],'INVALID')
    def test_continuous_once_allowed(self):
        self.m['uses']=self.m['uses'][:1]; self.assertFalse(evaluate(self.m,self.base)['failures'])
    def test_loop_fails(self):
        self.m['uses'][0]['loop']=True;self.assertTrue(evaluate(self.m,self.base)['failures'])
    def test_no_sample_no_pass(self): self.assertEqual(evaluate(self.m,self.base)['status'],'UNVERIFIED')
    def test_hash_change_rejected(self):
        (self.base/'a.mp4').write_bytes(b'changed');self.assertEqual(evaluate(self.m,self.base)['status'],'INVALID')
    def test_transient_compensation(self):
        self.assertEqual(placement({'source_range':[1,2],'transient_offset':1.2,'anchor_seconds':3},30),(1,2,2.8))
    def test_tail_not_silently_cut(self):
        with self.assertRaises(ValueError): placement({'source_range':[0,2],'anchor_seconds':29},30)
    def test_legacy_review_gate_required(self):
        r=json.loads((Path(__file__).resolve().parents[1]/'skill/assets/review.example.json').read_text(encoding='utf-8')); r['gates'].pop('visual_uniqueness',None)
        self.assertIn('gate:visual_uniqueness',review(r,self.base)['unverified'])

if __name__=='__main__': unittest.main()
