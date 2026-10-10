"""Real Chromium image/decode check; excludes only remote tracking images."""
import argparse
import asyncio
import json
from pathlib import Path
from playwright.async_api import async_playwright

async def check(url,output):
    async with async_playwright() as pw:
        browser=await pw.chromium.launch(executable_path='/usr/bin/chromium',headless=True)
        page=await browser.new_page(viewport={'width':1440,'height':1000})
        await page.goto(url,wait_until='networkidle',timeout=60000)
        images=page.locator('img[src*="assets/"]')
        for i in range(await images.count()):
            await images.nth(i).scroll_into_view_if_needed()
            await images.nth(i).evaluate('(img)=>img.decode()')
        bad=await images.evaluate_all('(imgs)=>imgs.filter(i=>!i.complete||!i.naturalWidth).map(i=>i.src)')
        if bad:raise RuntimeError('Unloaded assets: '+str(bad))
        await page.screenshot(path=str(output),full_page=True)
        result=dict(status='PASSED',url=url,imageCount=await images.count(),screenshot=str(output))
        output.with_suffix('.json').write_text(json.dumps(result,indent=2),encoding='utf-8')
        print(json.dumps(result));await browser.close()

if __name__=='__main__':
    parser=argparse.ArgumentParser();parser.add_argument('url');parser.add_argument('output',type=Path)
    args=parser.parse_args();asyncio.run(check(args.url,args.output))
