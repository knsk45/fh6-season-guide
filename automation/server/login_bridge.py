"""Owner-only device login. Never put codes/tokens in status, journal or chat."""
from pathlib import Path
import json
import subprocess
import os
import time

LOGIN=Path('/var/lib/fh6/login')
CODEX='/usr/local/bin/codex'

def status(state,started):
    target=LOGIN/'status.json'
    temporary=LOGIN/'status.tmp'
    temporary.write_text(json.dumps(dict(status=state,startedAt=started,updatedAt=time.time())),encoding='utf-8')
    os.chmod(temporary,0o640)
    os.replace(temporary,target)

def authenticated():
    return subprocess.run([CODEX,'login','status'],capture_output=True,timeout=15).returncode==0

def run_login():
    started=time.time()
    target=LOGIN/'device.txt'
    try:
        status('STARTING',started)
        if authenticated():
            status('CONNECTED',started)
            return 0
        with target.open('w') as output:
            os.chmod(target,0o640)
            status('WAITING_FOR_OWNER',started)
            result=subprocess.run([CODEX,'login','--device-auth'],stdin=subprocess.DEVNULL,
                                  stdout=output,stderr=output,timeout=900)
        if result.returncode==0 and authenticated():
            status('CONNECTED',started)
            return 0
        status('FAILED',started)
    except subprocess.TimeoutExpired:
        status('EXPIRED',started)
    except OSError:
        # No raw exception, command output, invitation URL or token in the journal.
        status('FAILED',started)
    finally:
        target.unlink(missing_ok=True)
    return 1

if __name__=='__main__':
    raise SystemExit(run_login())
