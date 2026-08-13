import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const reportDir = path.dirname(fileURLToPath(import.meta.url));
const artifactPath = path.join(reportDir, 'artifact.json');
const htmlPath = path.join(reportDir, 'current-week.html');
const statePath = path.join(reportDir, '..', 'data', 'current-season.json');
const projectPath = path.join(reportDir, '..', 'data', 'project.json');
const artifact = JSON.parse(fs.readFileSync(artifactPath, 'utf8'));
const state = JSON.parse(fs.readFileSync(statePath, 'utf8'));
const project = JSON.parse(fs.readFileSync(projectPath, 'utf8'));
const blocks = artifact?.manifest?.blocks ?? [];
const title = artifact?.manifest?.title;
const generatedAt = artifact?.snapshot?.generatedAt ?? artifact?.manifest?.generatedAt;
const deadlineAt = state?.season?.endAt;
const expectedCardCount = Number(state?.season?.expectedCardCount);
const maxPublicHtmlBytes = Number(state?.season?.maxPublicHtmlBytes ?? 200_000);
const branding = project?.branding;
const support = project?.support;

if (!title || !generatedAt || Number.isNaN(Date.parse(generatedAt)) || Number.isNaN(Date.parse(deadlineAt))) {
  throw new Error('artifact.json and current-season.json must contain valid title, generatedAt and endAt values');
}
if (!Number.isInteger(expectedCardCount) || expectedCardCount < 1) {
  throw new Error(`Invalid expectedCardCount: ${state?.season?.expectedCardCount}`);
}
if (blocks.length !== expectedCardCount || blocks.some((block) => block.type !== 'html' || !block.body)) {
  throw new Error(`Expected exactly ${expectedCardCount} HTML activity blocks, received ${blocks.length}`);
}
if (!branding?.faviconPng || !branding.appleTouchIcon || !/^#[0-9a-f]{6}$/i.test(branding.themeColor ?? '')) {
  throw new Error('data/project.json must contain complete branding assets and a valid themeColor');
}
for (const [name, value] of Object.entries({ faviconPng: branding.faviconPng, appleTouchIcon: branding.appleTouchIcon })) {
  if (!value.startsWith('reports/assets/project/')) throw new Error(`${name} must stay under reports/assets/project/: ${value}`);
  const assetPath = path.join(reportDir, ...value.slice('reports/'.length).split('/'));
  if (!fs.existsSync(assetPath)) throw new Error(`Missing branding asset: ${value}`);
}
if (!support?.enabled || !support.title || !support.description || !support.url || !support.buttonLabel || !support.qrAsset) {
  throw new Error('data/project.json must contain an enabled and complete support block');
}
if (!/^https:\/\/www\.sberbank\.com\//.test(support.url)) {
  throw new Error(`Invalid support URL: ${support.url}`);
}
if (!support.qrAsset.startsWith('reports/assets/project/')) {
  throw new Error(`Support QR must stay under reports/assets/project/: ${support.qrAsset}`);
}
const supportQrSrc = support.qrAsset.slice('reports/'.length);
const supportQrPath = path.join(reportDir, ...supportQrSrc.split('/'));
if (!fs.existsSync(supportQrPath)) throw new Error(`Missing support QR: ${support.qrAsset}`);
const faviconPngSrc = branding.faviconPng.slice('reports/'.length);
const appleTouchIconSrc = branding.appleTouchIcon.slice('reports/'.length);

function escapeHtml(value) {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;');
}

function staticCard(block, index) {
  let body = block.body.replace(/<style>[\s\S]*?<\/style>/i, '').trim();
  body = body.replace(
    /src="data:image\/[^\"]+"\s+data-local-src="([^"]+)"/g,
    'src="$1"'
  );
  if (index === 0) {
    body = body.replace('loading="lazy"', 'loading="eager" fetchpriority="high"');
  }
  if (body.includes('data:image/') || body.includes('data-local-src=')) {
    throw new Error(`Failed to externalize images in block ${block.id}`);
  }
  for (const match of body.matchAll(/src="(assets\/[^"]+)"/g)) {
    const assetPath = path.join(reportDir, ...match[1].split('/'));
    if (!fs.existsSync(assetPath)) throw new Error(`Missing referenced asset: ${match[1]}`);
  }
  return `<section class="activity-block" id="${escapeHtml(block.id)}" data-activity-block>${body}</section>`;
}

const sharedStyleMatch = blocks[0].body.match(/<style>([\s\S]*?)<\/style>/i);
if (!sharedStyleMatch) throw new Error('The first activity block has no shared card styles');
const sharedCardCss = sharedStyleMatch[1];
const cardsHtml = blocks.map(staticCard).join('\n');
const supportHtml = `
    <section class="support-section" id="support-project" data-support-block>
      <h2>${escapeHtml(support.title)}</h2>
      <p>${escapeHtml(support.description)}</p>
      <a class="support-qr-link" href="${escapeHtml(support.url)}" target="_blank" rel="noopener noreferrer" aria-label="${escapeHtml(support.buttonLabel)}">
        <img class="support-qr" src="${escapeHtml(supportQrSrc)}" width="636" height="636" loading="lazy" alt="QR-код для поддержки проекта через Сбербанк">
      </a>
      <a class="support-button" href="${escapeHtml(support.url)}" target="_blank" rel="noopener noreferrer">${escapeHtml(support.buttonLabel)}</a>
    </section>`;
const updatedText = new Intl.DateTimeFormat('ru-RU', {
  timeZone: 'Asia/Krasnoyarsk',
  day: '2-digit',
  month: '2-digit',
  year: 'numeric',
  hour: '2-digit',
  minute: '2-digit',
  hourCycle: 'h23'
}).format(new Date(generatedAt));

const html = `<!doctype html>
<html lang="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
  <meta name="color-scheme" content="dark">
  <meta name="theme-color" content="${escapeHtml(branding.themeColor)}">
  <link rel="icon" href="${escapeHtml(faviconPngSrc)}" type="image/png" sizes="32x32">
  <link rel="apple-touch-icon" href="${escapeHtml(appleTouchIconSrc)}" sizes="180x180">
  <meta http-equiv="Content-Security-Policy" content="default-src 'self'; img-src 'self'; style-src 'unsafe-inline'; script-src 'unsafe-inline'; connect-src 'none'; font-src 'none'; frame-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none'">
  <title>${escapeHtml(title)}</title>
  <style>
${sharedCardCss}
    html{scroll-behavior:smooth;background:#071014}
    body{min-width:0;overflow-x:hidden}
    .page-header{position:sticky;top:0;z-index:100;display:grid;grid-template-columns:minmax(0,1fr) auto;align-items:center;gap:20px;padding:12px max(20px,calc((100vw - 1360px)/2 + 24px));border-bottom:1px solid #29434b;background:#071014f2;backdrop-filter:blur(12px)}
    .page-header h1{min-width:0;margin:0;overflow:hidden;color:#fff;font-size:16px;line-height:1.35;font-weight:750;text-overflow:ellipsis;white-space:nowrap}
    .page-meta{display:flex;align-items:center;justify-content:flex-end;gap:12px;color:#b8ccd1;font-size:12px;white-space:nowrap}
    .countdown{display:inline-flex;align-items:center;padding:6px 11px;border:1px solid #36515a;border-radius:999px;background:#0e2025}
    .countdown strong{margin-left:5px;color:#d9ff00;font-variant-numeric:tabular-nums}
    .updated{color:#8ea8ae}
    .report{width:min(1360px,100%);margin:0 auto;padding:28px 32px 64px}
    .activity-list{display:grid;gap:28px}
    .activity-block{min-width:0;content-visibility:auto;contain-intrinsic-size:auto 360px}
    .activity-block .card{width:100%}
    .support-section{display:flex;flex-direction:column;align-items:center;margin-top:34px;padding:30px 22px;border:1px solid #29434b;border-radius:22px;background:linear-gradient(145deg,#0b191e,#10242a);text-align:center}
    .support-section h2{margin:0;color:#fff;font-size:clamp(22px,3vw,32px);line-height:1.2}
    .support-section p{max-width:650px;margin:12px 0 20px;color:#b8ccd1;font-size:15px;line-height:1.55}
    .support-qr-link{display:block;border-radius:18px;background:#fff;line-height:0;box-shadow:0 12px 32px #0007}
    .support-qr{display:block;width:min(240px,70vw);height:auto;border-radius:18px}
    .support-button{display:inline-flex;align-items:center;justify-content:center;min-height:50px;margin-top:20px;padding:0 24px;border-radius:14px;background:#21a038;color:#fff!important;font-size:16px;font-weight:750;text-decoration:none;box-shadow:0 8px 22px #0005;transition:transform .15s ease,background .15s ease}
    .support-button:hover{background:#27b743;transform:translateY(-1px)}
    .support-button:focus-visible,.support-qr-link:focus-visible{outline:3px solid #d9ff00;outline-offset:4px}
    @media(max-width:760px){
      .page-header{position:static;grid-template-columns:1fr;padding:16px 18px;gap:9px}
      .page-header h1{font-size:20px;white-space:normal}
      .page-meta{justify-content:flex-start;flex-wrap:wrap;gap:8px;font-size:11px}
      .report{padding:18px 14px 44px}
      .activity-list{gap:18px}
      .activity-block{contain-intrinsic-size:auto 620px}
      .support-section{margin-top:24px;padding:24px 16px;border-radius:18px}
      .support-button{width:100%;padding:0 14px;font-size:15px}
    }
    @media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
  </style>
</head>
<body>
  <header class="page-header">
    <h1>${escapeHtml(title)}</h1>
    <div class="page-meta">
      <span class="countdown">Заканчивается через <strong id="season-countdown">—</strong></span>
      <time class="updated" datetime="${escapeHtml(generatedAt)}">Обновлено: ${escapeHtml(updatedText)}</time>
    </div>
  </header>
  <main class="report">
    <div class="activity-list">
${cardsHtml}
    </div>
${supportHtml}
  </main>
  <script>
  (() => {
    const output = document.getElementById('season-countdown');
    const deadline = Date.parse(${JSON.stringify(deadlineAt)});
    function tick() {
      let seconds = Math.max(0, Math.floor((deadline - Date.now()) / 1000));
      const days = Math.floor(seconds / 86400); seconds %= 86400;
      const hours = Math.floor(seconds / 3600); seconds %= 3600;
      const minutes = Math.floor(seconds / 60); seconds %= 60;
      output.textContent = days + 'д ' + String(hours).padStart(2,'0') + 'ч ' + String(minutes).padStart(2,'0') + 'м ' + String(seconds).padStart(2,'0') + 'с';
    }
    tick();
    window.setInterval(tick, 1000);
  })();
  </script>
</body>
</html>`;

function writeFileWithRetry(filePath, content, attempts = 8) {
  let lastError;
  for (let attempt = 1; attempt <= attempts; attempt += 1) {
    try {
      fs.writeFileSync(filePath, content, 'utf8');
      return;
    } catch (error) {
      lastError = error;
      if (!['EBUSY', 'EPERM', 'EACCES', 'UNKNOWN'].includes(error?.code) || attempt === attempts) throw error;
      Atomics.wait(new Int32Array(new SharedArrayBuffer(4)), 0, 0, attempt * 150);
    }
  }
  throw lastError;
}

writeFileWithRetry(htmlPath, html);

const outputBytes = fs.statSync(htmlPath).size;
if (outputBytes > maxPublicHtmlBytes) throw new Error(`Lightweight report is unexpectedly large: ${outputBytes} bytes`);
if ((html.match(/data-activity-block/g) ?? []).length !== expectedCardCount) throw new Error('Lightweight report lost activity blocks');
if ((html.match(/data-support-block/g) ?? []).length !== 1 || !html.includes(support.url) || !html.includes(supportQrSrc)) {
  throw new Error('Lightweight report lost the configured support block');
}
for (const asset of [faviconPngSrc, appleTouchIconSrc]) {
  if (!html.includes(asset)) throw new Error(`Lightweight report lost branding asset: ${asset}`);
}
if (html.includes('<iframe') || html.includes('data:image/') || html.includes('data-analytics-portable-reader')) {
  throw new Error('Lightweight report still contains a heavy portable runtime or embedded images');
}

console.log(`Built lightweight ${htmlPath}: ${outputBytes} bytes, ${expectedCardCount} cards, 0 iframes`);
