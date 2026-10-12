"""Browser regression with disposable fixtures only; never owner credentials.

The localhost HTTP fixture simulates nginx TLS termination by normalizing only
its exact same-origin header to https. Null and foreign origins stay rejected.
"""
import asyncio
import importlib.util
import json
from pathlib import Path
import tempfile
import threading
import time
from unittest.mock import patch
from playwright.async_api import async_playwright


def module(name):
    spec=importlib.util.spec_from_file_location(name,Path(__file__).with_name(name+'.py'))
    result=importlib.util.module_from_spec(spec);spec.loader.exec_module(result);return result


ui=module('phone_ui')
password=module('phone_password')


async def main():
    token='a'*43  # public fixture, not a real invitation
    origins=[]
    class Fixture(ui.UI):
        def do_POST(self):
            origin=self.headers.get('Origin')
            origins.append(origin)
            if origin=='http://'+self.headers.get('Host',''):
                self.headers.replace_header('Origin','https://'+self.headers['Host'])
            super().do_POST()
    with tempfile.TemporaryDirectory() as folder:
        root=Path(folder)
        first=root/'phone-first-login.json'
        first.write_text(json.dumps(dict(status='pending',expiresAt=time.time()+60,
                                         tokenSha256=ui.fingerprint(token))))
        reports=root/'reports';reports.mkdir()
        for name in ['steam-guide-current.txt','steam-guide-current-en.txt']:
            (reports/name).write_text('Browser fixture',encoding='utf-8')
        def fixture_atomic(file,content,group,mode):
            file.write_text(content)
        with patch.object(ui,'FIRST_LOGIN',first),patch.object(password,'ETC',root),\
             patch.object(ui,'STORE',root),patch.object(ui,'ROOT',root),\
             patch.object(password,'atomic',side_effect=fixture_atomic),\
             patch.object(ui,'set_password',side_effect=lambda key,hashed:password.apply(dict(token=key,hash=hashed))):
            server=ui.ThreadingHTTPServer(('127.0.0.1',0),Fixture)
            thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
            base='http://127.0.0.1:'+str(server.server_port)
            try:
                async with async_playwright() as pw:
                    browser=await pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True)
                    page=await browser.new_page(viewport={'width':390,'height':844})
                    await page.goto(base+'/setup?key='+token)
                    assert await page.locator('input[name=password]').get_attribute('minlength') is None
                    await page.locator('input[name=password]').fill('a')
                    await page.locator('input[name=confirmation]').fill('a')
                    async with page.expect_navigation() as navigation:
                        await page.locator('button').click()
                    response=await navigation.value
                    assert response.status==200
                    assert 'Пароль установлен.' in await page.locator('body').inner_text()
                    assert origins==[base], 'Browser origin must survive form submission'
                    assert json.loads(first.read_text())['status']=='complete'
                    assert (root/'phone.htpasswd').read_text().startswith('knsk45:$6$')
                    replay=await page.goto(base+'/setup?key='+token)
                    assert replay.status==404
                    # Real button-only forms must not be rejected as empty uploads.
                    for path,name in [('/login','login-request'),('/refresh','refresh-request')]:
                        await page.goto(base+'/')
                        async with page.expect_navigation() as navigation:
                            await page.locator('form[action="'+path+'"] button').click()
                        response=await navigation.value
                        assert response.status==200
                        assert (root/name).is_file()
                        if path=='/login':
                            assert page.url==base+'/#codex'
                            assert 'Запрос принят' in await page.locator('#codex-status').inner_text()
                            await page.reload()  # Must be GET, never repost /login.
                            assert origins==[base,base]
                            login=root/'login';login.mkdir()
                            (login/'status.json').write_text(json.dumps(dict(status='CONNECTED',startedAt=time.time(),updatedAt=time.time())))
                            await page.locator('#codex-status').filter(has_text='Codex подключён').wait_for()
                            assert await page.locator('form[action="/login"]').count()==0
                    assert origins==[base,base,base]
                    await browser.close()
            finally:
                server.shutdown();server.server_close();thread.join()
    print('PHONE_BROWSER_FORM=PASSED SHORT_PASSWORD=PASSED INVITATION_REPLAY=REJECTED')
    print('PHONE_BROWSER_LOGIN=PASSED PHONE_BROWSER_REFRESH=PASSED LOGIN_AUTO_STATUS=PASSED')


if __name__=='__main__':asyncio.run(main())
