import sys
from pathlib import Path
sys.path.insert(0,str(Path(__file__).parent))
import tempfile,json,unittest
from unittest.mock import patch
import steam_consent as consent

class Tests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.base=Path(self.tmp.name)
        self.root=self.base/'repo';self.store=self.base/'store';self.store.mkdir()
        (self.root/'reports').mkdir(parents=True);(self.root/'automation/runs/refresh').mkdir(parents=True)
        self.active=self.root/'automation/runs/refresh/active.json'
        self.active.write_text(json.dumps({'status':'PENDING_CONFIRMATION'}))
        for name in ['steam-guide-current.txt','steam-guide-current-en.txt']:(self.root/'reports'/name).write_text('Approved text')
        self.uid=patch.object(consent.os,'geteuid',return_value=1000);self.uid.start()
    def tearDown(self):self.uid.stop();self.tmp.cleanup()
    def approvals(self):return [json.loads(f.read_text()) for f in self.store.glob('steam-approval-*.json')]
    def test_off_default_and_dedup_when_on(self):
        consent.sync(self.root,self.store);self.assertEqual(self.approvals(),[])
        consent.set_enabled(self.store,True);consent.sync(self.root,self.store);consent.sync(self.root,self.store)
        self.assertEqual(len(self.approvals()),1);self.assertTrue(self.approvals()[0]['automatic'])
    def test_new_pair_gets_approval(self):
        consent.set_enabled(self.store,True);consent.sync(self.root,self.store)
        (self.root/'reports/steam-guide-current-en.txt').write_text('New English')
        consent.sync(self.root,self.store)
        self.assertEqual(len(self.approvals()),2);self.assertNotEqual(*[a['sha256'] for a in self.approvals()])
    def test_disabled_revokes_auto_only(self):
        consent.set_enabled(self.store,True);consent.sync(self.root,self.store)
        (self.store/'steam-approval-manual.json').write_text(json.dumps({'automatic':False,'status':'AWAITING_BROWSER_PUBLICATION'}))
        consent.set_enabled(self.store,False);consent.sync(self.root,self.store)
        values=self.approvals();self.assertEqual(next(v for v in values if v['automatic'])['status'],'REVOKED')
        self.assertEqual(next(v for v in values if not v['automatic'])['status'],'AWAITING_BROWSER_PUBLICATION')
    def test_blocked_or_invalid_text_not_approved(self):
        consent.set_enabled(self.store,True);self.active.write_text(json.dumps({'status':'BLOCKED'}))
        consent.sync(self.root,self.store);self.assertEqual(self.approvals(),[])
        self.active.write_text(json.dumps({'status':'PENDING_CONFIRMATION'}))
        (self.root/'reports/steam-guide-current-en.txt').write_text('x'*4801)
        consent.sync(self.root,self.store);self.assertEqual(self.approvals(),[])

    def test_expired_approval_is_renewed_without_duplicates(self):
        consent.set_enabled(self.store,True);consent.sync(self.root,self.store)
        file=next(self.store.glob('steam-approval-*.json'));value=json.loads(file.read_text());value['approvedAt']=0;file.write_text(json.dumps(value))
        consent.sync(self.root,self.store);consent.sync(self.root,self.store)
        self.assertEqual(len(self.approvals()),2)

if __name__=='__main__':unittest.main()
