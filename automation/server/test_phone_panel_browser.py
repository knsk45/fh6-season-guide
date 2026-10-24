"""Real browser panel checks. Disposable local fixture, no accounts/publisher."""
import asyncio
import json
from pathlib import Path
import tempfile
import threading
import sys
from unittest.mock import patch
sys.path.insert(0,str(Path(__file__).parent))
from playwright.async_api import async_playwright,expect
import phone_ui as ui
import phone_tasks as tasks

async def main():
    class Fixture(ui.UI):
        def do_POST(self):
            # Only this disposable localhost origin simulates nginx TLS.
            if self.headers.get('Origin')=='http://'+self.headers.get('Host',''):
                self.headers.replace_header('Origin','https://'+self.headers['Host'])
            super().do_POST()
    with tempfile.TemporaryDirectory() as folder:
        root=Path(folder);(root/'reports').mkdir();(root/'inbox').mkdir();(root/'login').mkdir()
        (root/'automation/runs/refresh').mkdir(parents=True);(root/'data').mkdir()
        texts={'ru':'[h2]Русский текст[/h2]\nКод: 123 456 789','en':'[h2]English[/h2]\nCode: 123 456 789'}
        for lang,name in [('ru','steam-guide-current.txt'),('en','steam-guide-current-en.txt')]:
            (root/'reports'/name).write_text(texts[lang],encoding='utf-8')
        (root/'data/current-season.json').write_text(json.dumps({'lastContentUpdate':'2026-10-14T06:05:42+07:00','season':{'reportTitle':'Лето · Проверочная сводка'}}))
        (root/'automation/runs/refresh/active.json').write_text(json.dumps({'status':'PENDING_CONFIRMATION','steps':{'publish':{'status':'passed'}},'haReceipt':'CONFIRMED'}))
        (root/'login/status.json').write_text(json.dumps({'status':'CONNECTED'}))
        with patch.object(ui,'ROOT',root),patch.object(ui,'STORE',root),patch.object(tasks,'STORE',root),patch.object(tasks.os,'geteuid',return_value=1000):
            server=ui.ThreadingHTTPServer(('127.0.0.1',0),Fixture)
            thread=threading.Thread(target=server.serve_forever,daemon=True);thread.start()
            base='http://127.0.0.1:'+str(server.server_port)
            try:
                async with async_playwright() as pw:
                    browser=await pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True)
                    context=await browser.new_context(permissions=['clipboard-read','clipboard-write'])
                    page=await context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
                    for width,height in [(390,844),(1440,1000)]:
                        await page.set_viewport_size({'width':width,'height':height});await page.goto(base)
                        assert await page.locator('section.card').count()==5
                        assert not await page.evaluate('document.documentElement.scrollWidth>innerWidth')
                        assert await page.locator('#steam .steam-text:visible').count()==0
                        for lang in ['ru','en']:
                            button=page.locator('[data-copy="steam-'+lang+'"]');await button.click()
                            await expect(button).to_have_text('✓ Скопировано')
                            assert await page.evaluate('navigator.clipboard.readText()')==texts[lang]
                        assert await page.locator('#overview pre').count()==0
                        for section in await page.locator('section.card').all():
                            assert await section.evaluate('e=>getComputedStyle(e).borderStyle')=='solid'
                    await page.goto(base)
                    async def fail_copy(route):pass
                    await page.evaluate("Object.defineProperty(navigator,'clipboard',{configurable:true,value:{writeText:async()=>{throw Error('fixture')}}})")
                    await page.locator('[data-copy="steam-ru"]').click()
                    await expect(page.locator('#steam-ru')).to_be_visible()
                    await expect(page.locator('#steam')).to_contain_text('скопируйте вручную')
                    await page.goto(base)
                    await page.locator('#steam-consent').check()
                    await expect(page.locator('form[action="/consent"] .action-message')).to_contain_text('согласие включено')
                    await page.wait_for_timeout(1500)
                    assert json.loads((root/'steam-consent.json').read_text())['enabled'] is True
                    await expect(page.locator('#steam-consent')).to_be_checked()
                    await page.locator('#steam-consent').uncheck();await page.wait_for_timeout(1500)
                    assert json.loads((root/'steam-consent.json').read_text())['enabled'] is False
                    await page.locator('form[action="/approve"] button').click()
                    await expect(page.locator('form[action="/approve"] .action-message')).to_contain_text('Разрешение сохранено')
                    await page.wait_for_timeout(1500)
                    await expect(page.locator('#steam')).to_contain_text('Разрешение на эти два текста сохранено')
                    await page.locator('#task').fill('Проверочная задача')
                    await page.locator('form[action="/task"] button').click();await page.wait_for_timeout(1500)
                    await expect(page.locator('#tasks')).to_contain_text('В очереди')
                    await page.locator('form[action="/refresh"] button').click()
                    await expect(page.locator('form[action="/refresh"] .action-message')).to_contain_text('Запрос принят')
                    await page.wait_for_timeout(1500)
                    await expect(page.locator('#overview')).to_contain_text('Проверка поставлена в очередь')
                    (root/'refresh-request').unlink();await page.goto(base)
                    await page.route('**/refresh?*',lambda route:route.abort())
                    await page.locator('form[action="/refresh"] button').click()
                    await expect(page.get_by_role('button',name='Обновить статус')).to_be_visible()
                    await page.unroute('**/refresh?*');await page.goto(base)
                    await page.locator('#screens').set_input_files({'name':'fixture.png','mimeType':'image/png','buffer':b'\x89PNG\r\n\x1a\nfixture'})
                    await page.locator('#upload-button').click();await expect(page.locator('#message')).to_contain_text('Сохранено оригиналов: 1')
                    assert len(list((root/'inbox').glob('*.png')))==1
                    (root/'login/status.json').write_text(json.dumps({'status':'IDLE'}));await page.goto(base)
                    await page.locator('form[action="/login"] button').click()
                    await expect(page.locator('form[action="/login"] .action-message')).to_contain_text('Запрос входа принят')
                    assert not errors,errors
                    await browser.close()
            finally:server.shutdown();server.server_close();thread.join()
    print('PHONE_PANEL_BROWSER_OK mobile=390 desktop=1440; sections/copy/actions/errors/switch checked; no live task or publication')

if __name__=='__main__':asyncio.run(main())
