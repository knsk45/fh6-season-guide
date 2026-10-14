"""Readable private panel. Owner/model text is always escaped."""
import html
from datetime import datetime
from zoneinfo import ZoneInfo

def esc(value):return html.escape(str(value or ''))

def date(value):
    try:
        dt=datetime.fromtimestamp(value,ZoneInfo('Asia/Krasnoyarsk')) if isinstance(value,(int,float)) else datetime.fromisoformat(value)
        return '<time datetime="'+esc(dt.isoformat())+'">'+esc(dt.strftime('%d.%m.%Y · %H:%M'))+'</time>'
    except (ValueError,TypeError,OverflowError):return 'Ещё нет данных'

def badge(text,tone='neutral'):return '<span class="badge '+tone+'">'+esc(text)+'</span>'

def action(path,label,notice='',fields=''):
    return '<form class="action-form" method="post" action="'+path+'">'+fields+'<button type="submit">'+esc(label)+'</button><p class="action-message" role="status" aria-live="polite">'+esc(notice)+'</p></form>'

STYLE='''
.switch-label{display:flex;align-items:center;gap:14px;cursor:pointer}.switch-label input{position:absolute;opacity:0;width:48px;height:28px}.switch-track{pointer-events:none;position:relative;flex:0 0 48px;height:28px;border-radius:20px;background:#48556b}.switch-track:after{content:'';position:absolute;top:4px;left:4px;width:20px;height:20px;background:#fff;border-radius:50%;transition:transform .2s}.switch-label input:checked+.switch-track{background:#37b69c}.switch-label input:checked+.switch-track:after{transform:translateX(20px)}.switch-label input:focus-visible+.switch-track{outline:3px solid #8ad9ff;outline-offset:4px}
:root{color-scheme:dark;--bg:#0c1220;--card:#151e30;--line:#2b3850;--muted:#a7b6cc;--ink:#f4f7fc;--accent:#86e9df}*{box-sizing:border-box}body{margin:0;background:var(--bg);color:var(--ink);font:16px/1.55 system-ui,-apple-system,sans-serif}main{max-width:1080px;margin:auto;padding:28px 20px 72px}header{margin-bottom:26px}.eyebrow{color:var(--accent);font-size:12px;letter-spacing:.16em;text-transform:uppercase;font-weight:750}h1{font-size:clamp(28px,5vw,40px);line-height:1.15;margin:8px 0 12px}h2{font-size:22px;margin:0}h3{font-size:17px;margin:0 0 8px}p{margin:10px 0}a{color:var(--accent)}nav{display:flex;gap:10px;flex-wrap:wrap;margin-top:18px}nav a{padding:8px 14px;border:1px solid var(--line);border-radius:100px;text-decoration:none;font-size:14px}section.card{background:var(--card);border:1px solid var(--line);border-radius:20px;padding:24px;margin:18px 0;scroll-margin-top:20px}.section-head{display:flex;align-items:center;justify-content:space-between;gap:12px;margin-bottom:14px}.muted,.hint{color:var(--muted);font-size:14px}.grid{display:grid;grid-template-columns:repeat(3,minmax(0,1fr));gap:12px;margin:20px 0}.stat{border:1px solid var(--line);border-radius:14px;padding:16px}.stat strong{display:block;margin-bottom:8px}.badge{display:inline-block;border-radius:100px;padding:5px 11px;font-size:13px;font-weight:650;overflow-wrap:anywhere;background:#28344a;color:#d9e4f5}.good{background:#153d35;color:#9af0d3}.warn{background:#483821;color:#ffe0a0}.bad{background:#482833;color:#ffb7c5}.active{background:#17394f;color:#9bdcf9}.divider{height:1px;background:var(--line);margin:20px 0}button,.button{border:0;border-radius:12px;padding:13px 18px;min-height:48px;font:650 15px/1.4 system-ui;background:var(--accent);color:#09242a;cursor:pointer;white-space:normal}button.secondary{background:#26344c;color:var(--ink);border:1px solid #3b4c68}button:disabled{opacity:.55;cursor:default}button:focus-visible,summary:focus-visible,a:focus-visible,textarea:focus-visible{outline:3px solid #8ad9ff;outline-offset:4px}textarea{display:block;width:100%;font:inherit;color:var(--ink);background:#0e1625;border:1px solid #41516d;border-radius:12px;padding:14px;margin:10px 0 14px;resize:vertical}label{font-weight:650}form{margin:16px 0 0}.action-message{font-size:14px;min-height:0;color:var(--accent);overflow-wrap:anywhere}.action-message.error{color:#ffb7c5}.task{padding:16px;border:1px solid var(--line);border-radius:14px;margin-top:16px}.answer{white-space:pre-wrap;overflow-wrap:anywhere;font:inherit;border-left:3px solid var(--accent);padding:12px 16px;background:#10192a;border-radius:0 10px 10px 0;margin-top:14px}.task-title{display:flex;align-items:center;gap:10px;flex-wrap:wrap}.task .request{overflow-wrap:anywhere}details{border:1px solid var(--line);border-radius:12px;margin-top:14px;padding:12px 16px}summary{cursor:pointer;font-weight:650;min-height:32px;display:list-item}details[open] summary{margin-bottom:12px}.steam-row{display:flex;justify-content:space-between;align-items:center;gap:12px}.steam-block{padding:18px;border:1px solid var(--line);border-radius:14px;margin-top:14px}.steam-block details{border:0;padding:0}.steam-text{white-space:pre-wrap;overflow-wrap:anywhere;max-height:420px;overflow:auto;padding:16px;background:#0d1524;border-radius:10px;font:14px/1.65 ui-monospace,monospace}#notice{position:sticky;top:12px;z-index:2;border:1px solid #3f6c60;background:#153d35;border-radius:12px;padding:14px 18px;box-shadow:0 8px 30px #0004}#notice:empty{display:none}#notice.error{background:#482833;border-color:#8b4a5c}input[type=file]{max-width:100%;padding:12px 0}ul.checks{padding-left:20px;color:var(--muted)}.footer{color:var(--muted);font-size:13px;margin-top:26px}code{overflow-wrap:anywhere}#codex-code{white-space:pre-wrap;overflow-wrap:anywhere;background:#0e1625;border-radius:12px;padding:16px}@media(max-width:640px){main{padding:20px 14px 48px}section.card{padding:18px;border-radius:16px}.grid{grid-template-columns:1fr}.section-head{align-items:flex-start;flex-direction:column}.stat{display:flex;align-items:center;justify-content:space-between;gap:10px}.stat strong{margin:0}.steam-row{align-items:flex-start;flex-wrap:wrap}.steam-row button{flex:0 0 auto}form>button{width:100%}}
'''

SCRIPT='''
const notice=document.querySelector('#notice');
function announce(text,error=false){notice.textContent=text;notice.classList.toggle('error',error);}
function localDates(){document.querySelectorAll('time[datetime]').forEach(e=>{const d=new Date(e.dateTime);if(!isNaN(d))e.textContent=new Intl.DateTimeFormat('ru',{dateStyle:'medium',timeStyle:'short'}).format(d);});}localDates();
document.querySelectorAll('.action-form').forEach(form=>form.addEventListener('submit',async event=>{
 event.preventDefault();const button=form.querySelector('button[type=submit]');if(button.disabled)return;
 const original=button.textContent;const payload=new URLSearchParams(new FormData(form));if(form.action.endsWith('/consent'))form.querySelector('input[type=checkbox]').disabled=true;const message=form.querySelector('.action-message');button.disabled=true;button.textContent='Отправляем…';message.textContent='Запрос отправляется на сервер';message.classList.remove('error');
 try{const r=await fetch(form.action,{method:'POST',headers:{'X-FH6-UI':'1'},body:payload});const data=await r.json();message.textContent=data.message;message.classList.toggle('error',!r.ok);announce(data.message,!r.ok);
 if(!r.ok){if(form.action.endsWith('/consent'))form.querySelector('input[type=checkbox]').checked=!form.querySelector('input[type=checkbox]').checked;button.disabled=false;if(form.action.endsWith('/consent'))form.querySelector('input[type=checkbox]').disabled=false;button.textContent=original;return;}button.textContent='✓ Принято';sessionStorage.setItem('fh6-notice',data.message);
 if(data.anchor){setTimeout(()=>{location.assign('/#'+data.anchor);location.reload();},1200);}
 }catch{message.textContent='Не удалось получить ответ. Обновите страницу и проверьте статус перед повтором.';message.classList.add('error');announce(message.textContent,true);button.textContent='Проверьте статус';const retry=document.createElement('button');retry.type='button';retry.className='secondary';retry.textContent='Обновить статус';retry.addEventListener('click',()=>location.reload());message.after(retry);}
}));
const consent=document.querySelector('#steam-consent');if(consent){const form=consent.closest('form');form.querySelector('button').hidden=true;consent.addEventListener('change',()=>form.requestSubmit());}
const saved=sessionStorage.getItem('fh6-notice');if(saved){announce(saved);sessionStorage.removeItem('fh6-notice');}
document.querySelectorAll('[data-copy]').forEach(button=>button.addEventListener('click',async()=>{
 const source=document.getElementById(button.dataset.copy),message=button.closest('.steam-block').querySelector('.action-message');button.disabled=true;
 try{const text=source.textContent;if(navigator.clipboard?.writeText)await navigator.clipboard.writeText(text);else{const box=document.createElement('textarea');box.value=text;document.body.append(box);box.select();try{if(!document.execCommand('copy'))throw Error();}finally{box.remove();}}button.textContent='✓ Скопировано';message.classList.remove('error');message.textContent='Весь текст скопирован. Можно вставить в редактор Steam.';announce(message.textContent);}
 catch{source.closest('details').open=true;message.textContent='Браузер не разрешил копирование. Выделите текст в раскрытом блоке и скопируйте вручную.';message.classList.add('error');button.textContent='Повторить копирование';}
 finally{setTimeout(()=>{button.disabled=false;button.textContent='Скопировать текст';},2500);}
}));
const screens=document.querySelector('#screens'),uploadButton=document.querySelector('#upload-button'),uploadMessage=document.querySelector('#message');
screens.addEventListener('change',()=>{uploadButton.disabled=!screens.files.length;uploadMessage.textContent=screens.files.length?'Выбрано файлов: '+screens.files.length:'';});
uploadButton.addEventListener('click',async()=>{const files=[...screens.files];if(!files.length)return;uploadButton.disabled=true;screens.disabled=true;let done=0;
 try{for(const f of files){uploadButton.textContent='Загрузка '+(done+1)+' из '+files.length+'…';uploadMessage.textContent='Передаём '+f.name;const r=await fetch('/upload',{method:'POST',headers:{'Content-Type':'application/octet-stream','X-FH6-Request':'upload'},body:f});const text=await r.text();if(!r.ok)throw Error(text);done++;}screens.value='';uploadMessage.textContent='✓ Сохранено оригиналов: '+done+'. Они ожидают редакторской проверки.';announce(uploadMessage.textContent);}
 catch(e){uploadMessage.textContent='Сохранено '+done+' из '+files.length+'. '+e.message;announce(uploadMessage.textContent,true);}
 finally{screens.disabled=false;uploadButton.disabled=!screens.files.length;uploadButton.textContent='Загрузить скриншоты';}
});
async function poll(){if(document.hidden||document.querySelector('#task')?.value.trim()||screens?.files.length||document.querySelector('.action-form button:disabled'))return;try{const r=await fetch('/panel-status',{cache:'no-store'});if(!r.ok)return;const data=await r.json();if(JSON.stringify(data)!==JSON.stringify(initialPanel)){location.reload();}}catch{}}setInterval(poll,5000);
'''

def render(active,state,editor,recovery,auth,tasks,texts,sha,approval,queued,login_code='',signature=None,consent=None,steam_publication=None):
    status=active.get('status')
    labels={'RUNNING':('Обновление выполняется','active'),'BLOCKED':('Нужна проверка ошибки','bad'),
        'COMPLETED':('Обновление завершено','good'),'PENDING_CONFIRMATION':('Сайт обновлён · Steam ждёт разрешения','warn'),
        'AWAITING_DELIVERY':('Доставляем уведомление','active')}
    title,tone=labels.get(status,('Ожидаем первый запуск','neutral'))
    if status=='PENDING_CONFIRMATION' and (approval or (consent or {}).get('enabled')):
        title='Сайт обновлён · Steam ожидает публикации'
    if queued:title,tone='Проверка поставлена в очередь','active'
    published=active.get('steps',{}).get('publish',{})
    if isinstance(published,dict):published=published.get('status')
    site=badge('Обновлён','good') if published=='passed' else badge('В процессе','active') if status=='RUNNING' else badge('Нет подтверждения')
    notified=badge('Получено','good') if active.get('haReceipt')=='CONFIRMED' else badge('Отправлено','active') if active.get('notification') else badge('Ожидается')
    steam=badge('Тексты актуальны','good') if status=='COMPLETED' else badge('Разрешение сохранено','warn') if approval else badge('Нужно разрешение','warn') if status=='PENDING_CONFIRMATION' else badge('Проверяется') if status=='RUNNING' else badge('Нет данных')
    if (consent or {}).get('enabled') and status!='COMPLETED':steam=badge('Автосогласие включено','good')
    publication=steam_publication or {}
    publication_labels={'NEEDS_SETUP':('Нужна настройка браузера','warn'),
        'NEEDS_LOGIN':('Нужен вход в Steam','warn'),'STEAM_GUARD':('Подтвердите Steam Guard','warn'),
        'NEEDS_APPROVAL':('Нужно разрешение','warn'),'STALE_APPROVAL':('Нужно новое разрешение','warn'),
        'AUDIT_REQUIRED':('Нужна свежая проверка сезона','warn'),
        'PUBLISHING':('Публикуется','active'),'VERIFYING':('Проверяется публикация','active'),
        'UNCERTAIN':('Результат отправки уточняется','warn'),'BLOCKED':('Публикация остановлена','bad'),
        'COMPLETE':('Оба раздела опубликованы','good')}
    publication_status=publication.get('status')
    if publication_status=='COMPLETE' and publication.get('sha256')!=sha:publication_status=None
    if publication_status in publication_labels:
        label,t=publication_labels[publication_status];steam=badge(label,t)
        if publication_status=='COMPLETE' and status=='PENDING_CONFIRMATION':title,tone='Сайт и Steam обновлены','good'
    body='<!doctype html><html lang="ru"><meta charset="utf-8"><meta name="viewport" content="width=device-width,initial-scale=1"><title>FH6 · Панель сборщика</title><style>'+STYLE+'</style><main><header><div class="eyebrow">FH6 · управление проектом</div><h1>Панель сборщика</h1><p class="muted">Обновления, задачи и подготовка Steam — с телефона.</p><nav><a href="#overview">Обзор</a><a href="#tasks">Задачи</a><a href="#steam">Steam</a><a href="#screenshots">Скриншоты</a><a href="#codex">Вход в Codex</a></nav></header><div id="notice" role="status" aria-live="polite"></div>'
    body+='<section class="card" id="overview"><div class="section-head"><h2>Состояние проекта</h2>'+badge(title,tone)+'</div><p>'+esc(state.get('season',{}).get('reportTitle','Текущий сезон'))+'</p><p class="muted">Последнее обновление: '+date(state.get('lastContentUpdate'))+' · время вашего устройства</p><div class="grid"><div class="stat"><strong>Сайт</strong>'+site+'</div><div class="stat"><strong>Steam</strong>'+steam+'</div><div class="stat"><strong>Уведомление</strong>'+notified+'</div></div>'
    recovery_labels={'WAITING':'Автовосстановление запланировало повтор.', 'QUEUED':'Автовосстановление запускает повтор.', 'NEEDS_LOGIN':'Для продолжения войдите в Codex ниже.', 'NEEDS_REVIEW':'Нужна проверка причины ошибки.', 'LIMIT_REACHED':'Лимит повторов на сегодня исчерпан.'}
    if recovery.get('runId')==active.get('runId') and recovery.get('status') in recovery_labels:
        body+='<p>'+recovery_labels[recovery['status']]+'</p>'
        if recovery.get('nextAttemptAt'):body+='<p class="muted">Следующая попытка: '+date(recovery['nextAttemptAt'])+'</p>'
    if status=='RUNNING':body+='<p class="hint">Сборщик проверяет источники и готовит обновление. Статус обновляется автоматически.</p>'
    if status in {'RUNNING'} or queued:body+='<button disabled>Проверка '+('выполняется' if status=='RUNNING' else 'в очереди')+'</button>'
    else:body+=action('/refresh','Проверить и обновить сейчас','Запустит полную проверку сезона. Steam потребует отдельного разрешения.')
    body+='</section><section class="card" id="tasks"><div class="section-head"><h2>Задачи для Codex</h2>'+badge('Отдельная рабочая копия')+'</div><p class="hint">Опишите задачу. Ответ появится здесь. Подготовленные изменения устанавливаются отдельно.</p>'
    busy=any(t.get('status') in {'QUEUED','RUNNING'} for t in tasks)
    if busy:body+='<p class="hint">Дождитесь завершения текущей задачи перед отправкой следующей.</p>'
    else:body+=action('/task','Отправить задачу','До 2000 символов. Не вставляйте пароли или токены.','<label for="task">Что нужно сделать?</label><textarea id="task" name="task" rows="4" maxlength="2000" required placeholder="Например: проверь, что требуется для обновления Steam"></textarea>')
    task_labels={'QUEUED':('В очереди','active'),'RUNNING':('Выполняется','active'),'FINISHED':('Готово','good'),'FAILED':('Ошибка','bad'),'TIMED_OUT':('Превышено время','bad'),'NEEDS_LOGIN':('Нужен вход','warn'),'INTERRUPTED':('Прервано','warn')}
    for i,task in enumerate(tasks):
        if i==1:body+='<details><summary>Предыдущие задачи ('+str(len(tasks)-1)+')</summary>'
        label,t=task_labels.get(task.get('status'),('Статус неизвестен','neutral'))
        body+='<article class="task"><div class="task-title">'+badge(label,t)+'<span class="muted">'+date(task.get('createdAt'))+'</span></div><p class="request">'+esc(task.get('task'))+'</p>'
        if task.get('status')=='FINISHED':body+='<p class="hint">Предложение подготовлено. Изменения ещё не установлены.</p>'
        if task.get('result'):body+='<div class="answer">'+esc(task['result'])+'</div>'
        body+='</article>'
    if len(tasks)>1:body+='</details>'
    if not tasks:body+='<p class="hint">Пока нет задач. Отправьте первую выше.</p>'
    body+='</section><section class="card" id="steam"><div class="section-head"><h2>Обновление Steam</h2>'+steam+'</div><p class="hint">Подготовлены русский и английский тексты. Откройте для проверки или скопируйте целиком.</p>'
    if publication_status=='NEEDS_SETUP':body+='<p class="hint">Обработчик подготовлен. До настройки серверного браузера публикация выключена.</p>'
    if publication_status in {'NEEDS_LOGIN','STEAM_GUARD'}:body+='<p class="hint">Войдите в выделенном серверном браузере и подтвердите вход. Пароль и коды не вводите в панели или чате.</p>'
    if publication_status=='UNCERTAIN':body+='<p class="hint">Не запускайте отправку повторно вручную: сначала нужна проверка публичного результата.</p>'
    enabled=(consent or {}).get('enabled') is True
    body+=action('/consent','Сохранить настройку','Включение разрешает заменять оба текста во всех следующих обновлениях. Выключение отзывает автоматические разрешения.',
                 '<label class="switch-label"><input id="steam-consent" type="checkbox" role="switch" name="enabled" value="true" '+('checked' if enabled else '')+'><span class="switch-track" aria-hidden="true"></span><span>Постоянное согласие на обновление Steam</span></label><p class="hint">'+('Включено — согласие действует и на будущие тексты.' if enabled else 'Выключено — каждую пару текстов нужно разрешать отдельно.')+'</p>')
    for locale,label in [('ru','Русский'),('en','English')]:
        body+='<div class="steam-block"><div class="steam-row"><h3>'+label+'</h3><button class="secondary" type="button" data-copy="steam-'+locale+'">Скопировать текст</button></div><details><summary>Показать текст · '+str(len(texts[locale]))+' символов</summary><pre class="steam-text" id="steam-'+locale+'">'+esc(texts[locale])+'</pre></details><p class="action-message" role="status" aria-live="polite"></p></div>'
    if enabled:body+='<p class="action-message">Постоянное согласие активно. Сборщик сохранит разрешение на проверенные тексты автоматически.</p>'
    elif approval:body+='<p class="action-message">✓ Разрешение на эти два текста сохранено. Ожидается публикация.</p><button disabled>Разрешение сохранено</button>'
    else:body+=action('/approve','Разрешить обновление двух текстов','Разрешение сохраняется для текущих текстов. Само нажатие пока не публикует их в Steam.','<input type="hidden" name="sha" value="'+esc(sha)+'">')
    body+='<p class="hint">Публикация пока требует отдельного входа владельца в Steam и проверки результата.</p></section><section class="card" id="screenshots"><div class="section-head"><h2>Игровые скриншоты</h2>'+badge('Оригиналы')+'</div><p class="hint">Передайте полные игровые плитки. Сборщик сохранит файлы без изменений для проверки.</p><label for="screens">Выберите изображения</label><br><input id="screens" type="file" accept="image/png,image/jpeg,image/webp" multiple><br><button id="upload-button" type="button" disabled>Загрузить скриншоты</button><p id="message" class="action-message" role="status" aria-live="polite"></p></section>'
    auth_labels={'CONNECTED':('Codex подключён','good'),'IDLE':('Нужен вход','warn'),'QUEUED':('Вход в очереди','active'),'STARTING':('Запускаем вход','active'),'WAITING_FOR_OWNER':('Подтвердите вход','warn'),'FAILED':('Ошибка входа','bad'),'EXPIRED':('Код истёк','warn')}
    label,t=auth_labels.get(auth['status'],('Проверьте вход','warn'))
    body+='<section class="card" id="codex"><div class="section-head"><h2>Подключение Codex</h2>'+badge(label,t)+'</div><p id="codex-status">'+('Авторизация на сервере подтверждена. Можно отправлять задачи.' if auth['status']=='CONNECTED' else 'Подключите свой аккаунт OpenAI, чтобы серверный Codex мог выполнять задачи.')+'</p>'
    if auth['status']!='CONNECTED':
        if auth['status'] not in {'QUEUED','STARTING','WAITING_FOR_OWNER'}:body+=action('/login','Получить код входа')
        body+='<p><a href="https://auth.openai.com/codex/device" target="_blank" rel="noopener noreferrer">Открыть страницу входа OpenAI ↗</a></p><p class="hint">Код вводите на странице OpenAI. Пароль и код не отправляйте в чат.</p>'
        if login_code:body+='<pre id="codex-code">'+esc(login_code)+'</pre>'
    body+='</section><p class="footer">Панель защищена паролем. Статусы обновляются автоматически каждые 5 секунд.</p></main>'
    import json
    body+='<script>const initialPanel='+json.dumps(signature or {},ensure_ascii=True)+';'+SCRIPT+'</script></html>'
    return body
