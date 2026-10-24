"""Browser QA on a disposable localhost fixture, no real account or protected origin."""
import asyncio
from pathlib import Path
import tempfile
import threading
from urllib.parse import urlsplit
from playwright.async_api import async_playwright, expect
import phone_auth as auth
from test_phone_auth import make_hash


class Fixture(auth.Handler):
    def do_POST(self):
        # Only this isolated HTTP localhost test translates its own form origin.
        expected='http://'+self.headers.get('Host','')
        if self.headers.get('Origin')==expected:
            self.headers.replace_header('Origin','https://'+self.headers['Host'])
        super().do_POST()

    def do_GET(self):
        if urlsplit(self.path).path=='/':
            if self.server.auth.session(self.cookie(auth.SESSION)):
                return self.send(200,self.page('Проверочная панель','<a href="/signout">Выйти</a>'))
            return self.send(303,location='/signin')
        super().do_GET()


async def main():
    with tempfile.TemporaryDirectory() as directory:
        credential=Path(directory)/'passwd'
        credential.write_text('knsk45:'+make_hash('disposable-browser-fixture')+'\n')
        state=auth.State(credential,set())
        server=auth.Server(('127.0.0.1',0),state)
        server.RequestHandlerClass=Fixture
        host='localhost:'+str(server.server_port);state.hosts=frozenset({host})
        thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
        base='http://'+host
        out=Path(__file__).parent/'auth-browser-results';out.mkdir(exist_ok=True)
        try:
            async with async_playwright() as pw:
                browser=await pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True)
                context=await browser.new_context()
                page=await context.new_page();errors=[]
                page.on('pageerror',lambda error:errors.append(str(error)))
                for width,height in ((320,740),(390,844),(1440,1000)):
                    await page.set_viewport_size({'width':width,'height':height})
                    await page.goto(base)
                    await expect(page.get_by_role('heading',name='Вход в панель')).to_be_visible()
                    assert not await page.evaluate('document.documentElement.scrollWidth>innerWidth')
                    assert await page.locator('#password').get_attribute('autocomplete')=='current-password'
                    if width in (390,1440):await page.screenshot(path=str(out/f'login-{width}.png'),full_page=True)
                await page.locator('#password').fill('wrong-fixture-password')
                await page.get_by_role('button',name='Войти в панель').click()
                await expect(page.get_by_role('alert')).to_have_text('Неверный логин или пароль.')
                await page.locator('#password').fill('disposable-browser-fixture')
                await page.get_by_role('button',name='Войти в панель').click()
                await expect(page.get_by_role('heading',name='Проверочная панель')).to_be_visible()
                cookies=await context.cookies()
                session=next(row for row in cookies if row['name']==auth.SESSION)
                assert session['secure'] and session['httpOnly'] and session['sameSite']=='Lax'
                await page.reload();await expect(page.get_by_role('heading',name='Проверочная панель')).to_be_visible()
                await page.get_by_role('link',name='Выйти').click()
                await page.get_by_role('button',name='Выйти',exact=True).click()
                await expect(page.get_by_role('heading',name='Вход в панель')).to_be_visible()
                assert not errors,errors
                await browser.close()
        finally:server.shutdown();server.server_close();thread.join()
    print('PHONE_AUTH_BROWSER_OK widths=320,390,1440; invalid/correct synthetic login, reload, secure cookie, logout')


if __name__=='__main__':asyncio.run(main())
