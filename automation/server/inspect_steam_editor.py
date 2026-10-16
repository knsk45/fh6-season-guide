"""Read-only existing editor inspection; never output credentials or cookies."""
import fcntl
import json
from pathlib import Path
from urllib.parse import parse_qs, urlsplit

ROOT = Path('/opt/fh6/repo')
CONFIG = Path('/etc/fh6/steam-browser.json')
STORE = Path('/var/lib/fh6')

INSPECT = r'''expected => {
 const visible = e => !!e.getClientRects().length && getComputedStyle(e).visibility !== 'hidden';
 const safe = v => /^[\w .:\-]{0,100}$/.test(v || '') ? (v || '') : '';
 const functionName = v => {
  const match = (v || '').match(/^\s*(?:javascript:\s*)?(?:return\s+)?([A-Za-z_$][\w$]*)\s*\(/);
  return match ? match[1] : null;
 };
 const controls = Array.from(document.querySelectorAll('input:not([type="hidden"]):not([type="password"]),textarea,button,a,[role="button"],[onclick]:not([type="hidden"]):not([type="password"])'))
  .filter(visible).map(e => {
   const kind = e.tagName.toLowerCase();
   const type = (e.getAttribute('type') || '').toLowerCase();
   const text = kind==='input' && /^(submit|button)$/.test(type) ? e.value : (e.textContent || '').trim();
   // Steam may expose Save as a javascript: link, rather than a button/onclick.
   // Return only a boolean label match and a function identifier, never link
   // arguments, account names, session IDs, or an arbitrary element's text.
   const saveLabel = /\bsave\b|сохранить/i.test(text);
   const href = e.getAttribute('href') || '';
   const hrefIsJavascript = /^\s*javascript:/i.test(href);
   return {tag:kind,id:safe(e.id),name:safe(e.getAttribute('name')),type:safe(type),class:safe(e.getAttribute('class')),
    enabled:!e.disabled,titleMatches:kind==='input' && type!=='password' && e.value===expected,
    textLength:kind==='textarea' ? e.value.length : null,
    saveLabel,onclickFunction:functionName(e.getAttribute('onclick')),
    onclickPresent:e.hasAttribute('onclick'),
    hrefFunction:hrefIsJavascript ? functionName(href) : null,
    hrefIsJavascript,role:safe(e.getAttribute('role'))};
  });
 return {controls:controls.filter(e=>e.titleMatches || e.tag==='textarea' || e.saveLabel || e.onclickPresent || e.hrefIsJavascript || e.tag==='button' || e.role==='button' || /^(submit|button|image)$/.test(e.type)),textareaCount:controls.filter(e=>e.tag==='textarea').length,
  titleMatchCount:controls.filter(e=>e.titleMatches).length};
}'''


def validate(config, project):
    if config.get('publishEnabled') is True:
        raise RuntimeError('Publication must remain disabled during setup')
    if config['cdp'] != 'http://127.0.0.1:9222' or config['publicUrl'] != project['url']:
        raise RuntimeError('Unexpected browser or guide mapping')
    ids=[]
    for lang in ('ru','en'):
        section=config['sections'][lang];url=urlsplit(section['editUrl']);query=parse_qs(url.query)
        if (url.scheme!='https' or url.netloc!='steamcommunity.com'
                or url.path!='/sharedfiles/editguidesubsection/'
                or query.get('id')!=[project['id']]
                or not query.get('sectionid',[''])[0].isdigit()
                or section['titleText']!=project['sections'][lang]['title']):
            raise RuntimeError('Unexpected existing section mapping')
        ids.append(query['sectionid'][0])
    if len(set(ids))!=2:raise RuntimeError('Distinct existing sections required')


def main():
    config=json.loads(CONFIG.read_text())
    project=json.loads((ROOT/'data/project.json').read_text(encoding='utf-8-sig'))['steamGuide']
    validate(config,project)
    results=[]
    with (STORE/'runner.lock').open('rb') as lock:
        fcntl.flock(lock,fcntl.LOCK_EX|fcntl.LOCK_NB)
        from playwright.sync_api import sync_playwright
        with sync_playwright() as pw:
            browser=pw.chromium.connect_over_cdp(config['cdp'],timeout=15000)
            if len(browser.contexts)!=1:raise RuntimeError('Expected one dedicated browser context')
            for lang in ('ru','en'):
                page=browser.contexts[0].new_page()
                try:
                    section=config['sections'][lang]
                    response=page.goto(section['editUrl'],wait_until='domcontentloaded',timeout=20000)
                    page.wait_for_timeout(3000)
                    current=urlsplit(page.url)
                    result={'locale':lang,'httpStatus':response.status if response else None,
                            'exactEditUrl':page.url==section['editUrl'],
                            'loginRedirect':'/login' in current.path}
                    if current.scheme=='https' and current.netloc=='steamcommunity.com' and current.path=='/sharedfiles/editguidesubsection/':
                        result.update(page.evaluate(INSPECT,section['titleText']))
                    results.append(result)
                finally:page.close()
            # Disconnect the inspection transport without closing the owner's browser.
    print('STEAM_EDITOR_INSPECTION_READ_ONLY no form filled or submitted; no cookies accessed')
    for result in results:
        print(json.dumps(result,ensure_ascii=False,separators=(',',':')))


if __name__=='__main__':
    try:main()
    except Exception as error:
        print('STEAM_EDITOR_INSPECTION_FAILED type='+type(error).__name__)
        raise SystemExit(1)
