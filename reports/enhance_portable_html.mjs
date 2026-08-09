import fs from 'node:fs';
import path from 'node:path';
import { fileURLToPath } from 'node:url';

const reportDir = path.dirname(fileURLToPath(import.meta.url));
const htmlPath = path.join(reportDir, 'current-week.html');
const artifactPath = path.join(reportDir, 'artifact.json');
const beginMarker = '<!-- FH6_LIVE_META_BEGIN -->';
const endMarker = '<!-- FH6_LIVE_META_END -->';

const artifact = JSON.parse(fs.readFileSync(artifactPath, 'utf8'));
const generatedAt = artifact?.snapshot?.generatedAt ?? artifact?.manifest?.generatedAt;
if (!generatedAt || Number.isNaN(Date.parse(generatedAt))) {
  throw new Error('artifact.json does not contain a valid generatedAt timestamp');
}

let html = fs.readFileSync(htmlPath, 'utf8');
const oldStart = html.indexOf(beginMarker);
if (oldStart >= 0) {
  const oldEnd = html.indexOf(endMarker, oldStart);
  if (oldEnd < 0) throw new Error('Found an incomplete FH6 live metadata block');
  html = html.slice(0, oldStart) + html.slice(oldEnd + endMarker.length);
}

const enhancement = `${beginMarker}
<style id="fh6-live-meta-style">
  .fh6-live-countdown{display:inline-flex;align-items:center;white-space:nowrap;border:1px solid color-mix(in srgb,currentColor 22%,transparent);border-radius:999px;padding:6px 11px;font-size:12px;font-weight:750;letter-spacing:.01em}
  .fh6-live-countdown strong{margin-left:5px;color:#86a900;font-variant-numeric:tabular-nums}
  .analytics-top-bar-actions .fh6-live-countdown{margin-right:8px}
  .portable-page-meta{display:flex;align-items:flex-end;gap:8px;flex-direction:column}
  .portable-updated-label{font-size:12px;white-space:nowrap}
  @media(max-width:760px){.analytics-top-bar-actions .fh6-live-countdown{font-size:10px;padding:5px 8px}.analytics-reader-freshness .top-bar-refresh-text{max-width:120px;overflow:hidden;text-overflow:ellipsis;white-space:nowrap}.portable-page-header{gap:12px}.portable-page-meta{align-items:flex-start}}
</style>
<script id="fh6-live-meta-script">
(() => {
  const generatedAt = ${JSON.stringify(generatedAt)};
  const updatedText = 'Обновлено: ' + new Intl.DateTimeFormat('ru-RU', {
    timeZone: 'Asia/Krasnoyarsk', day: '2-digit', month: '2-digit', year: 'numeric',
    hour: '2-digit', minute: '2-digit'
  }).format(new Date(generatedAt));
  const krasnoyarskOffsetMs = 7 * 60 * 60 * 1000;

  function nextThursdayDeadline(nowMs) {
    const local = new Date(nowMs + krasnoyarskOffsetMs);
    const weekday = local.getUTCDay();
    let daysAhead = (4 - weekday + 7) % 7;
    let targetLocal = Date.UTC(
      local.getUTCFullYear(), local.getUTCMonth(), local.getUTCDate() + daysAhead, 21, 30, 0
    );
    if (targetLocal <= local.getTime()) {
      daysAhead += 7;
      targetLocal = Date.UTC(
        local.getUTCFullYear(), local.getUTCMonth(), local.getUTCDate() + daysAhead, 21, 30, 0
      );
    }
    return targetLocal - krasnoyarskOffsetMs;
  }

  function countdownText(nowMs) {
    let seconds = Math.max(0, Math.floor((nextThursdayDeadline(nowMs) - nowMs) / 1000));
    const days = Math.floor(seconds / 86400); seconds %= 86400;
    const hours = Math.floor(seconds / 3600); seconds %= 3600;
    const minutes = Math.floor(seconds / 60); seconds %= 60;
    return days + 'д ' + String(hours).padStart(2, '0') + 'ч ' +
      String(minutes).padStart(2, '0') + 'м ' + String(seconds).padStart(2, '0') + 'с';
  }

  function createCountdown(id) {
    const node = document.createElement('span');
    node.id = id;
    node.className = 'fh6-live-countdown';
    node.innerHTML = 'Заканчивается через <strong data-fh6-countdown></strong>';
    return node;
  }

  function decorate() {
    const fallbackMeta = document.querySelector('.portable-page-meta');
    if (fallbackMeta && !fallbackMeta.querySelector('.portable-updated-label')) {
      const time = fallbackMeta.querySelector('time');
      if (time) {
        time.textContent = updatedText;
        time.classList.add('portable-updated-label');
      }
      fallbackMeta.prepend(createCountdown('fh6-live-countdown-fallback'));
    }

    const readerFreshness = document.querySelector('.analytics-reader-freshness .top-bar-refresh-text');
    if (readerFreshness && readerFreshness.textContent !== updatedText) {
      readerFreshness.textContent = updatedText;
    }
    const actions = document.querySelector('.analytics-top-bar-actions');
    if (actions && !document.getElementById('fh6-live-countdown-reader')) {
      actions.prepend(createCountdown('fh6-live-countdown-reader'));
    }
  }

  function tick() {
    const value = countdownText(Date.now());
    document.querySelectorAll('[data-fh6-countdown]').forEach((node) => { node.textContent = value; });
  }

  decorate();
  tick();
  const observer = new MutationObserver(() => { decorate(); tick(); });
  observer.observe(document.documentElement, { childList: true, subtree: true });
  window.setInterval(tick, 1000);
})();
</script>
${endMarker}`;

if (!html.includes('</body>')) throw new Error('Portable HTML has no closing body tag');
html = html.replace('</body>', `${enhancement}\n</body>`);
fs.writeFileSync(htmlPath, html, 'utf8');

if (!html.includes('Заканчивается через') || !html.includes('Обновлено: ')) {
  throw new Error('Live metadata enhancement verification failed');
}
console.log(`Enhanced ${htmlPath} with a live Thursday 21:30 Asia/Krasnoyarsk countdown`);
