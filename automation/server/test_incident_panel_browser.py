"""Offline mobile/desktop clipboard QA; disposable panel, no real tasks/model."""
import asyncio,json,tempfile,threading
from pathlib import Path
from unittest.mock import patch
from playwright.async_api import async_playwright,expect
import phone_ui as ui
import phone_tasks as tasks
import refresh_receipts

async def main():
    class Fixture(ui.UI):
        def do_POST(self):
            if self.headers.get('Origin')=='http://'+self.headers.get('Host',''):
                self.headers.replace_header('Origin','https://'+self.headers['Host'])
            super().do_POST()
    with tempfile.TemporaryDirectory(prefix='fh6-incident-browser-') as d:
        root=Path(d)
        for name in ('reports','inbox','login','data'): (root/name).mkdir()
        for name in ('steam-guide-current.txt','steam-guide-current-en.txt'):(root/'reports'/name).write_text('Fixture')
        (root/'data/current-season.json').write_text(json.dumps({'lastContentUpdate':'2026-10-16T16:22:00+07:00','season':{'reportTitle':'Browser fixture'}}))
        (root/'login/status.json').write_text('{"status":"CONNECTED"}')
        run_id='fh6-20261016-162200-123456'
        run={'runId':run_id,'status':'BLOCKED','startedAt':'2026-10-16T16:22:00+07:00','finishedAt':'2026-10-16T16:23:00+07:00',
             'steps':{'audit':{'status':'passed'},'publish':{'status':'failed','exitCode':1}}}
        base=root/'automation/runs/refresh'/run_id;base.mkdir(parents=True)
        (base/'run.json').write_text(json.dumps(run))
        (base/'publish.log').write_text('Local branch does not contain origin/daily-season. SECRET_FIXTURE')
        (base.parent/'active.json').write_text(json.dumps(run))
        with patch.object(ui,'ROOT',root),patch.object(ui,'STORE',root),patch.object(tasks,'STORE',root),patch('os.geteuid',return_value=1000):
            refresh_receipts.accept(root);refresh_receipts.bind(root,run_id)
            server=ui.ThreadingHTTPServer(('127.0.0.1',0),Fixture)
            worker=threading.Thread(target=server.serve_forever,daemon=True);worker.start()
            try:
                async with async_playwright() as pw:
                    browser=await pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True,chromium_sandbox=True)
                    context=await browser.new_context(permissions=['clipboard-read','clipboard-write'])
                    page=await context.new_page();errors=[];page.on('pageerror',lambda e:errors.append(str(e)))
                    for width,height in ((390,844),(1440,1000)):
                        await page.set_viewport_size({'width':width,'height':height})
                        await page.goto('http://127.0.0.1:'+str(server.server_port))
                        assert not await page.evaluate('document.documentElement.scrollWidth>innerWidth')
                        assert 'SECRET_FIXTURE' not in await page.content()
                        button=page.get_by_role('button',name='Скопировать диагностику')
                        await button.click();await expect(button).to_have_text('✓ Скопировано')
                        copied=await page.evaluate('navigator.clipboard.readText()')
                        assert run_id in copied and 'BRANCH_DIVERGED' in copied and 'SECRET_FIXTURE' not in copied
                    await page.reload()
                    await page.evaluate("Object.defineProperty(navigator,'clipboard',{configurable:true,value:{writeText:async()=>{throw Error('fixture')}}})")
                    await page.get_by_role('button',name='Скопировать диагностику').click()
                    await expect(page.locator('#refresh-progress .steam-text')).to_be_visible()
                    assert not errors,errors
                    await context.close();await browser.close()
            finally:server.shutdown();server.server_close();worker.join()
    print('INCIDENT_PANEL_BROWSER_QA=PASSED')

if __name__=='__main__':asyncio.run(main())
