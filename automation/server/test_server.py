import importlib.util
from pathlib import Path
import unittest
from unittest.mock import patch
import tempfile
import hashlib
import json
import time
import os
import subprocess
import threading
import urllib.request
import urllib.error
from urllib.parse import urlencode

def module(name):
    spec=importlib.util.spec_from_file_location(name,Path(__file__).with_name(name+'.py'))
    result=importlib.util.module_from_spec(spec);spec.loader.exec_module(result);return result

ui=module('phone_ui')
password=module('phone_password')

class Tests(unittest.TestCase):
    def test_only_image_upload_types(self):
        self.assertEqual(ui.mime(b'\x89PNG\r\n\x1a\nfixture'),'.png')
        self.assertEqual(ui.mime(b'\xff\xd8\xfffixture'),'.jpg')
        with self.assertRaises(ValueError):ui.mime(b'<script>evil</script>')
    def test_approval_binds_both_locales(self):
        self.assertNotEqual(ui.fingerprint('ru\nen'),ui.fingerprint('ru\nchanged'))

class PasswordTests(unittest.TestCase):
    token='a'*43
    hashed='$6$salt$'+'b'*86
    def pending(self):
        return dict(status='pending',expiresAt=time.time()+60,
                    tokenSha256=hashlib.sha256(self.token.encode()).hexdigest())
    def test_invitation_token_required(self):
        for token in ['',None,'a'*42,'../'+self.token,'b'*43]:
            self.assertFalse(password.valid_invitation(self.pending(),token))
        self.assertTrue(password.valid_invitation(self.pending(),self.token))
    def test_expired_and_consumed_invitations(self):
        state=self.pending();state['expiresAt']=0
        self.assertFalse(password.valid_invitation(state,self.token))
        for status in ['complete','applying']:
            state=self.pending();state['status']=status
            self.assertFalse(password.valid_invitation(state,self.token))
    def test_invalid_hash_does_not_change_credentials(self):
        with patch.object(password,'read_state',return_value=self.pending()),patch.object(password,'atomic') as write:
            for hashed in ['plaintext','!','$6$bad\nkns:other',self.hashed+'\n']:
                self.assertFalse(password.apply(dict(token=self.token,hash=hashed))['ok'])
            write.assert_not_called()
    def test_success_and_replay(self):
        state=self.pending();writes=[]
        def record(file,content,group,mode):
            writes.append((file.name,content,group,mode))
            if file.name=='phone-first-login.json':
                state.clear();state.update(json.loads(content))
        with patch.object(password,'read_state',side_effect=lambda:state.copy()),patch.object(password,'atomic',side_effect=record):
            self.assertTrue(password.apply(dict(token=self.token,hash=self.hashed))['ok'])
            self.assertFalse(password.apply(dict(token=self.token,hash=self.hashed))['ok'])
        self.assertEqual(len(writes),3)
        self.assertEqual(writes[1][1],'knsk45:'+self.hashed+'\n')
        self.assertNotIn(self.token,json.dumps(writes))
        self.assertNotIn('tokenSha256',state)
    def test_interrupted_write_fails_closed(self):
        state=self.pending()
        def interrupted(file,content,group,mode):
            if file.name=='phone-first-login.json':
                state.clear();state.update(json.loads(content))
            else:raise OSError('test failure')
        with patch.object(password,'read_state',side_effect=lambda:state.copy()),patch.object(password,'atomic',side_effect=interrupted):
            with self.assertRaises(OSError):password.apply(dict(token=self.token,hash=self.hashed))
        self.assertFalse(password.valid_invitation(state,self.token))
    def test_password_validation(self):
        with patch.object(ui.subprocess,'run') as run:
            for value,confirm in [('', ''),('a','b'),('a\n','a\n'),('a\0','a\0')]:
                with self.assertRaises(ValueError):ui.password_hash(value,confirm)
            run.assert_not_called()
    def test_no_password_length_or_complexity_policy(self):
        with patch.object(ui.subprocess,'run') as run:
            run.return_value.stdout=self.hashed+'\n'
            for value in ['a','123','a'*129,'тест']:
                self.assertEqual(ui.password_hash(value,value),self.hashed)
    def test_password_hash_uses_stdin_not_arguments(self):
        with patch.object(ui.subprocess,'run') as run:
            run.return_value.stdout=self.hashed+'\n'
            self.assertEqual(ui.password_hash('test-only-pass-123','test-only-pass-123'),self.hashed)
            self.assertNotIn('test-only-pass-123',str(run.call_args.args))

class SetupHttpTests(unittest.TestCase):
    def setUp(self):
        self.folder=tempfile.TemporaryDirectory()
        self.file=Path(self.folder.name)/'first.json'
        self.token='a'*43
        self.file.write_text(json.dumps(dict(status='pending',expiresAt=time.time()+60,
                              tokenSha256=ui.fingerprint(self.token))))
        self.patcher=patch.object(ui,'FIRST_LOGIN',self.file);self.patcher.start()
        self.server=ui.ThreadingHTTPServer(('127.0.0.1',0),ui.UI)
        self.thread=threading.Thread(target=self.server.serve_forever,daemon=True);self.thread.start()
        self.base='http://127.0.0.1:'+str(self.server.server_port)
    def tearDown(self):
        self.server.shutdown();self.server.server_close();self.thread.join()
        self.patcher.stop();self.folder.cleanup()
    def get(self,path):
        try:
            with urllib.request.urlopen(self.base+path) as response:return response.status,response.read(),response.headers
        except urllib.error.HTTPError as error:return error.code,error.read(),error.headers
    def post(self,fields,origin=None):
        headers={'Content-Type':'application/x-www-form-urlencoded',
                 'Origin':origin or 'https://127.0.0.1:'+str(self.server.server_port)}
        request=urllib.request.Request(self.base+'/setup',data=urlencode(fields).encode(),headers=headers,method='POST')
        try:
            with urllib.request.urlopen(request) as response:return response.status,response.read()
        except urllib.error.HTTPError as error:return error.code,error.read()
    def test_form_is_not_public(self):
        self.assertEqual(self.get('/setup')[0],404)
        self.assertEqual(self.get('/setup?key='+'b'*43)[0],404)
    def test_valid_form_and_security_headers(self):
        status,body,headers=self.get('/setup?key='+self.token)
        self.assertEqual(status,200);self.assertIn(b'knsk45',body)
        self.assertNotIn(b'minlength',body);self.assertNotIn(b'maxlength',body)
        self.assertEqual(headers['Cache-Control'],'no-store')
        self.assertEqual(headers['Referrer-Policy'],'strict-origin')
        self.assertEqual(headers['X-Frame-Options'],'DENY')
    def test_cross_origin_is_rejected(self):
        fields=dict(key=self.token,password='test-only-pass-123',confirmation='test-only-pass-123')
        self.assertEqual(self.post(fields,'https://untrusted.invalid')[0],403)
    def test_password_is_not_echoed_or_written(self):
        fields=dict(key=self.token,password='test-only-pass-123',confirmation='test-only-pass-123')
        with patch.object(ui,'password_hash',return_value=PasswordTests.hashed),patch.object(ui,'set_password',return_value=dict(ok=True)) as broker:
            status,body=self.post(fields)
        self.assertEqual(status,200);self.assertNotIn(b'test-only-pass-123',body)
        broker.assert_called_once_with(self.token,PasswordTests.hashed)
    def test_confirmation_and_size_rejected_before_broker(self):
        with patch.object(ui,'set_password') as broker:
            self.assertEqual(self.post(dict(key=self.token,password='test-only-pass-123',confirmation='different'))[0],400)
            self.assertEqual(self.post(dict(key=self.token,password='x'*5000,confirmation='x'*5000))[0],413)
            broker.assert_not_called()

@unittest.skipUnless(os.name=='posix' and getattr(os,'geteuid',lambda:1)()==0,
                     'Root Linux storage test')
class RootStorageTests(unittest.TestCase):
    def test_real_hash_and_atomic_credentials(self):
        import grp
        token='a'*43
        with tempfile.TemporaryDirectory() as folder,patch.object(password,'ETC',Path(folder)):
            state=dict(status='pending',expiresAt=time.time()+60,tokenSha256=ui.fingerprint(token))
            password.atomic(Path(folder)/'phone-first-login.json',json.dumps(state),'fh6',0o640)
            hashed=ui.password_hash('a','a')
            self.assertTrue(password.apply(dict(token=token,hash=hashed))['ok'])
            actual=Path(folder)/'phone.htpasswd'
            self.assertEqual(actual.read_text(),'knsk45:'+hashed+'\n')
            self.assertEqual(actual.stat().st_uid,0)
            self.assertEqual(actual.stat().st_gid,grp.getgrnam('www-data').gr_gid)
            self.assertEqual(actual.stat().st_mode & 0o777,0o640)
            self.assertNotEqual(subprocess.run(['runuser','-u','www-data','--','test','-r',str(actual)]).returncode,0)
            subprocess.run(['setfacl','-m','u:www-data:--x',folder],check=True)
            self.assertEqual(subprocess.run(['runuser','-u','www-data','--','test','-r',str(actual)]).returncode,0)
            self.assertNotEqual(subprocess.run(['runuser','-u','www-data','--','test','-r',str(Path(folder)/'phone-first-login.json')]).returncode,0)
            self.assertFalse(password.apply(dict(token=token,hash=hashed))['ok'])
            self.assertFalse(any('test-only-pass-123' in file.read_text() for file in Path(folder).iterdir()))

if __name__=='__main__':unittest.main()
