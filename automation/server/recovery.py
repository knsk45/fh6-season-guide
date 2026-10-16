"""Bounded recovery of transient failures. Never takes commands from logs."""
from datetime import datetime, timedelta
import json
from pathlib import Path
import re
import subprocess
import sys

import runner
from refresh_guard import atomic, exclusive, now, read

DELAYS=(300,900,3600)
UNITS=('fh6-refresh.service','fh6-manual.service','fh6-recovery-run.service')
TRANSIENT=re.compile(r'(?i)\b(?:429|500|502|503|504)\b|rate.limit|usage.limit|quota.exceeded|too.many.requests|'
                     r'connection.(?:reset|refused|timed.out)|timed.out|timeout|temporary.failure|'
                     r'network.(?:error|unreachable)|service.unavailable|failed.to.fetch|'
                     r'could.not.resolve|couldn.t.resolve|TLS.handshake|upstream.connect')
AUTH=re.compile(r'(?i)unauthorized|authentication.failed|token.expired|invalid.(?:token|api.key)|please.log.in')

def load(path):
    try:return read(path)
    except (OSError,ValueError):return {}

def tail(path):
    try:
        with path.open('rb') as stream:
            stream.seek(0,2);size=stream.tell();stream.seek(max(0,size-65536))
            return stream.read().decode('utf-8','replace')
    except OSError:return ''

def failure(run,editor,logs):
    """Return a fixed code; private log contents never enter public status."""
    if run.get('status')=='RUNNING':return 'INTERRUPTED'
    if editor.get('status')=='AUTH_REQUIRED' or AUTH.search(logs):return 'AUTH_REQUIRED'
    if editor.get('error')=='TimeoutExpired':return 'TIMEOUT'
    # Three focused handoff attempts already ran in the isolated workspace.
    # Old network text must not turn an incomplete handoff into a blind retry.
    if editor.get('status')=='NO_AUDIT':return 'AUDIT_INCOMPLETE'
    failed={key for key,value in run.get('steps',{}).items() if value.get('status')=='failed'}
    if failed & {'structure','preflight','rollover_preflight','visual_queue','portable','html','artifact','markdown','timestamp'}:
        return 'REVIEW_REQUIRED'
    if TRANSIENT.search(logs):return 'TEMPORARY_FAILURE'
    return 'REVIEW_REQUIRED'

def decision(run,state,editor,logs,at,auth_ready=False):
    day=at.date().isoformat()
    state=dict(state) if state.get('day')==day else {'day':day,'retryCount':0}
    if run.get('status') not in {'RUNNING','BLOCKED'} or run.get('runDate')!=day:
        state.update(status='IDLE',nextAttemptAt=None)
        return state,False
    reason=failure(run,editor,logs)
    if reason=='AUTH_REQUIRED' and auth_ready:reason='AUTH_RESTORED'
    if state.get('runId')!=run['runId']:
        state.update(runId=run['runId'],nextAttemptAt=None)
    state['reason']=reason
    if reason in {'REVIEW_REQUIRED','AUDIT_INCOMPLETE'}:
        state.update(status='NEEDS_REVIEW',nextAttemptAt=None);return state,False
    if reason=='AUTH_REQUIRED':
        state.update(status='NEEDS_LOGIN',nextAttemptAt=None);return state,False
    count=state.get('retryCount',0)
    if not isinstance(count,int) or count<0:count=0
    if count>=len(DELAYS):
        state.update(status='LIMIT_REACHED',nextAttemptAt=None);return state,False
    if not state.get('nextAttemptAt'):
        state.update(status='WAITING',nextAttemptAt=(at+timedelta(seconds=DELAYS[count])).isoformat())
        return state,False
    if at<datetime.fromisoformat(state['nextAttemptAt']):return state,False
    state.update(status='QUEUED',retryCount=count+1,lastAttemptAt=at.isoformat(),nextAttemptAt=None)
    return state,True

def running():
    for unit in UNITS:
        result=subprocess.run(['systemctl','show',unit,'--property=ActiveState','--value'],
                              capture_output=True,text=True,timeout=10)
        if result.returncode or result.stdout.strip() in {'active','activating','deactivating','reloading'}:
            return True
    return False

def login_restored(run,login):
    # login status alone only proves stored credentials, possibly expired.
    # Require a new owner-completed login after this failure as well.
    try:
        return (login.get('status')=='CONNECTED' and
                float(login['updatedAt'])>datetime.fromisoformat(run.get('finishedAt') or run['startedAt']).timestamp())
    except (KeyError,TypeError,ValueError):return False

def tick():
    if running():return
    root,store=runner.ROOT,runner.STORE
    store.mkdir(parents=True,exist_ok=True)
    process_lock=root/'automation/runs/refresh/process.lock'
    # Do not create a root-owned guard lock before the publisher's first run.
    if not process_lock.exists():return
    try:
        with exclusive(store/'runner.lock'),exclusive(process_lock):
            run=load(root/'automation/runs/refresh/active.json')
            state=load(store/'recovery.json')
            editor=load(store/'editor-status.json')
            # Successful/delivering runs do not even inspect logs or auth.
            logs=''
            if run.get('status')=='BLOCKED':
                if run.get('steps',{}).get('audit',{}).get('status')!='passed':
                    logs=tail(store/'editor.log')+'\n'+tail(store/'candidate-validation.log')
                for step in run.get('steps',{}).values():
                    if step.get('status')=='failed' and step.get('log'):
                        path=Path(step['log'])
                        if path.resolve().is_relative_to((root/'automation/runs/refresh').resolve()):
                            logs+='\n'+tail(path)
            ready=False
            if (run.get('status')=='BLOCKED' and failure(run,editor,logs)=='AUTH_REQUIRED'
                    and login_restored(run,load(store/'login/status.json'))):
                ready=subprocess.run(['runuser','-u','fh6-editor','--','/usr/local/bin/codex','login','status'],
                                     stdout=subprocess.DEVNULL,stderr=subprocess.DEVNULL,timeout=15).returncode==0
            state,queue=decision(run,state,editor,logs,datetime.fromisoformat(now()),ready)
            atomic(store/'recovery.json',state)
            if queue:
                subprocess.run(['systemctl','start','--no-block','fh6-recovery-run.service'],check=True,timeout=15)
            print('RECOVERY_STATUS='+state['status'])
    except BlockingIOError:
        print('RECOVERY_STATUS=BUSY')

def resume():
    state=load(runner.STORE/'recovery.json')
    if state.get('status')!='QUEUED' or not state.get('runId'):return
    runner.run(recovery_run_id=state['runId'])

if __name__=='__main__':
    if sys.argv[1:]==['tick']:tick()
    elif sys.argv[1:]==['run']:resume()
    else:raise SystemExit('Use tick or run')
