"""Owner task queue. Isolated proposals only; never executes a publisher."""
import contextlib
from datetime import datetime
import fcntl
import json
import os
from pathlib import Path
import pwd
import shutil
import signal
import subprocess
import tempfile
import time
import uuid
from zoneinfo import ZoneInfo

ROOT=Path(os.environ.get('FH6_ROOT','/opt/fh6/repo'))
STORE=Path(os.environ.get('FH6_STORE','/var/lib/fh6'))
BUSY={'QUEUED','RUNNING'}
MAX_TASK=2000

@contextlib.contextmanager
def lock(path,blocking=False):
    with path.open('a+b') as stream:
        fcntl.flock(stream,fcntl.LOCK_EX|(0 if blocking else fcntl.LOCK_NB))
        yield

def save(path,value):
    fd,name=tempfile.mkstemp(dir=path.parent,prefix='.task-')
    try:
        with os.fdopen(fd,'w',encoding='utf-8') as stream:
            json.dump(value,stream,ensure_ascii=False);stream.flush();os.fsync(stream.fileno())
            os.fchmod(stream.fileno(),0o640)
            if os.geteuid()==0:
                owner=pwd.getpwnam('fh6');os.fchown(stream.fileno(),owner.pw_uid,owner.pw_gid)
        os.replace(name,path)
    finally:
        Path(name).unlink(missing_ok=True)

def read(path):
    try:return json.loads(path.read_text(encoding='utf-8'))
    except (OSError,ValueError):return {}

def queue_dir():
    path=STORE/'tasks'
    if path.is_symlink():raise ValueError('Unexpected queue path')
    path.mkdir(mode=0o750,exist_ok=True)
    queue_lock=path/'queue.lock'
    if queue_lock.is_symlink():raise ValueError('Unexpected queue lock')
    queue_lock.touch(exist_ok=True)
    if os.geteuid()==0:
        owner=pwd.getpwnam('fh6')
        os.chown(path,owner.pw_uid,owner.pw_gid)
        os.chown(queue_lock,owner.pw_uid,owner.pw_gid)
        queue_lock.chmod(0o640)
    return path

def latest():
    path=STORE/'tasks'
    if not path.is_dir():return []
    rows=[read(f) for f in path.glob('*.json') if not f.is_symlink()]
    return sorted((r for r in rows if r.get('id')),key=lambda r:r.get('createdAt',0),reverse=True)[:10]

def enqueue(text):
    text=text.strip()
    if not text or len(text)>MAX_TASK or '\0' in text:
        raise ValueError('Введите задачу длиной от 1 до 2000 символов.')
    path=queue_dir()
    with lock(path/'queue.lock'):
        if any(read(f).get('status') in BUSY for f in path.glob('*.json')):
            raise ValueError('Предыдущая задача ещё в очереди или выполняется.')
        row=dict(id=uuid.uuid4().hex,task=text,status='QUEUED',createdAt=time.time(),result='')
        save(path/(row['id']+'.json'),row)
    return row

def snapshot(work):
    """Copy tracked regular source files, never .git or ignored credentials."""
    names=subprocess.run(['git','ls-files','-z'],cwd=ROOT,check=True,capture_output=True,timeout=30).stdout
    for raw in names.split(b'\0'):
        if not raw:continue
        relative=Path(os.fsdecode(raw))
        if relative.is_absolute() or '..' in relative.parts or relative.parts[:2]==('automation','runs'):
            continue
        source=ROOT/relative
        if source.is_symlink() or not source.resolve().is_relative_to(ROOT.resolve()) or not source.is_file():continue
        dest=work/relative;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,dest)
    # Read current server state even when a publication is newer than the checkout.
    for relative in ['data/current-season.json','reports/SOURCE_NOTES.md']:
        source=ROOT/relative
        if source.is_file() and not source.is_symlink():
            dest=work/relative;dest.parent.mkdir(parents=True,exist_ok=True);shutil.copyfile(source,dest)

def execute(row):
    auth=subprocess.run(['runuser','-u','fh6-editor','--','/usr/local/bin/codex','login','status'],capture_output=True,timeout=30)
    if auth.returncode:return 'NEEDS_LOGIN','Войдите в Codex через панель и отправьте задачу заново.'
    base=STORE/'task-workspaces';base.mkdir(mode=0o711,exist_ok=True)
    work=base/row['id'];work.mkdir(mode=0o700)
    snapshot(work)
    subprocess.run(['chown','-R','fh6-editor:fh6-editor',str(work)],check=True,timeout=60)
    prompt=('Выполни задачу владельца проекта в этой отдельной копии. Читай AGENTS.md. '
            'Можно исследовать и подготовить изменения, но не публикуй, не запускай полный pipeline, '
            'не меняй системные службы и не читай/не выводи пароли, токены или файлы авторизации. '
            'Изменения этой копии не устанавливаются автоматически. В конце ответь по-русски: '
            'что сделано, какие файлы изменены, как проверено и что нужно для применения. '
            'Если недоступны нужные данные или права, объясни ограничение. Задача владельца:\n'+row['task'])
    result=work/'task-result.txt'
    logs=STORE/'task-logs';logs.mkdir(mode=0o700,exist_ok=True)
    with (logs/(row['id']+'.log')).open('wb') as log:
        process=subprocess.Popen(['runuser','-u','fh6-editor','--','/usr/local/bin/codex','--search','exec',
            '--sandbox','workspace-write','--skip-git-repo-check','--ephemeral','-o',str(result),prompt],
            cwd=work,stdout=log,stderr=log,start_new_session=True)
        try:process.wait(timeout=1200)
        except subprocess.TimeoutExpired:
            for sig in [signal.SIGTERM,signal.SIGKILL]:
                try:os.killpg(process.pid,sig)
                except ProcessLookupError:pass
                try:process.wait(timeout=5)
                except subprocess.TimeoutExpired:continue
            return 'TIMED_OUT','Задача остановлена по лимиту 20 минут. Сузьте запрос и отправьте заново.'
    if process.returncode:return 'FAILED','Codex завершился с ошибкой. Подробный журнал сохранён на сервере.'
    if result.is_symlink() or not result.is_file() or result.stat().st_size>100_000:
        return 'FAILED','Codex не оставил корректный итоговый ответ.'
    return 'FINISHED',result.read_text(encoding='utf-8',errors='replace')

def reserved_for_schedule():
    current=datetime.now(ZoneInfo('Asia/Krasnoyarsk'))
    minute=current.hour*60+current.minute
    return (335<=minute<=380 or (current.weekday()==3 and 1205<=minute<=1310))

def tick():
    # Reserve time before the daily and Thursday timers; owner tasks cannot
    # consume the single runner lock when a scheduled refresh is about to start.
    if reserved_for_schedule():return
    directory=queue_dir()
    try:
        # Same lock as scheduled/manual refresh: the workspace is never copied during publication.
        with lock(STORE/'runner.lock'):
            with lock(directory/'queue.lock',blocking=True):
                rows=[read(f) for f in directory.glob('*.json') if not f.is_symlink()]
                for row in rows:
                    if row.get('status')=='RUNNING':
                        row.update(status='INTERRUPTED',result='Предыдущий процесс прерван. Отправьте задачу заново.',finishedAt=time.time())
                        save(directory/(row['id']+'.json'),row)
                queued=sorted((r for r in rows if r.get('status')=='QUEUED'),key=lambda r:r['createdAt'])
                if not queued:return
                row=queued[0]
                if len(row.get('id',''))!=32 or any(c not in '0123456789abcdef' for c in row['id']):
                    raise ValueError('Invalid task ID')
                row.update(status='RUNNING',startedAt=time.time());save(directory/(row['id']+'.json'),row)
            try:status,result=execute(row)
            except Exception:status,result='FAILED','Не удалось выполнить задачу. Подробности доступны администратору сервера.'
            with lock(directory/'queue.lock',blocking=True):
                row.update(status=status,result=result,finishedAt=time.time());save(directory/(row['id']+'.json'),row)
    except BlockingIOError:return

if __name__=='__main__':tick()
