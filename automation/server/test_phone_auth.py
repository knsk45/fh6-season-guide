"""Disposable credentials and HTTP server; never reads production auth or publishes."""
import hashlib
from http import cookies
import http.client
from pathlib import Path
import re
import subprocess
import tempfile
import threading
import unittest
from unittest.mock import patch
from urllib.parse import urlencode
import phone_auth as auth


def make_hash(password, salt='testSalt'):
    return subprocess.run(['openssl','passwd','-6','-salt',salt,'-stdin'],
                          input=password+'\n',text=True,capture_output=True,check=True).stdout.strip()


class Tests(unittest.TestCase):
    def setUp(self):
        self.temp=tempfile.TemporaryDirectory()
        self.path=Path(self.temp.name)/'htpasswd'
        self.password='only-a-disposable-test-password'
        self.path.write_text('knsk45:'+make_hash(self.password)+'\n')
        self.now=100000
        self.state=auth.State(self.path, {'192.168.1.55:8443','fh6.knsk45.crazedns.ru'},clock=lambda:self.now)
        self.server=auth.Server(('127.0.0.1',0),self.state)
        self.thread=threading.Thread(target=self.server.serve_forever,daemon=True)
        self.thread.start()

    def tearDown(self):
        self.server.shutdown();self.server.server_close();self.thread.join();self.temp.cleanup()

    def request(self,path,fields=None,cookie='',origin='https://192.168.1.55:8443',host='192.168.1.55:8443',extra=None):
        connection=http.client.HTTPConnection('127.0.0.1',self.server.server_port,timeout=5)
        headers={'Host':host,'Cookie':cookie,'Origin':origin,'X-Real-IP':'192.0.2.1'}
        headers.update(extra or {})
        body=None if fields is None else urlencode(fields,doseq=True)
        if body is not None:headers['Content-Type']='application/x-www-form-urlencoded'
        connection.request('GET' if fields is None else 'POST',path,body,headers)
        response=connection.getresponse();data=response.read().decode();items=response.getheaders()
        status=response.status;connection.close()
        return status,items,data

    def form(self):
        status,headers,body=self.request('/signin')
        self.assertEqual(status,200)
        value=re.search(r'name="csrf" value="([^"]+)"',body).group(1)
        header=next(v for k,v in headers if k.lower()=='set-cookie')
        return header.split(';')[0],value

    def login(self,password=None,username='knsk45'):
        cookie,csrf=self.form()
        return self.request('/signin',{'username':username,'password':self.password if password is None else password,'csrf':csrf},cookie)

    def session_cookie(self):
        status,headers,_=self.login();self.assertEqual(status,303)
        return next(v for k,v in headers if k.lower()=='set-cookie' and v.startswith(auth.SESSION+'=')).split(';')[0]

    def test_public_form_no_basic_challenge_or_secret(self):
        status,headers,body=self.request('/signin')
        self.assertEqual(status,200);self.assertIn('Вход в панель',body)
        self.assertNotIn('www-authenticate',dict((k.lower(),v) for k,v in headers))
        self.assertNotIn(self.password,body);self.assertNotIn(self.path.read_text(),body)
        self.assertIn('autocomplete="current-password"',body)
        self.assertIn('name="csrf"',body)

    def test_anonymous_and_forged_cookies_denied(self):
        for cookie in ('',auth.SESSION+'=fake',auth.SESSION+'='+'a'*43):
            self.assertEqual(self.request('/_auth',cookie=cookie)[0],401)

    def test_success_secure_cookie_and_session(self):
        status,headers,_=self.login();self.assertEqual(status,303)
        self.assertEqual(dict(headers)['Location'],'/')
        cookie=next(v for k,v in headers if k=='Set-Cookie' and v.startswith(auth.SESSION+'='))
        for flag in ('Secure','HttpOnly','SameSite=Lax','Path=/','Max-Age=28800'):self.assertIn(flag,cookie)
        self.assertEqual(self.request('/_auth',cookie=cookie.split(';')[0])[0],204)
        self.assertEqual(self.request('/signin',cookie=cookie.split(';')[0])[0],303)

    def test_bad_password_does_not_issue_session(self):
        status,headers,body=self.login(password='wrong')
        self.assertEqual(status,401);self.assertIn('Неверный логин или пароль',body)
        self.assertFalse(any(v.startswith(auth.SESSION+'=') for k,v in headers if k=='Set-Cookie'))
        self.assertEqual(len(self.state.sessions),0)

    def test_username_cannot_be_substituted(self):
        self.assertEqual(self.login(username='attacker')[0],401)

    def test_csrf_missing_wrong_replayed_and_foreign_origin(self):
        cookie,token=self.form()
        fields={'username':'knsk45','password':self.password,'csrf':token}
        self.assertEqual(self.request('/signin',fields,cookie,origin='https://evil.example')[0],403)
        self.assertEqual(self.request('/signin',fields,cookie,origin='null')[0],403)
        self.assertEqual(self.request('/signin',fields,'')[0],403)
        self.assertEqual(self.request('/signin',dict(fields,csrf='wrong'),cookie)[0],403)
        self.assertEqual(self.request('/signin',fields,cookie)[0],303)
        self.assertEqual(self.request('/signin',fields,cookie)[0],403)

    def test_configured_public_origin_survives_proxy_host_change(self):
        cookie,token=self.form()
        fields={'username':'knsk45','password':self.password,'csrf':token}
        self.assertEqual(self.request('/signin',fields,cookie,origin='https://fh6.knsk45.crazedns.ru')[0],303)

    def test_expired_form(self):
        cookie,token=self.form();self.now+=601
        self.assertEqual(self.request('/signin',{'username':'knsk45','password':self.password,'csrf':token},cookie)[0],403)

    def test_idle_and_absolute_session_expiration(self):
        cookie=self.session_cookie();self.now+=3601
        self.assertEqual(self.request('/_auth',cookie=cookie)[0],401)
        cookie=self.session_cookie()
        for _ in range(8):
            self.now+=3500;self.assertEqual(self.request('/_auth',cookie=cookie)[0],204)
        self.now+=900;self.assertEqual(self.request('/_auth',cookie=cookie)[0],401)

    def test_password_change_revokes_existing_sessions(self):
        cookie=self.session_cookie()
        self.path.write_text('knsk45:'+make_hash('replacement-disposable-password')+'\n')
        self.assertEqual(self.request('/_auth',cookie=cookie)[0],401)

    def test_logout_requires_csrf_and_revokes_session(self):
        cookie=self.session_cookie()
        status,_,body=self.request('/signout',cookie=cookie);self.assertEqual(status,200)
        self.assertEqual(self.request('/signout',{'csrf':'wrong'},cookie)[0],403)
        self.assertEqual(self.request('/_auth',cookie=cookie)[0],204)
        token=re.search(r'name="csrf" value="([^"]+)"',body).group(1)
        status,headers,_=self.request('/signout',{'csrf':token},cookie)
        self.assertEqual(status,303);self.assertEqual(self.request('/_auth',cookie=cookie)[0],401)
        self.assertTrue(any('Max-Age=0' in v for k,v in headers if k=='Set-Cookie'))

    def test_rate_limit_and_recovery(self):
        for _ in range(5):self.assertEqual(self.login(password='wrong')[0],401)
        self.assertEqual(self.login()[0],429)
        self.now+=901;self.assertEqual(self.login()[0],303)

    def test_bad_host_duplicates_oversize_and_cookie_parser(self):
        self.assertEqual(self.request('/signin',host='evil.example')[0],400)
        cookie,token=self.form()
        self.assertEqual(self.request('/signin',{'username':['knsk45','evil'],'password':self.password,'csrf':token},cookie)[0],400)
        self.assertEqual(self.request('/signin',{'password':'a'*5000},cookie)[0],413)

    def test_missing_or_unsupported_credentials_fail_closed(self):
        self.path.write_text('knsk45:not-a-supported-hash\n')
        self.assertEqual(self.login()[0],503)
        self.assertEqual(len(self.state.sessions),0)

    def test_nonce_and_session_storage_bounded(self):
        with self.state.lock:
            self.state.nonces={str(i):self.now+600 for i in range(1024)}
        self.assertIsNone(self.state.nonce())
        self.now+=601;self.assertIsNotNone(self.state.nonce())
        revision=self.state.credentials()[2]
        for _ in range(256):self.assertIsNotNone(self.state.create_session(revision))
        self.assertIsNone(self.state.create_session(revision))


if __name__=='__main__':unittest.main()
