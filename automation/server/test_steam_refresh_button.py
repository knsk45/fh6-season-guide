"""Offline request tests: no browser, services, publication or credentials."""
import json,tempfile,threading,time,unittest,urllib.request,urllib.parse,urllib.error
from pathlib import Path
from unittest.mock import patch
import phone_ui as ui
import phone_view
import steam_publish
from test_phone_view import fixture


class Tests(unittest.TestCase):
    def setUp(self):
        self.tmp=tempfile.TemporaryDirectory();self.addCleanup(self.tmp.cleanup)
        self.root=Path(self.tmp.name);(self.root/'reports').mkdir()
        for name in ('steam-guide-current.txt','steam-guide-current-en.txt'):
            (self.root/'reports'/name).write_text('Fixture '+name)
        self.sha=steam_publish.combined(steam_publish.texts(self.root))
        for obj,key,value in ((ui,'ROOT',self.root),(ui,'STORE',self.root)):
            p=patch.object(obj,key,value);p.start();self.addCleanup(p.stop)
        p=patch('os.geteuid',return_value=1000);p.start();self.addCleanup(p.stop)
        self.server=ui.ThreadingHTTPServer(('127.0.0.1',0),ui.UI)
        self.thread=threading.Thread(target=self.server.serve_forever,daemon=True);self.thread.start()
        self.addCleanup(self.close)
        self.host='127.0.0.1:'+str(self.server.server_port)

    def close(self):
        self.server.shutdown();self.server.server_close();self.thread.join()

    def post(self,sha=None,origin=None):
        fields={'sha':sha or self.sha,'_csrf':ui.CSRF_TOKEN}
        req=urllib.request.Request('http://'+self.host+'/steam-refresh?_ui=1',
            data=urllib.parse.urlencode(fields).encode(),
            headers={'Origin':origin or 'https://'+self.host,'X-FH6-UI':'1'})
        return json.load(urllib.request.urlopen(req))

    def consent(self):
        (self.root/'steam-consent.json').write_text(json.dumps({'enabled':True,'updatedAt':time.time()}))

    def test_no_consent_cannot_queue(self):
        with self.assertRaises(urllib.error.HTTPError) as e:self.post()
        self.assertEqual(e.exception.code,409)
        self.assertFalse((self.root/'steam-publish-request').exists())

    def test_current_pair_queues_only_existing_publisher(self):
        self.consent()
        status=json.dumps({'status':'BLOCKED','sections':{'en':'SUBMITTING'}})
        (self.root/'steam-status.json').write_text(status)
        self.assertEqual(self.post()['anchor'],'steam')
        row=json.loads((self.root/'steam-publish-request').read_text())
        self.assertEqual(row['sha256'],self.sha)
        self.assertFalse((self.root/'refresh-request').exists())
        self.assertEqual((self.root/'steam-status.json').read_text(),status)
        with self.assertRaises(urllib.error.HTTPError) as e:self.post()
        self.assertEqual(e.exception.code,409)

    def test_changed_pair_is_rejected(self):
        self.consent()
        with self.assertRaises(urllib.error.HTTPError) as e:self.post('0'*64)
        self.assertEqual(e.exception.code,409)
        self.assertFalse((self.root/'steam-publish-request').exists())

    def test_hostile_origin_is_rejected_even_with_nonce(self):
        self.consent()
        with self.assertRaises(urllib.error.HTTPError) as e:self.post(origin='https://evil.example')
        self.assertEqual(e.exception.code,403)
        self.assertFalse((self.root/'steam-publish-request').exists())

    def test_valid_one_time_approval_allows_request(self):
        (self.root/'steam-approval-fixture.json').write_text(json.dumps(dict(
            action='replace-current-ru-en',sha256=self.sha,approvedAt=time.time(),
            status='AWAITING_BROWSER_PUBLICATION')))
        self.post();self.assertTrue((self.root/'steam-publish-request').exists())

    def test_symlink_request_is_rejected(self):
        self.consent();outside=self.root/'unrelated';outside.write_text('unchanged')
        (self.root/'steam-publish-request').symlink_to(outside)
        with self.assertRaises(urllib.error.HTTPError):self.post()
        self.assertEqual(outside.read_text(),'unchanged')

    def test_button_has_hash_and_requires_permission(self):
        data=fixture();body=phone_view.render(**data)
        self.assertNotIn('action="/steam-refresh"',body)
        data['consent']={'enabled':True}
        data['steam_publication']={'requestedAt':time.time(),'updatedAt':0}
        body=phone_view.render(**data)
        self.assertIn('action="/steam-refresh"',body)
        self.assertIn('Обновить тексты Steam',body)
        self.assertIn('Запрос Steam принят',body)
        self.assertIn('name="sha" value="'+'a'*64+'"',body)

    def test_path_unit_can_only_activate_steam_service(self):
        unit=(Path(__file__).parent/'fh6-steam-request.path').read_text()
        self.assertIn('PathChanged=/var/lib/fh6/steam-publish-request',unit)
        self.assertIn('Unit=fh6-steam.service',unit)
        self.assertNotIn('fh6-manual',unit)


if __name__=='__main__':unittest.main()
