"""One-time CT109 repair; preserves the existing editor result and never publishes."""
import fcntl
import hashlib
import importlib.util
import os
from pathlib import Path
import shutil
import socket
import subprocess
import tempfile

ORIGINAL = '1978740329e5722c473fd315df2a2304fa2f93f593fd2fa7236a286b484cf11f'
REPAIRED = 'f6aff75366869bb41d47ea8afb5ab9993cff7720e763dea15fe9c71578b22875'
HELPER = 'def grant_candidate_read_access(work):\n    """Let the publisher validate the handoff without sharing either account\'s secrets."""\n    if work != EDITOR/\'work\' or EDITOR.is_symlink() or work.is_symlink() or not work.is_dir():\n        raise RuntimeError(\'Unexpected editorial workspace\')\n    # The editor parent remains private: the publisher can traverse but not list it.\n    subprocess.run([\'setfacl\',\'-m\',\'u:fh6:--x\',str(EDITOR)],check=True)\n    # Apply after every editor run, including files recreated with mode 0600.\n    # Physical traversal never grants access through a candidate symlink.\n    subprocess.run([\'setfacl\',\'-R\',\'-P\',\'-m\',\'u:fh6:rX\',str(work)],check=True)\n\n'

def patched(raw):
    sha = hashlib.sha256(raw).hexdigest()
    if sha == REPAIRED:
        return raw
    if sha != ORIGINAL:
        raise RuntimeError('Unexpected runner version; no code changed')
    text = raw.decode('utf-8')
    text = text.replace('def editor():', HELPER + 'def editor():', 1)
    text = text.replace('                files=safe_candidate(work)\n',
                        '                files=safe_candidate(work)\n                grant_candidate_read_access(work)\n', 1)
    result = text.encode('utf-8')
    if hashlib.sha256(result).hexdigest() != REPAIRED:
        raise RuntimeError('Repair content mismatch; no code changed')
    return result

def main():
    if os.geteuid() != 0 or socket.gethostname() != 'fh6-collector':
        raise RuntimeError('Run only as root inside CT109 fh6-collector')
    root = Path('/opt/fh6/repo')
    store = Path('/var/lib/fh6')
    target = root/'automation/server/runner.py'
    with (store/'runner.lock').open('a') as lock:
        fcntl.flock(lock, fcntl.LOCK_EX | fcntl.LOCK_NB)
        if target.is_symlink():
            raise RuntimeError('Unexpected runner symlink')
        original = target.read_bytes()
        repaired = patched(original)
        if repaired != original:
            backup = store/'repairs'
            backup.mkdir(mode=0o700, exist_ok=True)
            if backup.is_symlink():
                raise RuntimeError('Unexpected backup symlink')
            saved = backup/('runner-'+ORIGINAL+'.py')
            if not saved.exists():
                saved.write_bytes(original)
            if saved.read_bytes() != original:
                raise RuntimeError('Backup mismatch; no code changed')
            stat = target.stat()
            fd, temporary = tempfile.mkstemp(prefix='.runner-repair-', dir=target.parent)
            try:
                with os.fdopen(fd, 'wb') as output:
                    output.write(repaired)
                    output.flush()
                    os.fsync(output.fileno())
                    os.fchown(output.fileno(), stat.st_uid, stat.st_gid)
                    os.fchmod(output.fileno(), stat.st_mode & 0o7777)
                os.replace(temporary, target)
            finally:
                if Path(temporary).exists():
                    Path(temporary).unlink()
        spec = importlib.util.spec_from_file_location('fh6_repaired_runner', target)
        runner = importlib.util.module_from_spec(spec)
        spec.loader.exec_module(runner)
        work = store/'editor/work'
        runner.grant_candidate_read_access(work)
        state = work/'data/current-season.json'
        subprocess.run(['runuser','-u','fh6','--','test','-r',str(state)], check=True)
        if subprocess.run(['runuser','-u','fh6','--','test','-w',str(state)]).returncode == 0:
            raise RuntimeError('Publisher unexpectedly has write access to editor state')
        print('EDITOR_ACCESS_REPAIRED read=yes write=no; saved candidate preserved', flush=True)
        result = subprocess.run(['runuser','-u','fh6','--','pwsh','-NoProfile','-File',
            str(root/'automation/validate_season.ps1'),'-StatePath',str(state),'-SkipOutputs'], cwd=root)
        return result.returncode

if __name__ == '__main__':
    raise SystemExit(main())
