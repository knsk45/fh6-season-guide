"""Server supervisor. An HTTP success is NEVER treated as an editorial audit.

Agent runs as a different Linux user without publisher/HA credentials. Only a
fresh full editorial audit may enter the existing guard. Phone approvals are
hash-bound review records, not evidence that Steam was actually published.
"""
import argparse
import concurrent.futures
import hashlib
import json
import os
from pathlib import Path
import shutil
import signal
import subprocess
import sys
import time
import urllib.request
import urllib.error

os.environ.setdefault('FH6_BROWSER_QA','/opt/fh6/venv/bin/python')

ROOT = Path(os.environ.get('FH6_ROOT', '/opt/fh6/repo'))
STORE = Path(os.environ.get('FH6_STORE', '/var/lib/fh6'))
EDITOR = STORE / 'editor'
sys.path.insert(0, str(ROOT / 'automation'))
from refresh_guard import Guard, atomic, read, digest, now, exclusive

def publisher(*args, check=True):
    return subprocess.run(['runuser','-u','fh6','--',*map(str,args)],cwd=ROOT,check=check)

def guard(action, *args):
    return publisher('python3', ROOT/'automation/refresh_guard.py',action,*args)

def fetch(row):
    request = urllib.request.Request(row['url'],headers={'User-Agent':'FH6-server/1.0'})
    for attempt in range(3):
        try:
            with urllib.request.urlopen(request,timeout=25) as response:
                body=response.read(2_000_000)
                return dict(id=row['id'],url=row['url'],checkedAt=now(),httpStatus=response.status,
                            sha256=hashlib.sha256(body).hexdigest(),body=body.decode('utf-8','replace'),
                            editorialStatus='NOT_REVIEWED')
        except Exception as exc:
            status=getattr(exc,'code',0)
            temporary=(status in {429,500,502,503,504} or
                       (not status and isinstance(exc,(urllib.error.URLError,TimeoutError))))
            if temporary and attempt<2:
                time.sleep((2,5)[attempt]);continue
            return dict(id=row['id'],url=row['url'],checkedAt=now(),httpStatus=status,
                        error=type(exc).__name__,editorialStatus='NOT_REVIEWED')

def collect():
    rows=read(ROOT/'data/project.json')['requiredSources']
    with concurrent.futures.ThreadPoolExecutor(max_workers=4) as pool:
        results=list(pool.map(fetch,rows))
    atomic(STORE/'source-snapshots.json',dict(checkedAt=now(),sources=results))
    return results

def safe_candidate(path):
    """No symlinks, traversal, unexpected file types or executable content."""
    allowed=['data/current-season.json','reports/SOURCE_NOTES.md','automation/editor-audit.json','automation/new-season-input.json']
    files=[path/name for name in allowed if (path/name).is_file()]
    files+=list((path/'reports/assets').rglob('*')) if (path/'reports/assets').exists() else []
    assets=read(path/'data/current-season.json')['season']['assetsDirectory']
    if not assets.startswith('reports/assets/') or '..' in Path(assets).parts:
        raise RuntimeError('Candidate asset directory escapes reports/assets')
    files=[f for f in files if not f.is_file() or not (ROOT/f.relative_to(path)).exists()
           or digest(f)!=digest(ROOT/f.relative_to(path)) or f.relative_to(path).as_posix() in allowed]
    for file in files:
        if file.is_symlink() or not file.resolve().is_relative_to(path.resolve()):
            raise RuntimeError('Symlink/traversal in candidate')
        if file.is_file() and file.relative_to(path).as_posix() not in allowed:
            if file.suffix.lower() not in {'.png','.jpg','.jpeg','.webp'}:
                raise RuntimeError('Unexpected new asset type')
    return [f for f in files if f.is_file()]

def grant_candidate_read_access(work):
    """Let the publisher validate the handoff without sharing either account's secrets."""
    if work != EDITOR/'work' or EDITOR.is_symlink() or work.is_symlink() or not work.is_dir():
        raise RuntimeError('Unexpected editorial workspace')
    # The editor parent remains private: the publisher can traverse but not list it.
    subprocess.run(['setfacl','-m','u:fh6:--x',str(EDITOR)],check=True)
    # Apply after every editor run, including files recreated with mode 0600.
    # Physical traversal never grants access through a candidate symlink.
    subprocess.run(['setfacl','-R','-P','-m','u:fh6:rX',str(work)],check=True)

def wait_editor(process,timeout=1200,grace=5):
    try:
        process.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        # runuser and Codex descendants belong to the invocation's own group.
        for sig in (signal.SIGTERM,signal.SIGKILL):
            try:os.killpg(process.pid,sig)
            except ProcessLookupError:pass
            try:process.wait(timeout=grace)
            except subprocess.TimeoutExpired:continue
        raise

def editor():
    # Dedicated directory; rebuild source view without any ignored secrets/.git.
    work=EDITOR/'work'
    if work.exists():
        archive=EDITOR/('previous-'+str(time.time_ns()))
        work.rename(archive)
    shutil.copytree(ROOT,work,ignore=shutil.ignore_patterns('.git','runs','outputs','__pycache__','*.bak','*.tmp','editor-audit.json'))
    shutil.copyfile(STORE/'source-snapshots.json',work/'source-snapshots.json')
    shutil.copytree(STORE/'inbox',work/'phone-inbox',dirs_exist_ok=True)
    subprocess.run(['chown','-R','fh6-editor:fh6-editor',str(EDITOR)],check=True)
    prompt=(ROOT/'automation/server/editor-prompt.md').read_text(encoding='utf-8')
    # Account authentication stays in editor's private home; never copy PC auth.
    status=subprocess.run(['runuser','-u','fh6-editor','--','/usr/local/bin/codex','login','status'],capture_output=True)
    if status.returncode:
        atomic(STORE/'editor-status.json',{'status':'AUTH_REQUIRED','at':now()})
        return None
    logs=STORE/'editor-logs';logs.mkdir(mode=0o700,exist_ok=True)
    if (STORE/'editor.log').exists():
        (STORE/'editor.log').rename(logs/('editor-'+str(time.time_ns())+'.log'))
    if (STORE/'candidate-validation.log').exists():
        (STORE/'candidate-validation.log').rename(logs/('validation-'+str(time.time_ns())+'.log'))
    atomic(STORE/'editor-status.json',{'status':'RUNNING','at':now()})
    with (STORE/'editor.log').open('w') as log:
        process=subprocess.Popen(['runuser','-u','fh6-editor','--','/usr/local/bin/codex','--search','exec',
                  '--sandbox','workspace-write','--skip-git-repo-check','--ephemeral',prompt],
                  cwd=work,stdout=log,stderr=log,start_new_session=True)
        wait_editor(process)
    audit=work/'automation/editor-audit.json'
    status='FAILED' if process.returncode else ('FINISHED' if audit.is_file() else 'NO_AUDIT')
    atomic(STORE/'editor-status.json',{'status':status,'at':now()})
    return work if status=='FINISHED' else None

def run(force=False,recovery_run_id=None):
    STORE.mkdir(parents=True,exist_ok=True)
    with exclusive(STORE/'runner.lock'):
        checkpoint=ROOT/'automation/runs/refresh/active.json'
        if checkpoint.exists():
            previous=read(checkpoint)
            if recovery_run_id:
                if previous['runId']!=recovery_run_id or previous['status'] not in {'RUNNING','BLOCKED'}:
                    return
                # A recent, accepted audit can repeat guarded deterministic stages
                # without another model invocation. Hash/freshness checks stay intact.
                if Guard(ROOT).audit_valid(previous):
                    audit=previous['steps']['audit']['path']
                    guard('start');guard('audit','--input',audit);guard('execute')
                    return
            if (not force and not recovery_run_id and previous['status'] in {'COMPLETED','BLOCKED','PENDING_CONFIRMATION'}
                    and previous.get('runDate')==now()[:10]
                    and previous.get('finishedAt','')[11:16]>='06:00'):
                return
        elif recovery_run_id:
            return
        guard('start')
        active=read(ROOT/'automation/runs/refresh/active.json')
        if active.get('resultPath') and active['status']=='AWAITING_DELIVERY':
            # Old final is not today's success. Preserve it and close as an error.
            if read(active['resultPath'])['runDate'] < now()[:10] and not active.get('notification'):
                guard('close-expired')
            guard('execute')
            active=read(ROOT/'automation/runs/refresh/active.json')
            if active['status']=='AWAITING_DELIVERY': return
            guard('start')
        if force:
            import refresh_receipts
            refresh_receipts.bind(STORE,read(ROOT/'automation/runs/refresh/active.json')['runId'])
        collect()
        try:
            work=editor()
        except Exception as exc:
            atomic(STORE/'editor-status.json',{'status':'FAILED','at':now(),'error':type(exc).__name__})
            work=None
        if work:
            try:
                files=safe_candidate(work)
                grant_candidate_read_access(work)
                # Daily hybrid phase: new seasons require editorial review here.
                if read(work/'data/current-season.json')['season'] != read(ROOT/'data/current-season.json')['season']:
                    raise RuntimeError('Season rollover candidate requires review before application')
                validation=subprocess.run(['runuser','-u','fh6','--','pwsh','-NoProfile','-File',
                    str(ROOT/'automation/validate_season.ps1'),'-StatePath',str(work/'data/current-season.json'),
                    '-SkipOutputs'],cwd=ROOT,stdout=subprocess.PIPE,stderr=subprocess.STDOUT,text=True,timeout=120)
                (STORE/'candidate-validation.log').write_text(validation.stdout,encoding='utf-8')
                validation.check_returncode()
                # Validate a prospective audit BEFORE changing canonical state.
                # Guard is rooted in the credential-free candidate, so all paths match.
                review=Guard(work)
                candidate=review.start()
                review.audit(candidate,work/'automation/editor-audit.json')
                if not review.audit_valid(candidate): raise RuntimeError('Candidate audit rejected')
                # Preserve before-images for operational rollback, never delete evidence.
                backup=STORE/('before-editor-'+str(time.time_ns()))
                for file in files:
                    relative=file.relative_to(work)
                    target=ROOT/relative
                    if target.exists():
                        saved=backup/relative;saved.parent.mkdir(parents=True,exist_ok=True)
                        shutil.copyfile(target,saved)
                    target.parent.mkdir(parents=True,exist_ok=True)
                    shutil.copyfile(file,target)
                    shutil.chown(target,user='fh6',group='fh6')
                guard('audit','--input',ROOT/'automation/editor-audit.json')
                (STORE/'review-required.json').unlink(missing_ok=True)
            except Exception as exc:
                atomic(STORE/'review-required.json',{'at':now(),'reason':str(exc),'stateSha256':digest(ROOT/'data/current-season.json')})
        else:
            atomic(STORE/'review-required.json',{'at':now(),'reason':'Full live editorial audit not produced. No public timestamp refresh.','stateSha256':digest(ROOT/'data/current-season.json')})
        # The guard yields an honest BLOCKED final when no audit is available.
        guard('execute')
        active=read(ROOT/'automation/runs/refresh/active.json')
        if active['status']=='AWAITING_DELIVERY': raise RuntimeError('HA delivery is not confirmed; run remains unfinished')

if __name__=='__main__':
    parser=argparse.ArgumentParser()
    parser.add_argument('action',choices=['run','collect','publish-audit'])
    parser.add_argument('--force',action='store_true',help='Owner-requested unscheduled audit, still resumes unfinished runs')
    parser.add_argument('--audit')
    args=parser.parse_args()
    if args.action=='collect': collect()
    elif args.action=='publish-audit':
        with exclusive(STORE/'runner.lock'):
            guard('start');guard('audit','--input',args.audit);guard('execute')
    else: run(args.force)
