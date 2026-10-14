"""Durable manual request receipts; project only safe guard status fields."""
import time
import uuid
import re
from pathlib import Path
import phone_tasks

STAGES={'audit':'Проверка источников и изображений','structure':'Проверка структуры сезона','html':'Подготовка страниц','markdown':'Подготовка отчёта','portable':'Сборка сайта','artifact':'Артефакт сайта','timestamp':'Время обновления','browser_qa':'Проверка отображения','publish':'Публикация сайта','steam_check':'Проверка Steam','steam_render':'Подготовка текстов Steam','preflight':'Предварительная проверка','rollover_preflight':'Проверка границ сезона','visual_queue':'Проверка изображений','ha_receipt':'Подтверждение уведомления','metrics':'Сбор показателей','notification':'Доставка уведомления'}

def directory(store):
    p=store/'refresh-history'
    if p.is_symlink():raise ValueError('Недопустимый каталог истории.')
    p.mkdir(mode=0o750,exist_ok=True)
    if __import__('os').geteuid()==0:
        import os,pwd
        u=pwd.getpwnam('fh6');os.chown(p,u.pw_uid,u.pw_gid)
    return p

def records(store):
    base=store/'refresh-history'
    if not base.is_dir() or base.is_symlink():return []
    files=sorted((p for p in base.glob('*.json') if not p.is_symlink()),reverse=True)[:20]
    rows=[phone_tasks.read(p) for p in files]
    return [r for r in rows if re.fullmatch(r'[0-9]+-[a-f0-9]{32}',str(r.get('id','')))]

def accept(store):
    rows=records(store)
    if rows and not rows[0].get('runId') and rows[0].get('status')=='ACCEPTED' and time.time()-rows[0].get('acceptedAt',0)<3600:
        raise ValueError('Запрос уже принят. Его состояние показано под кнопкой.')
    row={'id':str(time.time_ns())+'-'+uuid.uuid4().hex,'acceptedAt':time.time(),'status':'ACCEPTED'}
    phone_tasks.save(directory(store)/(row['id']+'.json'),row)
    return row

def bind(store,run_id):
    if not re.fullmatch(r'fh6-[0-9-]+',run_id):raise ValueError('Unexpected run identity')
    rows=records(store)
    if rows and rows[0].get('status')=='ACCEPTED' and not rows[0].get('runId'):
        row=rows[0];row.update(runId=run_id,status='STARTED',workerStartedAt=time.time())
        phone_tasks.save(directory(store)/(row['id']+'.json'),row)

def failed(store,row):
    row['status']='FAILED_TO_QUEUE'
    phone_tasks.save(directory(store)/(row['id']+'.json'),row)

def snapshot(root,store):
    out=[]
    for row in records(store)[:5]:
        r={k:row.get(k) for k in ('id','acceptedAt','runId','workerStartedAt')}
        run_id=row.get('runId','')
        run={}
        if re.fullmatch(r'fh6-[0-9-]+',run_id):
            file=root/'automation/runs/refresh'/run_id/'run.json'
            if file.is_file() and not file.is_symlink() and not file.parent.is_symlink():run=phone_tasks.read(file)
        status=run.get('status') if run.get('runId')==run_id else row.get('status')
        if status=='ACCEPTED' and time.time()-row.get('acceptedAt',0)>120:status='WAITING_FOR_WORKER'
        r.update(status=status,startedAt=run.get('startedAt'),finishedAt=run.get('finishedAt'))
        steps=run.get('steps',{})
        r['steps']={k:v.get('status') for k,v in steps.items() if k in STAGES and isinstance(v,dict)}
        r['siteVerified']=r['steps'].get('publish')=='passed'
        r['notificationReceived']=run.get('haReceipt')=='CONFIRMED'
        out.append(r)
    return out
