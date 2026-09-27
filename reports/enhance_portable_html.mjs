import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const cliArgs = process.argv.slice(2);
for (let i = 0; i < cliArgs.length; i += 2) {
  if (!['--root', '--output'].includes(cliArgs[i]) || !cliArgs[i + 1]) throw new Error('Usage: enhance_portable_html.mjs [--root project] [--output file]');
}
const option = (key) => cliArgs.includes(key) ? cliArgs[cliArgs.indexOf(key) + 1] : undefined;
const reportDir = option('--root') ? path.join(path.resolve(option('--root')), 'reports') : path.dirname(fileURLToPath(import.meta.url));
const artifactPath = path.join(reportDir, 'artifact.json');
const htmlPath = option('--output') ? path.resolve(option('--output')) : path.join(reportDir, 'current-week.html');
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
const analytics = project?.analytics;
const community = project?.community;
const steamGuide = project?.steamGuide;
const publicationMetrics = artifact?.snapshot?.datasets?.publicationMetrics;
const englishLocale = state?.locales?.en;

if (!title || !generatedAt || Number.isNaN(Date.parse(generatedAt)) || Number.isNaN(Date.parse(deadlineAt))) {
  throw new Error('artifact.json and current-season.json must contain valid title, generatedAt and endAt values');
}
if (!Number.isInteger(expectedCardCount) || expectedCardCount < 1) {
  throw new Error(`Invalid expectedCardCount: ${state?.season?.expectedCardCount}`);
}
if (!englishLocale?.reportTitle || !englishLocale?.seasonDisplay || !englishLocale?.activities ||
    state.activities.some((activity) => !englishLocale.activities[activity.id])) {
  throw new Error('data/current-season.json must contain a complete English locale for every activity');
}
for (const activity of state.activities) {
  const translation = englishLocale.activities[activity.id];
  for (const field of ['title', 'points', 'conditionHtml', 'howHtml', 'tuneHtml']) {
    if (typeof translation[field] !== 'string' || !translation[field].trim()) {
      throw new Error(`English locale is missing ${field} for ${activity.id}`);
    }
  }
}
if (blocks.length !== expectedCardCount || blocks.some((block) => block.type !== 'html' || !block.body)) {
  throw new Error(`Expected exactly ${expectedCardCount} HTML activity blocks, received ${blocks.length}`);
}
if (!branding?.faviconPng || !branding.appleTouchIcon || !/^#[0-9a-f]{6}$/i.test(branding.themeColor ?? '')) {
  throw new Error('data/project.json must contain complete branding assets and a valid themeColor');
}
if (!steamGuide?.enabled || !steamGuide?.url || !steamGuide?.title) {
  throw new Error('data/project.json must contain the enabled public Steam guide');
}
if (!/^https:\/\/github\.com\/knsk45\/fh6-season-guide\/issues\/new$/.test(community?.feedbackUrl ?? '') || !community?.feedbackTitlePrefix) {
  throw new Error('data/project.json must contain the configured public GitHub feedback endpoint');
}
for (const [name, value] of Object.entries({ faviconPng: branding.faviconPng, appleTouchIcon: branding.appleTouchIcon })) {
  if (!value.startsWith('reports/assets/project/')) throw new Error(`${name} must stay under reports/assets/project/: ${value}`);
  const assetPath = path.join(reportDir, ...value.slice('reports/'.length).split('/'));
  if (!fs.existsSync(assetPath)) throw new Error(`Missing branding asset: ${value}`);
}
if (!support?.enabled || !support.title || !support.description || !support.url || !support.buttonLabel || !support.qrAsset || !support.boosty?.url || !support.boosty?.buttonLabel || !support.boosty?.internationalButtonLabel) {
  throw new Error('data/project.json must contain an enabled and complete support block');
}
if (!/^https:\/\/www\.sberbank\.com\//.test(support.url)) {
  throw new Error(`Invalid support URL: ${support.url}`);
}
if (!/^https:\/\/boosty\.to\/knsk45\/?$/.test(support.boosty.url)) {
  throw new Error(`Invalid Boosty URL: ${support.boosty.url}`);
}
if (!support.qrAsset.startsWith('reports/assets/project/')) {
  throw new Error(`Support QR must stay under reports/assets/project/: ${support.qrAsset}`);
}
const supportQrSrc = support.qrAsset.slice('reports/'.length);
const supportQrPath = path.join(reportDir, ...supportQrSrc.split('/'));
if (!fs.existsSync(supportQrPath)) throw new Error(`Missing support QR: ${support.qrAsset}`);
if (!analytics?.enabled || analytics.provider !== 'hits.sh' || !analytics.title || !analytics.description || !analytics.counterImageUrl || !analytics.dashboardUrl) {
  throw new Error('data/project.json must contain an enabled and complete hits.sh analytics block');
}
if (!/^https:\/\/hits\.sh\/.+\.svg(?:\?.*)?$/.test(analytics.counterImageUrl)) {
  throw new Error(`Invalid hits.sh counter image URL: ${analytics.counterImageUrl}`);
}
if (!/^https:\/\/hits\.sh\/.+\/$/.test(analytics.dashboardUrl)) {
  throw new Error(`Invalid hits.sh dashboard URL: ${analytics.dashboardUrl}`);
}
if (!publicationMetrics || !Array.isArray(publicationMetrics.rows) || publicationMetrics.rows.length < 2 || publicationMetrics.rows.length > 30) {
  throw new Error('artifact.json must contain 2-30 publication-metrics rows');
}
if (!publicationMetrics.source?.steam || !publicationMetrics.source?.github || !publicationMetrics.title || !publicationMetrics.description) {
  throw new Error('Publication metrics chart is missing source metadata');
}
const faviconPngSrc = branding.faviconPng.slice('reports/'.length);
const appleTouchIconSrc = branding.appleTouchIcon.slice('reports/'.length);
const englishLocaleJson = JSON.stringify(englishLocale).replace(/</g, '\\u003c');
const activityKindsJson = JSON.stringify(Object.fromEntries(state.activities.map((activity) => [activity.id, activity.kind]))).replace(/</g, '\\u003c');

function escapeHtml(value) {
  return String(value)
    .replaceAll('&', '&amp;')
    .replaceAll('<', '&lt;')
    .replaceAll('>', '&gt;')
    .replaceAll('"', '&quot;');
}

function publicationChartHtml(dataset) {
  const rows = dataset.rows;
  const width = 660;
  const height = 270;
  const pad = { left: 44, right: 18, top: 22, bottom: 42 };
  const plotWidth = width - pad.left - pad.right;
  const plotHeight = height - pad.top - pad.bottom;
  const values = rows.flatMap((row) => [Number(row.steamViews), Number(row.githubViews)]);
  const max = Math.max(...values);
  const scaleMax = Math.max(10, Math.ceil(max / 100) * 100);
  const x = (index) => pad.left + (rows.length === 1 ? plotWidth / 2 : (plotWidth * index) / (rows.length - 1));
  const y = (value) => pad.top + plotHeight - (Number(value) / scaleMax) * plotHeight;
  const path = (key) => rows.map((row, index) => `${index ? 'L' : 'M'}${x(index).toFixed(1)},${y(row[key]).toFixed(1)}`).join(' ');
  const last = rows.at(-1);
  const formatLabel = (value) => new Intl.DateTimeFormat('ru-RU', { timeZone: 'Asia/Krasnoyarsk', day: '2-digit', month: '2-digit' }).format(new Date(value));
  const labelIndexes = [...new Set([0, Math.floor((rows.length - 1) / 2), rows.length - 1])];
  const labels = labelIndexes.map((index) => `<text class="trend-axis-label" x="${x(index).toFixed(1)}" y="${height - 14}" text-anchor="middle">${escapeHtml(formatLabel(rows[index].collectedAt))}</text>`).join('');
  const gridValues = [0, Math.round(scaleMax / 2), scaleMax];
  const grid = gridValues.map((value) => `<line class="trend-grid" x1="${pad.left}" x2="${width - pad.right}" y1="${y(value).toFixed(1)}" y2="${y(value).toFixed(1)}"></line><text class="trend-axis-label" x="${pad.left - 8}" y="${(y(value) + 4).toFixed(1)}" text-anchor="end">${value}</text>`).join('');
  const latestDate = new Intl.DateTimeFormat('ru-RU', { timeZone: 'Asia/Krasnoyarsk', day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit', hourCycle: 'h23' }).format(new Date(last.collectedAt));
  const formatCount = (value) => new Intl.NumberFormat('ru-RU').format(Number(value));
  return `
      <section class="publication-chart" data-publication-chart aria-labelledby="publication-chart-title">
        <h3 id="publication-chart-title">${escapeHtml(dataset.title)}</h3>
        <p class="publication-chart-subtitle" id="publication-chart-subtitle">${escapeHtml(dataset.description)}</p>
        <div class="publication-chart-legend" id="publication-chart-legend" role="group" aria-label="Легенда графика">
          <span class="publication-chart-legend-item"><span class="publication-chart-swatch trend-github" aria-hidden="true"></span><span id="chart-legend-github">GitHub · ${formatCount(last.githubViews)}</span></span>
          <span class="publication-chart-legend-item"><span class="publication-chart-swatch trend-steam" aria-hidden="true"></span><span id="chart-legend-steam">Steam · ${formatCount(last.steamViews)}</span></span>
        </div>
        <svg class="publication-chart-svg" id="publication-chart-svg" viewBox="0 0 ${width} ${height}" role="img" aria-label="Steam — уникальные посетители: ${last.steamViews}; GitHub — срабатывания счётчика страницы: ${last.githubViews}; последний замер ${escapeHtml(latestDate)}">
          ${grid}
          <path class="trend-line trend-steam" d="${path('steamViews')}"></path>
          <path class="trend-line trend-github" d="${path('githubViews')}"></path>
          <circle class="trend-point trend-steam" cx="${x(rows.length - 1).toFixed(1)}" cy="${y(last.steamViews).toFixed(1)}" r="4"></circle>
          <circle class="trend-point trend-github" cx="${x(rows.length - 1).toFixed(1)}" cy="${y(last.githubViews).toFixed(1)}" r="4"></circle>
          ${labels}
        </svg>
        <p class="publication-chart-note" id="publication-chart-note">Последний замер: ${escapeHtml(latestDate)} · Steam в избранном: ${last.steamFavorites}. Значения фиксируются после успешной публичной проверки.</p>
      </section>`;
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

const activityNavLinks = state.activities.map((activity) => {
  const englishTitle = englishLocale.activities[activity.id]?.title ?? activity.title;
  return `<a class="activity-nav-link" href="#${escapeHtml(activity.id)}" data-toc-link="${escapeHtml(activity.id)}"><span class="activity-nav-number">${escapeHtml(activity.number)}</span><span class="activity-nav-title" data-toc-title="${escapeHtml(activity.id)}" data-toc-title-ru="${escapeHtml(activity.title)}" data-toc-title-en="${escapeHtml(englishTitle)}">${escapeHtml(activity.title)}</span></a>`;
}).join('\n');

const sharedStyleMatch = blocks[0].body.match(/<style>([\s\S]*?)<\/style>/i);
if (!sharedStyleMatch) throw new Error('The first activity block has no shared card styles');
const sharedCardCss = sharedStyleMatch[1];
const cardsHtml = blocks.map(staticCard).join('\n');
const publicationChart = publicationChartHtml(publicationMetrics);
const feedbackActivityOptions = state.activities.map((activity) => {
  const englishTitle = englishLocale.activities[activity.id]?.title ?? activity.title;
  return `<option value="${escapeHtml(activity.id)}" data-number="${escapeHtml(activity.number)}" data-title-ru="${escapeHtml(activity.title)}" data-title-en="${escapeHtml(englishTitle)}">${escapeHtml(activity.number)} · ${escapeHtml(activity.title)}</option>`;
}).join('');
const communityHtml = `
    <section class="community-actions" aria-labelledby="community-title">
      <h2 id="community-title">Поделиться и помочь улучшить сводку</h2>
      <p id="community-description">Поделитесь гайдом или предложите исправление. Отзывы отправляются через GitHub и становятся публичными.</p>
      <div class="community-actions-row">
        <button class="community-button community-button-primary" id="share-guide-button" type="button">Поделиться сводкой</button>
        <button class="community-button" id="open-feedback-button" type="button" aria-haspopup="dialog" aria-controls="feedback-dialog">Нашли ошибку или хотите дополнить?</button>
        <a class="community-button" id="steam-discussion-link" href="${escapeHtml(steamGuide.url)}#comments" target="_blank" rel="noopener noreferrer">Обсудить в Steam</a>
      </div>
      <p class="community-status" id="community-status" aria-live="polite" role="status"></p>
      <dialog class="feedback-dialog" id="feedback-dialog" aria-labelledby="feedback-dialog-title">
        <div class="feedback-dialog-content">
          <h2 id="feedback-dialog-title">Сообщить об ошибке или предложить уточнение</h2>
          <label for="feedback-language" id="feedback-language-label">Язык сообщения</label>
          <select id="feedback-language"><option id="feedback-language-ru" value="ru">Русский</option><option id="feedback-language-en" value="en">English</option></select>
          <label for="feedback-activity" id="feedback-activity-label">Активность</label>
          <select id="feedback-activity"><option value="__guide__">Вся сводка</option>${feedbackActivityOptions}</select>
          <label for="feedback-comment" id="feedback-comment-label">Комментарий</label>
          <textarea id="feedback-comment" rows="5" maxlength="2000" required></textarea>
          <p class="feedback-privacy" id="feedback-privacy">Продолжая, вы откроете черновик публичного GitHub Issue; для отправки потребуется вход в GitHub. Не указывайте личные данные.</p>
          <div class="feedback-dialog-actions">
            <button class="community-button" id="cancel-feedback-button" type="button">Отмена</button>
            <a class="community-button community-button-primary" id="continue-feedback-link" href="${escapeHtml(community.feedbackUrl)}" target="_blank" rel="noopener noreferrer">Продолжить в GitHub</a>
          </div>
        </div>
      </dialog>
    </section>`;
const supportHtml = `
    <section class="support-section" id="support-project" data-support-block>
      <h2 id="support-title">${escapeHtml(support.title)}</h2>
      <p id="support-description">${escapeHtml(support.description)}</p>
      <a class="support-qr-link" data-support-method="sber" href="${escapeHtml(support.url)}" target="_blank" rel="noopener noreferrer" aria-label="${escapeHtml(support.buttonLabel)}">
        <img class="support-qr" src="${escapeHtml(supportQrSrc)}" width="636" height="636" loading="lazy" alt="QR-код для поддержки проекта через Сбербанк">
      </a>
      <div class="support-actions">
        <a class="support-button support-button-sber" id="support-sber-button" data-support-method="sber" href="${escapeHtml(support.url)}" target="_blank" rel="noopener noreferrer">${escapeHtml(support.buttonLabel)}</a>
        <a class="support-button support-button-boosty" id="support-boosty-button" data-support-method="boosty" href="${escapeHtml(support.boosty.url)}" target="_blank" rel="noopener noreferrer">${escapeHtml(support.boosty.buttonLabel)}</a>
      </div>
      <div class="visit-stats" data-visit-stats>
        <h3 id="analytics-title">${escapeHtml(analytics.title)}</h3>
        <a class="visit-stats-link" id="analytics-link" href="${escapeHtml(analytics.dashboardUrl)}" target="_blank" rel="noopener noreferrer" aria-label="Открыть подробную статистику посещений">
          <img class="visit-stats-badge" id="analytics-badge" src="${escapeHtml(analytics.counterImageUrl)}" height="28" alt="Посещения страницы: сегодня и всего" referrerpolicy="no-referrer">
        </a>
        <p class="visit-stats-note" id="analytics-description">${escapeHtml(analytics.description)}</p>
      </div>
${publicationChart}
      <a class="steam-guide-link" data-steam-guide-link id="steam-guide-link" href="${escapeHtml(steamGuide.url)}" target="_blank" rel="noopener noreferrer">Открыть руководство в Steam</a>
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
<html lang="ru" data-language="ru">
<head>
  <meta charset="utf-8">
  <meta name="viewport" content="width=device-width,initial-scale=1,viewport-fit=cover">
  <meta name="color-scheme" content="dark">
  <meta name="theme-color" content="${escapeHtml(branding.themeColor)}">
  <link rel="icon" href="${escapeHtml(faviconPngSrc)}" type="image/png" sizes="32x32">
  <link rel="apple-touch-icon" href="${escapeHtml(appleTouchIconSrc)}" sizes="180x180">
  <meta http-equiv="Content-Security-Policy" content="default-src 'self'; img-src 'self' https://hits.sh; style-src 'unsafe-inline'; script-src 'unsafe-inline'; connect-src 'none'; font-src 'none'; frame-src 'none'; object-src 'none'; base-uri 'none'; form-action 'none'">
  <title>${escapeHtml(title)}</title>
  <style>
${sharedCardCss}
    html{scroll-behavior:smooth;background:#071014}
    body{min-width:0;overflow-x:hidden}
    .page-header{position:sticky;top:0;z-index:100;display:grid;gap:9px;padding:12px max(20px,calc((100vw - 1360px)/2 + 24px));border-bottom:1px solid #29434b;background:#071014f2;backdrop-filter:blur(12px)}
    .header-title-row{display:flex;align-items:center;justify-content:space-between;gap:16px;min-width:0}
    .page-header h1{min-width:0;margin:0;color:#fff;font-size:16px;line-height:1.35;font-weight:750}
    .language-switch{display:inline-flex;flex:0 0 auto;align-items:center;gap:2px;padding:3px;border:1px solid #36515a;border-radius:10px;background:#0e2025}
    .language-switch-label{padding:0 5px;color:#8ea8ae;font-size:11px;font-weight:700}
    .language-switch button{min-width:34px;padding:4px 7px;border:0;border-radius:7px;background:transparent;color:#b8ccd1;font:700 11px/1 Inter,Segoe UI,Arial,sans-serif;cursor:pointer}
    .language-switch button[aria-pressed="true"]{background:#d9ff00;color:#071014}.language-switch button:focus-visible{outline:2px solid #fff;outline-offset:2px}
    .page-meta{display:flex;align-items:center;justify-content:flex-start;flex-wrap:wrap;gap:8px 12px;color:#b8ccd1;font-size:12px}
    .countdown{display:inline-flex;align-items:center;padding:6px 11px;border:1px solid #36515a;border-radius:999px;background:#0e2025}
    .countdown strong{margin-left:5px;color:#d9ff00;font-variant-numeric:tabular-nums}
    .updated{color:#8ea8ae}
    .completion-progress{color:#d9ff00;font-variant-numeric:tabular-nums}.completion-filter{display:inline-flex;align-items:center;gap:5px;color:#b8ccd1;cursor:pointer}.completion-filter input{accent-color:#d9ff00}.hide-completed .activity-block.is-complete{display:none}.copy-code.copied:after{content:'Скопировано'}
    html[data-language="en"] .copy-code.copied:after{content:'Copied'}html[data-language="en"] .completion-toggle:after{content:'Mark complete'}html[data-language="en"] .completion-toggle[aria-pressed="true"]:after{content:'Completed'}
    .report{width:min(1360px,100%);margin:0 auto;padding:28px 32px 64px}
    .activity-list{display:grid;gap:28px}
    .activity-block{min-width:0;content-visibility:auto;contain-intrinsic-size:auto 360px}
    .activity-block .card{width:100%}
    .community-actions{margin:30px 0 0;padding:22px;border:1px solid #29434b;border-radius:18px;background:linear-gradient(145deg,#0b191e,#10242a)}
    .community-actions h2{margin:0;color:#fff;font-size:20px;line-height:1.3}.community-actions>p:not(.community-status){margin:8px 0 16px;color:#b8ccd1;font-size:14px;line-height:1.5}
    .community-actions-row{display:flex;flex-wrap:wrap;gap:10px}.community-button{display:inline-flex;min-height:44px;align-items:center;justify-content:center;padding:10px 16px;border:1px solid #45636c;border-radius:11px;background:#10242a;color:#eaf4f2!important;font:700 14px/1.3 Inter,Segoe UI,Arial,sans-serif;text-align:center;text-decoration:none;cursor:pointer}
    .community-button:hover{border-color:#d9ff00;color:#d9ff00!important}.community-button-primary{border-color:#d9ff00;background:#d9ff00;color:#071014!important}.community-button-primary:hover{background:#e8ff58;color:#071014!important}
    .community-button:focus-visible,.feedback-dialog select:focus-visible,.feedback-dialog textarea:focus-visible{outline:3px solid #fff;outline-offset:3px}.community-status{min-height:1.4em;margin:9px 0 0!important;color:#d9ff00!important;font-size:13px!important}
    .feedback-dialog{width:min(560px,calc(100% - 24px));max-height:min(90dvh,760px);padding:0;border:1px solid #45636c;border-radius:18px;background:#0b171c;color:#eef6f5;box-shadow:0 24px 80px #000b}.feedback-dialog::backdrop{background:#000a;backdrop-filter:blur(3px)}.feedback-dialog-content{display:grid;gap:9px;padding:22px}
    .feedback-dialog h2{margin:0 0 6px;font-size:20px;line-height:1.3}.feedback-dialog label{color:#d9ff00;font-size:13px;font-weight:750}.feedback-dialog select,.feedback-dialog textarea{width:100%;min-height:42px;padding:10px;border:1px solid #36515a;border-radius:9px;background:#10242a;color:#eef6f5;font:inherit}.feedback-dialog textarea{resize:vertical;line-height:1.45}.feedback-privacy{margin:4px 0;color:#b8ccd1;font-size:12px;line-height:1.45}.feedback-dialog-actions{display:flex;justify-content:flex-end;flex-wrap:wrap;gap:9px;margin-top:4px}
    .support-section{display:flex;flex-direction:column;align-items:center;margin-top:34px;padding:30px 22px;border:1px solid #29434b;border-radius:22px;background:linear-gradient(145deg,#0b191e,#10242a);text-align:center}
    .support-section h2{margin:0;color:#fff;font-size:clamp(22px,3vw,32px);line-height:1.2}
    .support-section p{max-width:650px;margin:12px 0 20px;color:#b8ccd1;font-size:15px;line-height:1.55}
    .support-qr-link{display:block;border-radius:18px;background:#fff;line-height:0;box-shadow:0 12px 32px #0007}
    .support-qr{display:block;width:min(240px,70vw);height:auto;border-radius:18px}
    .support-actions{display:flex;flex-wrap:wrap;gap:12px;margin-top:20px}.support-button{display:inline-flex;align-items:center;justify-content:center;min-height:50px;padding:0 24px;border-radius:14px;background:#21a038;color:#fff!important;font-size:16px;font-weight:750;text-decoration:none;box-shadow:0 8px 22px #0005;transition:transform .15s ease,background .15s ease}.support-button-boosty{background:#f15a24}.support-button-boosty:hover{background:#ff7040!important}
    .support-button:hover{background:#27b743;transform:translateY(-1px)}
    html[data-language="en"] [data-support-method="sber"]{display:none}
    .visit-stats{width:min(100%,650px);margin-top:28px;padding-top:22px;border-top:1px solid #29434b}
    .visit-stats h3{margin:0 0 12px;color:#fff;font-size:17px;line-height:1.3}
    .visit-stats-link{display:inline-flex;min-height:28px;align-items:center;justify-content:center}
    .visit-stats-badge{display:block;width:auto;max-width:100%;height:28px}
    .support-section .visit-stats-note{margin:10px auto 0;color:#7f9aa1;font-size:12px;line-height:1.45}
    .publication-chart{width:min(100%,700px);margin-top:26px;padding-top:22px;border-top:1px solid #29434b;text-align:left}
    .publication-chart h3{margin:0;color:#fff;font-size:17px;line-height:1.3}
    .publication-chart-subtitle{margin:8px 0 12px!important;color:#b8ccd1!important;font-size:13px!important;line-height:1.5!important}
    .publication-chart-legend{display:flex;flex-wrap:wrap;gap:8px 20px;margin:12px 0 2px;color:#eef6f5;font-size:13px;font-weight:750}
    .publication-chart-legend-item{display:inline-flex;align-items:center;gap:8px;min-height:24px}
    .publication-chart-swatch{display:inline-block;width:24px;height:0;border-top:3px solid;border-radius:2px}.publication-chart-swatch.trend-github{border-color:#d9ff00;border-top-style:dashed}.publication-chart-swatch.trend-steam{border-color:#ff2f92}
    .publication-chart-svg{display:block;width:100%;height:auto;overflow:visible}
    .trend-grid{stroke:#29434b;stroke-width:1}.trend-axis-label{fill:#9bb4ba;font-size:11px;font-family:Inter,Segoe UI,Arial,sans-serif}.trend-line{fill:none;stroke-width:3;stroke-linecap:round;stroke-linejoin:round}.trend-steam{stroke:#ff2f92}.trend-github{stroke:#d9ff00;stroke-dasharray:7 5}.trend-point{stroke:#071014;stroke-width:2}.publication-chart-note{margin:8px 0 0!important;color:#9bb4ba!important;font-size:12px!important;line-height:1.5!important}
    .activity-toc{margin:0 0 24px;border:1px solid #29434b;border-radius:14px;background:#0d1a1f;box-shadow:0 8px 22px #0003}
    .activity-toc summary{padding:13px 16px;color:#d9ff00;font-size:15px;font-weight:800;cursor:pointer;list-style:none}
    .activity-toc summary::-webkit-details-marker{display:none}.activity-toc summary:after{content:'＋';float:right;color:#b8ccd1}.activity-toc details[open]>summary:after{content:'−'}
    .activity-toc-links{display:grid;grid-template-columns:repeat(auto-fit,minmax(190px,1fr));gap:6px;padding:0 12px 12px}
    .activity-nav-link{display:flex;align-items:flex-start;gap:9px;min-width:0;padding:9px 10px;border:1px solid #20363c;border-radius:9px;color:#dce9e9;text-decoration:none;font-size:13px;line-height:1.35;transition:background .15s ease,border-color .15s ease}
    .activity-nav-link:hover{border-color:#8fae00;background:#14272c}.activity-nav-link:focus-visible{outline:2px solid #d9ff00;outline-offset:2px}
    .activity-nav-number{flex:0 0 auto;color:#d9ff00;font-variant-numeric:tabular-nums;font-weight:900}.activity-nav-title{min-width:0;overflow-wrap:anywhere}
    .activity-block[id]{scroll-margin-top:116px}
    .steam-guide-link{display:inline-flex;align-items:center;justify-content:center;min-height:44px;margin-top:22px;padding:0 20px;border:1px solid #4b7690;border-radius:12px;color:#d9ff00!important;font-weight:750;text-decoration:none;background:#0e2025;transition:transform .15s ease,border-color .15s ease}.steam-guide-link:hover{border-color:#d9ff00;transform:translateY(-1px)}
    .support-button:focus-visible,.support-qr-link:focus-visible,.visit-stats-link:focus-visible{outline:3px solid #d9ff00;outline-offset:4px}
    @media(max-width:760px){
      .page-header{position:static;padding:16px 18px;gap:10px}
      .header-title-row{align-items:flex-start;flex-direction:column;gap:9px}
      .page-header h1{font-size:20px;white-space:normal}
      .page-meta{justify-content:flex-start;flex-wrap:wrap;gap:8px;font-size:11px}
      .report{padding:18px 14px 44px}
      .activity-toc{position:sticky;top:8px;z-index:80;margin:0 0 18px;background:#0b171cf5;backdrop-filter:blur(10px)}
      .activity-toc summary{min-height:46px;padding:14px 15px;font-size:14px}
      .activity-toc details[open]{max-height:min(72vh,620px);overflow:auto}
      .activity-toc-links{grid-template-columns:1fr;gap:5px;padding:0 9px 10px}
      .activity-nav-link{min-height:42px;padding:10px;font-size:14px}
      .activity-block[id]{scroll-margin-top:12px}
      .activity-list{gap:18px}
      .activity-block{contain-intrinsic-size:auto 620px}
      .support-section{margin-top:24px;padding:24px 16px;border-radius:18px}
      .community-actions{margin-top:20px;padding:18px 14px}.community-actions-row{display:grid;grid-template-columns:1fr}.community-button{width:100%;min-height:48px}.feedback-dialog-content{padding:18px 14px}.feedback-dialog-actions{display:grid;grid-template-columns:1fr}
      .support-actions{width:100%}.support-button{width:100%;padding:0 14px;font-size:15px}
      .visit-stats{margin-top:24px;padding-top:20px}
      .visit-stats-badge{height:26px}
      .publication-chart{margin-top:22px;padding-top:20px}
    }
    @media(prefers-reduced-motion:reduce){html{scroll-behavior:auto}}
  </style>
</head>
<body>
  <header class="page-header">
    <div class="header-title-row">
      <h1 id="report-title">${escapeHtml(title)}</h1>
      <div class="language-switch" role="group" aria-labelledby="language-switch-label">
        <span class="language-switch-label" id="language-switch-label">Язык</span>
        <button type="button" data-language-button="ru" aria-pressed="true">RU</button>
        <button type="button" data-language-button="en" aria-pressed="false">EN</button>
      </div>
    </div>
    <div class="page-meta">
      <span class="countdown"><span id="countdown-label">Заканчивается через</span> <strong id="season-countdown">—</strong></span>
      <time class="updated" datetime="${escapeHtml(generatedAt)}"><span id="updated-label">Обновлено:</span> ${escapeHtml(updatedText)}</time>
      <span class="completion-progress" id="completion-progress" aria-live="polite">Готово: 0/${expectedCardCount}</span>
      <label class="completion-filter"><input id="completion-filter" type="checkbox"><span id="completion-filter-label">Только невыполненные</span></label>
    </div>
  </header>
  <main class="report">
    <nav class="activity-toc" id="activity-toc-nav" aria-label="Навигация по активностям">
      <details id="activity-toc-details" open>
        <summary id="activity-toc-summary">Перейти к активности</summary>
        <div class="activity-toc-links">
${activityNavLinks}
        </div>
      </details>
    </nav>
    <div class="activity-list">
${cardsHtml}
    </div>
${communityHtml}
${supportHtml}
  </main>
  <script>
  (() => {
    const englishLocale = ${englishLocaleJson};
    const languageStorageKey = 'fh6-guide-language';
    const labels = {
      ru: {
        language: 'Язык', countdown: 'Заканчивается через', updated: 'Обновлено:', complete: 'Готово', unfinished: 'Только невыполненные',
        condition: 'Условие:', how: 'Как выполнить:', tune: 'Автомобиль и тюнинг:', supportTitle: ${JSON.stringify(support.title)},
        supportDescription: ${JSON.stringify(support.description)}, supportSberButton: ${JSON.stringify(support.buttonLabel)}, supportBoostyButton: ${JSON.stringify(support.boosty.buttonLabel)}, analyticsTitle: ${JSON.stringify(analytics.title)},
        analyticsDescription: ${JSON.stringify(analytics.description)}, analyticsLink: 'Открыть подробную статистику посещений', analyticsImage: 'Посещения страницы: сегодня и всего',
        steamGuide: 'Открыть руководство в Steam', toc: 'К активностям',
        communityTitle: 'Поделиться и помочь улучшить сводку', communityDescription: 'Поделитесь гайдом или предложите исправление. Отзывы отправляются через GitHub и становятся публичными.', shareGuide: 'Поделиться сводкой', shareCopied: 'Ссылка на сводку скопирована.', shareFailed: 'Не удалось скопировать автоматически — выделите и скопируйте адрес страницы.', feedbackOpen: 'Нашли ошибку или хотите дополнить?', steamDiscussion: 'Обсудить в Steam', feedbackDialogTitle: 'Сообщить об ошибке или предложить уточнение', feedbackLanguage: 'Язык сообщения', feedbackLanguageRu: 'Русский', feedbackLanguageEn: 'Английский', feedbackActivity: 'Активность', feedbackWholeGuide: 'Вся сводка', feedbackComment: 'Комментарий', feedbackPrivacy: 'Продолжая, вы откроете черновик публичного GitHub Issue; для отправки потребуется вход в GitHub. Не указывайте личные данные.', feedbackCancel: 'Отмена', feedbackContinue: 'Продолжить в GitHub', feedbackCommentRequired: 'Сначала добавьте комментарий.', feedbackIssueTitle: 'Отзыв о сводке FH6', feedbackIssueBody: 'Язык', feedbackIssueActivity: 'Активность', feedbackIssueComment: 'Комментарий', feedbackIssuePrivacy: 'Отправленный отзыв будет публичным на GitHub.', feedbackIssueReport: 'Ссылка на сводку'
      },
      en: {
        language: 'Language', countdown: 'Ends in', updated: 'Updated:', complete: 'Completed', unfinished: 'Only unfinished',
        condition: 'Requirement:', how: 'How to complete:', tune: 'Car and tune:', supportTitle: 'Say thanks (support the project)',
        supportDescription: 'If this guide saved you time, you can support the project with an international card via Boosty.', supportSberButton: 'Support via Sberbank', supportBoostyButton: ${JSON.stringify(support.boosty.internationalButtonLabel)},
        analyticsTitle: 'Visitor statistics', analyticsDescription: 'Page visits today and in total. Repeat loads and bots may increase the counter.',
        analyticsLink: 'Open detailed visitor statistics', analyticsImage: 'Page visits: today and total', steamGuide: 'Open the guide on Steam', toc: 'Jump to an activity',
        communityTitle: 'Share feedback and help improve the guide', communityDescription: 'Share the guide or suggest a correction. Feedback is submitted through GitHub and becomes public.', shareGuide: 'Share the guide', shareCopied: 'Guide link copied.', shareFailed: 'Could not copy automatically; select and copy the page address.', feedbackOpen: 'Found an error or want to add a tip?', steamDiscussion: 'Discuss on Steam', feedbackDialogTitle: 'Report an error or suggest a correction', feedbackLanguage: 'Comment language', feedbackLanguageRu: 'Russian', feedbackLanguageEn: 'English', feedbackActivity: 'Activity', feedbackWholeGuide: 'Whole guide', feedbackComment: 'Comment', feedbackPrivacy: 'Continue to open a public GitHub Issue draft; signing in to GitHub is required to submit it. Do not include personal information.', feedbackCancel: 'Cancel', feedbackContinue: 'Continue to GitHub', feedbackCommentRequired: 'Please add a comment first.', feedbackIssueTitle: ${JSON.stringify(community.feedbackTitlePrefix)}, feedbackIssueBody: 'Language', feedbackIssueActivity: 'Activity', feedbackIssueComment: 'Comment', feedbackIssuePrivacy: 'Submitted feedback will be public on GitHub.', feedbackIssueReport: 'Guide link'
      }
    };
    const kindLabels = {
      ru: { weekly: 'Еженедельное испытание', daily: 'Ежедневные задания', photo: 'Фотоиспытание', treasure_hunt: 'Охота за сокровищами', championship: 'Сезонный чемпионат', pr: 'PR-испытание', trial: 'The Trial', horizon_play: 'Horizon Play', monthly_rivals: 'Monthly Rivals' },
      en: { weekly: 'Weekly Challenge', daily: 'Daily Challenges', photo: 'Photo Challenge', treasure_hunt: 'Treasure Hunt', championship: 'Seasonal Championship', pr: 'PR Stunt', trial: 'The Trial', horizon_play: 'Horizon Play', monthly_rivals: 'Monthly Rivals' }
    };
    const readableKind = (kind, language) => kindLabels[language][kind] ?? String(kind || '')
      .replace(/[_-]+/g, ' ').trim().replace(/\b\w/g, letter => letter.toUpperCase());
    const provenanceLabels = {
      'Условия: Forza': 'Requirements: Forza', 'Решение: сообщество': 'Solution: community', 'Тюнинг: сообщество': 'Tune: community', 'Плитка: нужен скриншот': 'Tile: screenshot needed'
    };
    const sourceLabels = {
      'Официальная Playlist': 'Official Playlist', 'Новости Forza: British Automotive': 'Forza News: British Automotive',
      'Официальная карта Forza Labs': 'Official Forza Labs map', 'Forza Horizon Hub': 'Forza Horizon Hub',
      'Reddit: ForzaHorizon6': 'Reddit: ForzaHorizon6'
    };
    const chart = ${JSON.stringify({ title: publicationMetrics.title, description: publicationMetrics.description, latestDate: new Intl.DateTimeFormat('ru-RU', { timeZone: 'Asia/Krasnoyarsk', day: '2-digit', month: '2-digit', year: 'numeric', hour: '2-digit', minute: '2-digit', hourCycle: 'h23' }).format(new Date(publicationMetrics.rows.at(-1).collectedAt)), steamViews: publicationMetrics.rows.at(-1).steamViews, githubViews: publicationMetrics.rows.at(-1).githubViews, favorites: publicationMetrics.rows.at(-1).steamFavorites })};
    const output = document.getElementById('season-countdown');
    const deadline = Date.parse(${JSON.stringify(deadlineAt)});
    function tick() {
      let seconds = Math.max(0, Math.floor((deadline - Date.now()) / 1000));
      const days = Math.floor(seconds / 86400); seconds %= 86400;
      const hours = Math.floor(seconds / 3600); seconds %= 3600;
      const minutes = Math.floor(seconds / 60); seconds %= 60;
      output.textContent = document.documentElement.dataset.language === 'en'
        ? days + 'd ' + String(hours).padStart(2,'0') + 'h ' + String(minutes).padStart(2,'0') + 'm ' + String(seconds).padStart(2,'0') + 's'
        : days + 'д ' + String(hours).padStart(2,'0') + 'ч ' + String(minutes).padStart(2,'0') + 'м ' + String(seconds).padStart(2,'0') + 'с';
    }
    tick();
    window.setInterval(tick, 1000);

    const storageKey = ${JSON.stringify(`fh6-season-progress:${state.season.seriesSlug}:${state.season.season}:${state.season.startAt}`)};
    const activityKinds = ${activityKindsJson};
    const cards = [...document.querySelectorAll('[data-activity-block]')];
    const progress = document.getElementById('completion-progress');
    const filter = document.getElementById('completion-filter');
    const activityToc = document.getElementById('activity-toc-details');
    const activityTocNav = document.getElementById('activity-toc-nav');
    const languageButtons = [...document.querySelectorAll('[data-language-button]')];
    const communityStatus = document.getElementById('community-status');
    const feedbackDialog = document.getElementById('feedback-dialog');
    const feedbackLanguage = document.getElementById('feedback-language');
    const feedbackActivity = document.getElementById('feedback-activity');
    const feedbackComment = document.getElementById('feedback-comment');
    const continueFeedbackLink = document.getElementById('continue-feedback-link');
    const originalCards = new Map(cards.map((section) => [section.id, {
      title: section.querySelector('[data-card-title]')?.textContent ?? '',
      points: section.querySelector('[data-card-points]')?.textContent ?? '',
      kind: section.querySelector('[data-card-kind]')?.textContent ?? '',
      conditionHtml: section.querySelector('[data-card-condition-text]')?.innerHTML ?? '',
      howHtml: section.querySelector('[data-card-how-text]')?.innerHTML ?? '',
      tuneHtml: section.querySelector('[data-card-tune-text]')?.innerHTML ?? '',
      sources: section.querySelector('[data-card-sources]')?.innerHTML ?? ''
    }]));
    let currentLanguage = 'ru';
    let complete = new Set();
    try { complete = new Set(JSON.parse(localStorage.getItem(storageKey) || '[]')); } catch { complete = new Set(); }
    const save = () => localStorage.setItem(storageKey, JSON.stringify([...complete]));
    const renderProgress = () => {
      for (const section of cards) {
        const id = section.id;
        const done = complete.has(id);
        section.classList.toggle('is-complete', done);
        const button = section.querySelector('[data-completion-toggle]');
        if (button) button.setAttribute('aria-pressed', String(done));
      }
      progress.textContent = labels[currentLanguage].complete + ': ' + complete.size + '/${expectedCardCount}';
      document.documentElement.classList.toggle('hide-completed', Boolean(filter.checked));
    };
    const setText = (id, text) => { const node = document.getElementById(id); if (node) node.textContent = text; };
    const formatPiBadges = (root) => {
      if (!root) return;
      const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
      const textNodes = [];
      while (walker.nextNode()) {
        const node = walker.currentNode;
        if (!node.parentElement?.closest('.pi-badge')) textNodes.push(node);
      }
      const pattern = /\\b(D|C|B|A|S1|S2|R|X)\\s+(\\d{3})\\b/g;
      for (const node of textNodes) {
        const text = node.nodeValue ?? '';
        pattern.lastIndex = 0;
        if (!pattern.test(text)) continue;
        pattern.lastIndex = 0;
        const fragment = document.createDocumentFragment();
        let cursor = 0;
        for (const match of text.matchAll(pattern)) {
          fragment.append(document.createTextNode(text.slice(cursor, match.index)));
          const badge = document.createElement('span');
          badge.className = 'pi-badge pi-' + match[1].toLowerCase();
          badge.title = 'Class ' + match[1] + ', PI ' + match[2];
          const classLabel = document.createElement('span');
          classLabel.className = 'pi-class';
          classLabel.textContent = match[1];
          const score = document.createElement('span');
          score.className = 'pi-score';
          score.textContent = match[2];
          badge.append(classLabel, score);
          fragment.append(badge);
          cursor = match.index + match[0].length;
        }
        fragment.append(document.createTextNode(text.slice(cursor)));
        node.replaceWith(fragment);
      }
    };
    const formatShareCodes = (root) => {
      const walker = document.createTreeWalker(root, NodeFilter.SHOW_TEXT);
      const textNodes = [];
      while (walker.nextNode()) {
        const node = walker.currentNode;
        if (!node.parentElement?.closest('code, a, .share-code')) textNodes.push(node);
      }
      const pattern = /(?<!\\d)(\\d{3}(?:[ -]?\\d{3}){2})(?!\\d)/g;
      for (const node of textNodes) {
        const text = node.nodeValue ?? '';
        pattern.lastIndex = 0;
        if (!pattern.test(text)) continue;
        pattern.lastIndex = 0;
        const fragment = document.createDocumentFragment();
        let cursor = 0;
        for (const match of text.matchAll(pattern)) {
          fragment.append(document.createTextNode(text.slice(cursor, match.index)));
          const digits = match[1].replace(/\\D/g, '');
          const code = document.createElement('code');
          code.textContent = digits.replace(/(\\d{3})(?=\\d)/g, '$1 ');
          const wrapper = document.createElement('span');
          wrapper.className = 'share-code';
          wrapper.append(code);
          fragment.append(wrapper);
          cursor = match.index + match[0].length;
        }
        fragment.append(document.createTextNode(text.slice(cursor)));
        node.replaceWith(fragment);
      }
    };
    const applyLanguage = (requestedLanguage) => {
      currentLanguage = requestedLanguage === 'en' ? 'en' : 'ru';
      const copy = labels[currentLanguage];
      const translatedActivities = currentLanguage === 'en' ? englishLocale.activities : null;
      document.documentElement.lang = currentLanguage;
      document.documentElement.dataset.language = currentLanguage;
      document.title = currentLanguage === 'en' ? englishLocale.reportTitle : ${JSON.stringify(title)};
      setText('report-title', document.title);
      setText('language-switch-label', copy.language);
      setText('countdown-label', copy.countdown);
      setText('updated-label', copy.updated);
      setText('completion-filter-label', copy.unfinished);
      setText('support-title', copy.supportTitle);
      setText('support-description', copy.supportDescription);
      setText('support-sber-button', copy.supportSberButton);
      setText('support-boosty-button', copy.supportBoostyButton);
      setText('analytics-title', copy.analyticsTitle);
      setText('analytics-description', copy.analyticsDescription);
      setText('steam-guide-link', copy.steamGuide);
      setText('activity-toc-summary', copy.toc);
      setText('community-title', copy.communityTitle);
      setText('community-description', copy.communityDescription);
      setText('share-guide-button', copy.shareGuide);
      setText('open-feedback-button', copy.feedbackOpen);
      setText('steam-discussion-link', copy.steamDiscussion);
      setText('feedback-dialog-title', copy.feedbackDialogTitle);
      setText('feedback-language-label', copy.feedbackLanguage);
      setText('feedback-language-ru', copy.feedbackLanguageRu);
      setText('feedback-language-en', copy.feedbackLanguageEn);
      setText('feedback-activity-label', copy.feedbackActivity);
      setText('feedback-comment-label', copy.feedbackComment);
      setText('feedback-privacy', copy.feedbackPrivacy);
      setText('cancel-feedback-button', copy.feedbackCancel);
      setText('continue-feedback-link', copy.feedbackContinue);
      const guideOption = feedbackActivity?.querySelector('option[value="__guide__"]');
      if (guideOption) guideOption.textContent = copy.feedbackWholeGuide;
      for (const option of feedbackActivity?.querySelectorAll('option[data-title-ru]') ?? []) {
        const title = option.dataset[currentLanguage === 'en' ? 'titleEn' : 'titleRu'];
        if (title) option.textContent = option.dataset.number + ' · ' + title;
      }
      activityTocNav?.setAttribute('aria-label', currentLanguage === 'en' ? 'Activity navigation' : 'Навигация по активностям');
      document.getElementById('publication-chart-legend')?.setAttribute('aria-label', currentLanguage === 'en' ? 'Chart legend' : 'Легенда графика');
      for (const link of document.querySelectorAll('[data-toc-title]')) {
        const title = link.dataset[currentLanguage === 'en' ? 'tocTitleEn' : 'tocTitleRu'];
        if (title) link.textContent = title;
      }
      setText('publication-chart-title', currentLanguage === 'en' ? 'Audience trend' : chart.title);
      setText('publication-chart-subtitle', currentLanguage === 'en'
        ? 'Steam shows unique guide visitors. GitHub shows hits counted on this page, not unique visitors; repeat loads and bots may increase the total.'
        : 'Steam показывает уникальных посетителей руководства. GitHub — срабатывания счётчика страницы, а не уникальных посетителей; повторы и боты могут увеличить итог.');
      setText('chart-legend-github', (currentLanguage === 'en' ? 'GitHub page hits · ' : 'GitHub · ') + new Intl.NumberFormat(currentLanguage === 'en' ? 'en-US' : 'ru-RU').format(chart.githubViews));
      setText('chart-legend-steam', (currentLanguage === 'en' ? 'Steam unique visitors · ' : 'Steam · ') + new Intl.NumberFormat(currentLanguage === 'en' ? 'en-US' : 'ru-RU').format(chart.steamViews));
      setText('publication-chart-note', currentLanguage === 'en'
        ? 'Latest measurement: ' + chart.latestDate + ' · Steam favorites: ' + chart.favorites + '. Values are recorded after successful public verification.'
        : 'Последний замер: ' + chart.latestDate + ' · Steam в избранном: ' + chart.favorites + '. Значения фиксируются после успешной публичной проверки.');
      document.getElementById('publication-chart-svg')?.setAttribute('aria-label', currentLanguage === 'en'
        ? 'Steam unique guide visitors: ' + chart.steamViews + '; GitHub page-counter hits, not unique visitors: ' + chart.githubViews + '; latest measurement ' + chart.latestDate
        : 'Уникальные посетители Steam: ' + chart.steamViews + '; срабатывания счётчика страницы GitHub, не уникальные посетители: ' + chart.githubViews + '; последний замер ' + chart.latestDate);
      document.getElementById('analytics-link')?.setAttribute('aria-label', copy.analyticsLink);
      document.getElementById('analytics-badge')?.setAttribute('alt', copy.analyticsImage);
      for (const button of languageButtons) button.setAttribute('aria-pressed', String(button.dataset.languageButton === currentLanguage));
      for (const section of cards) {
        const original = originalCards.get(section.id);
        const translated = translatedActivities?.[section.id];
        section.querySelector('[data-card-title]')?.replaceChildren(document.createTextNode(translated?.title ?? original.title));
        section.querySelector('[data-card-points]')?.replaceChildren(document.createTextNode(translated?.points ?? original.points));
        const kind = section.querySelector('[data-card-kind]');
        if (kind) kind.textContent = readableKind(activityKinds[section.id], currentLanguage);
        const condition = section.querySelector('[data-card-condition-text]'); if (condition) { condition.innerHTML = translated?.conditionHtml ?? original.conditionHtml; formatPiBadges(condition); }
        const how = section.querySelector('[data-card-how-text]'); if (how) { how.innerHTML = translated?.howHtml ?? original.howHtml; formatPiBadges(how); }
        const tune = section.querySelector('[data-card-tune-text]'); if (tune) { tune.innerHTML = translated?.tuneHtml ?? original.tuneHtml; formatPiBadges(tune); formatShareCodes(tune); }
        const sources = section.querySelector('[data-card-sources]');
        if (sources) {
          sources.innerHTML = original.sources;
          if (currentLanguage === 'en') for (const link of sources.querySelectorAll('a')) link.textContent = sourceLabels[link.textContent] ?? link.textContent;
        }
        for (const [selector, label] of [['condition', copy.condition], ['how', copy.how], ['tune', copy.tune]]) {
          const node = section.querySelector('[data-card-label="' + selector + '"]'); if (node) node.textContent = label;
        }
        for (const chip of section.querySelectorAll('.provenance-chip')) {
          chip.dataset.russianText ||= chip.textContent;
          chip.textContent = currentLanguage === 'en' ? (provenanceLabels[chip.dataset.russianText] ?? chip.dataset.russianText) : chip.dataset.russianText;
        }
      }
      try { localStorage.setItem(languageStorageKey, currentLanguage); } catch {}
      tick();
      renderProgress();
    };
    for (const section of cards) {
      section.querySelector('[data-completion-toggle]')?.addEventListener('click', () => {
        const id = section.id;
        if (complete.has(id)) complete.delete(id); else complete.add(id);
        save(); renderProgress();
      });
    }
    filter.addEventListener('change', renderProgress);
    for (const button of languageButtons) button.addEventListener('click', () => applyLanguage(button.dataset.languageButton));
    const tocViewport = window.matchMedia('(max-width: 760px)');
    const syncTocDisclosure = () => { if (activityToc) activityToc.open = !tocViewport.matches; };
    syncTocDisclosure();
    tocViewport.addEventListener?.('change', syncTocDisclosure);
    for (const link of document.querySelectorAll('.activity-nav-link')) {
      link.addEventListener('click', () => { if (tocViewport.matches && activityToc) activityToc.open = false; });
    }
    let savedLanguage = 'ru';
    try { savedLanguage = localStorage.getItem(languageStorageKey) || 'ru'; } catch {}
    const sharedLanguage = new URL(window.location.href).searchParams.get('lang');
    if (sharedLanguage === 'ru' || sharedLanguage === 'en') savedLanguage = sharedLanguage;
    applyLanguage(savedLanguage);
    const reportUrlForLanguage = (language) => {
      const url = new URL(window.location.href);
      url.searchParams.set('lang', language);
      return url.toString();
    };
    document.getElementById('share-guide-button')?.addEventListener('click', async () => {
      const language = document.documentElement.dataset.language === 'en' ? 'en' : 'ru';
      const shareData = { title: document.title, text: language === 'en' ? 'Forza Horizon 6 Festival Playlist guide' : 'Сводка Festival Playlist Forza Horizon 6', url: reportUrlForLanguage(language) };
      if (window.matchMedia('(max-width: 760px)').matches && typeof navigator.share === 'function') {
        try { await navigator.share(shareData); } catch (error) { if (error?.name !== 'AbortError') communityStatus.textContent = labels[language].shareFailed; }
        return;
      }
      try {
        if (navigator.clipboard?.writeText) await navigator.clipboard.writeText(shareData.url);
        else {
          const helper = document.createElement('textarea'); helper.value = shareData.url; helper.setAttribute('readonly', ''); helper.style.position = 'fixed'; helper.style.opacity = '0'; document.body.append(helper); helper.select();
          const copied = document.execCommand('copy'); helper.remove(); if (!copied) throw new Error('clipboard unavailable');
        }
        communityStatus.textContent = labels[language].shareCopied;
      } catch { communityStatus.textContent = labels[language].shareFailed; }
    });
    document.getElementById('open-feedback-button')?.addEventListener('click', () => {
      feedbackLanguage.value = document.documentElement.dataset.language === 'en' ? 'en' : 'ru';
      feedbackDialog.showModal(); feedbackActivity.focus();
    });
    document.getElementById('cancel-feedback-button')?.addEventListener('click', () => feedbackDialog.close());
    feedbackDialog?.addEventListener('click', (event) => { if (event.target === feedbackDialog) feedbackDialog.close(); });
    continueFeedbackLink?.addEventListener('click', (event) => {
      const comment = feedbackComment.value.trim();
      if (!comment) { event.preventDefault(); feedbackComment.setAttribute('aria-invalid', 'true'); feedbackComment.focus(); communityStatus.textContent = labels[document.documentElement.dataset.language === 'en' ? 'en' : 'ru'].feedbackCommentRequired; return; }
      feedbackComment.removeAttribute('aria-invalid');
      const currentLanguage = feedbackLanguage.value === 'en' ? 'en' : 'ru';
      const selected = feedbackActivity.selectedOptions[0];
      const activity = selected.value === '__guide__' ? labels[currentLanguage].feedbackWholeGuide : selected.dataset[currentLanguage === 'en' ? 'titleEn' : 'titleRu'];
      const copy = labels[currentLanguage];
      const issueUrl = new URL(${JSON.stringify(community.feedbackUrl)});
      issueUrl.searchParams.set('title', copy.feedbackIssueTitle + ': ' + activity);
      issueUrl.searchParams.set('body', '**' + copy.feedbackIssueBody + ':** ' + (currentLanguage === 'en' ? 'English' : 'Русский') + '\\n**' + copy.feedbackIssueActivity + ':** ' + activity + '\\n**' + copy.feedbackIssueReport + ':** ' + reportUrlForLanguage(currentLanguage) + '\\n\\n**' + copy.feedbackIssueComment + ':**\\n' + comment + '\\n\\n_' + copy.feedbackIssuePrivacy + '_');
      continueFeedbackLink.href = issueUrl.toString();
      feedbackDialog.close();
    });
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

const outputBytes = Buffer.byteLength(html, 'utf8');
if (outputBytes > maxPublicHtmlBytes) throw new Error(`Lightweight report is unexpectedly large: ${outputBytes} bytes`);
if ((html.match(/<section class="activity-block"[^>]*\bdata-activity-block\b/g) ?? []).length !== expectedCardCount) throw new Error('Lightweight report lost activity blocks');
if ((html.match(/<section class="support-section"[^>]*\bdata-support-block\b/g) ?? []).length !== 1 || !html.includes(support.url) || !html.includes(support.boosty.url) || !html.includes(supportQrSrc)) {
  throw new Error('Lightweight report lost the configured support block');
}
if ((html.match(/<div class="visit-stats"[^>]*\bdata-visit-stats\b/g) ?? []).length !== 1 || !html.includes(escapeHtml(analytics.counterImageUrl)) || !html.includes(escapeHtml(analytics.dashboardUrl))) {
  throw new Error('Lightweight report lost the configured visit statistics');
}
if ((html.match(/<section class="publication-chart"[^>]*\bdata-publication-chart\b/g) ?? []).length !== 1 || !html.includes('Динамика аудитории')) {
  throw new Error('Lightweight report lost the native publication-history chart');
}
if ((html.match(/<a class="steam-guide-link"[^>]*\bdata-steam-guide-link\b/g) ?? []).length !== 1 || !html.includes(escapeHtml(steamGuide.url)) || html.indexOf('data-steam-guide-link') < html.indexOf('data-publication-chart')) {
  throw new Error('Lightweight report lost the Steam guide link after the audience chart');
}
for (const asset of [faviconPngSrc, appleTouchIconSrc]) {
  if (!html.includes(asset)) throw new Error(`Lightweight report lost branding asset: ${asset}`);
}
if (html.includes('<iframe') || html.includes('data:image/') || html.includes('data-analytics-portable-reader')) {
  throw new Error('Lightweight report still contains a heavy portable runtime or embedded images');
}

writeFileWithRetry(htmlPath, html);
console.log(`Built lightweight ${htmlPath}: ${outputBytes} bytes, ${expectedCardCount} cards, 0 iframes`);
