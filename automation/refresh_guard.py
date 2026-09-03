"""Durable FH6 run journal and checked completion. Python standard library only."""
import argparse
import contextlib
import hashlib
import json
import os
import re
from pathlib import Path
import shutil
import subprocess
import sys
import time
from datetime import datetime, timedelta, timezone

ZONE = timezone(timedelta(hours=7))
TASK = 'Update FH6 Festival Playlist; audit sources and visuals, publish, check Steam, collect metrics, notify HA.'
TERMINAL = {'COMPLETED', 'PENDING_CONFIRMATION', 'BLOCKED'}

def now():
    return datetime.now(ZONE).isoformat(timespec='seconds')

def read(path):
    return json.loads(Path(path).read_text(encoding='utf-8-sig'))

def atomic(path, value):
    path = Path(path)
    path.parent.mkdir(parents=True, exist_ok=True)
    temp = path.with_suffix(path.suffix + '.tmp')
    with temp.open('w', encoding='utf-8', newline='\n') as stream:
        json.dump(value, stream, ensure_ascii=False, indent=2)
        stream.write('\n')
        stream.flush()
        os.fsync(stream.fileno())
    # OneDrive/AV or a concurrent read may briefly deny Windows rename sharing.
    # Keep the previous valid checkpoint until replacement succeeds; never truncate it.
    for attempt in range(12):
        try:
            os.replace(temp, path)
            break
        except PermissionError:
            if attempt == 11:
                raise
            time.sleep(min(0.1 * (attempt + 1), 0.5))

def digest(path):
    return hashlib.sha256(Path(path).read_bytes()).hexdigest()

def content_digest(state):
    data = dict(state)
    data.pop('lastContentUpdate', None)
    return hashlib.sha256(json.dumps(data, sort_keys=True, ensure_ascii=False).encode()).hexdigest()

@contextlib.contextmanager
def exclusive(path):
    """OS-owned lock is released on process exit/crash; never a stale PID lock."""
    Path(path).parent.mkdir(parents=True, exist_ok=True)
    with open(path, 'a+b') as stream:
        stream.seek(0)
        if os.name == 'nt':
            import msvcrt
            if Path(path).stat().st_size == 0:
                stream.write(b'0'); stream.flush(); stream.seek(0)
            try:
                msvcrt.locking(stream.fileno(), msvcrt.LK_NBLCK, 1)
            except OSError as exc:
                raise RuntimeError('Another refresh_guard process is active; do not start a duplicate.') from exc
        else:
            import fcntl
            fcntl.flock(stream, fcntl.LOCK_EX | fcntl.LOCK_NB)
        try:
            yield
        finally:
            stream.seek(0)
            if os.name == 'nt':
                msvcrt.locking(stream.fileno(), msvcrt.LK_UNLCK, 1)
            else:
                fcntl.flock(stream, fcntl.LOCK_UN)

class Guard:
    def __init__(self, root):
        self.root = Path(root).resolve()
        self.base = self.root / 'automation/runs/refresh'
        self.active = self.base / 'active.json'
        self.state_path = self.root / 'data/current-season.json'
        self.project_path = self.root / 'data/project.json'

    def save(self, run):
        run['updatedAt'] = now()
        atomic(self.base / run['runId'] / 'run.json', run)
        atomic(self.active, run)

    def start(self):
        if self.active.exists():
            run = read(self.active)
            if run['status'] not in TERMINAL:
                return run
        stamp = now()
        run = {'schemaVersion': 1, 'automationId': 'fh6',
               'runId': 'fh6-' + datetime.now(ZONE).strftime('%Y%m%d-%H%M%S-%f'),
               'runDate': stamp[:10], 'startedAt': stamp, 'status': 'RUNNING',
               'task': TASK, 'nextAction': 'Audit every required source and visual; record audit.json.',
               'initialContentSha256': content_digest(read(self.state_path)),
               'steps': {}, 'blockers': [], 'notification': None, 'haReceipt': None}
        self.save(run)
        return run

    def load(self):
        if not self.active.exists():
            raise RuntimeError('Run start first.')
        return read(self.active)

    def audit(self, run, path):
        if run['status'] in TERMINAL:
            raise RuntimeError('Start a new run before recording another audit.')
        audit = read(path)
        state, project = read(self.state_path), read(self.project_path)
        required = {s['id'] for s in project['requiredSources']}
        rows = audit.get('sources', [])
        if len(rows) != len(required) or {s.get('id') for s in rows} != required:
            raise RuntimeError('Audit must cover every required source exactly once.')
        for row in rows:
            if row.get('status') not in {'checked', 'unavailable', 'no_current_item'} or not row.get('note') or not row.get('url', '').startswith('https://'):
                raise RuntimeError('Each audited source needs status, evidence URL and note.')
        for stamp in [audit.get('checkedAt')] + [r.get('checkedAt') for r in rows]:
            age = datetime.now(ZONE) - datetime.fromisoformat(stamp or '')
            if not timedelta(0) <= age <= timedelta(hours=4):
                raise RuntimeError('Audit evidence is stale or future-dated; repeat the live checks.')
        if audit.get('seasonConfirmed') is not True or audit.get('seasonEndAt') != state['season']['endAt']:
            raise RuntimeError('Live season confirmation must match state.')
        if datetime.fromisoformat(state['season']['endAt']) <= datetime.now(ZONE):
            raise RuntimeError('Stored season has ended. Confirm rollover before refresh.')
        visuals = audit.get('visuals', [])
        activities = {a['id']: a for a in state['activities']}
        if len(visuals) != len(activities) or {v.get('id') for v in visuals} != set(activities):
            raise RuntimeError('Every activity visual must be audited exactly once.')
        for visual in visuals:
            activity = activities[visual['id']]
            file = self.root / state['season']['assetsDirectory'] / activity['visual']['image']
            if visual.get('sha256') != digest(file) or not visual.get('note'):
                raise RuntimeError('Visual audit does not match current asset bytes.')
        if not audit.get('sourceNotesSha256') == digest(self.root / 'reports/SOURCE_NOTES.md'):
            raise RuntimeError('Dated source notes must match the audit.')
        audit['stateContentSha256'] = content_digest(state)
        audit['projectSha256'] = digest(self.project_path)
        destination = self.base / run['runId'] / 'audit.json'
        atomic(destination, audit)
        run['steps']['audit'] = {'status': 'passed', 'at': now(), 'path': str(destination), 'sha256': digest(destination)}
        run['nextAction'] = 'Run execute: preflight, build/publication gates, Steam, metrics and final notification.'
        self.save(run)

    def audit_valid(self, run):
        try:
            return self._audit_valid(run)
        except (OSError, ValueError, KeyError, TypeError):
            return False

    def _audit_valid(self, run):
        step = run['steps'].get('audit', {})
        if step.get('status') != 'passed':
            return False
        audit = read(step['path'])
        state = read(self.state_path)
        visuals = {v['id']: v for v in audit['visuals']}
        for activity in state['activities']:
            asset = self.root / state['season']['assetsDirectory'] / activity['visual']['image']
            if digest(asset) != visuals[activity['id']]['sha256']:
                return False
        return (digest(step['path']) == step['sha256']
                and content_digest(read(self.state_path)) == audit['stateContentSha256']
                and digest(self.project_path) == audit['projectSha256']
                and digest(self.root / 'reports/SOURCE_NOTES.md') == audit['sourceNotesSha256']
                and timedelta(0) <= datetime.now(ZONE) - datetime.fromisoformat(audit['checkedAt']) <= timedelta(hours=4)
                and datetime.now(ZONE) < datetime.fromisoformat(audit['seasonEndAt']))

    def command(self, run, name, argv, markers=(), timeout=300):
        run['nextAction'] = name
        run['steps'][name] = {'status': 'running', 'startedAt': now()}
        self.save(run)
        log = self.base / run['runId'] / (name + '.log')
        print('STEP=' + name, flush=True)
        try:
            p = subprocess.run([str(x) for x in argv], cwd=self.root, capture_output=True,
                               encoding='utf-8', errors='replace', timeout=timeout)
            output = p.stdout + '\n' + p.stderr
            code = p.returncode
        except (OSError, subprocess.TimeoutExpired) as exc:
            output, code = str(exc), -1
        log.write_text(output, encoding='utf-8')
        passed = code == 0 and all(token in output for token in markers)
        run['steps'][name] = {'status': 'passed' if passed else 'failed', 'at': now(),
                              'exitCode': code, 'log': str(log), 'sha256': digest(log)}
        if not passed:
            run['blockers'].append(name + ': command failed or required evidence missing; see ' + log.name)
        self.save(run)
        print(output.strip()[-2200:], flush=True)
        return passed, output

    def outcome(self, run):
        required = ['audit', 'preflight', 'timestamp', 'markdown', 'artifact', 'portable', 'html',
                    'structure', 'publish', 'steam_render', 'steam_check', 'metrics']
        missing = [x for x in required if run['steps'].get(x, {}).get('status') != 'passed']
        for name, step in run['steps'].items():
            if step.get('log') and (not Path(step['log']).exists() or digest(step['log']) != step['sha256']):
                missing.append(name + ': changed evidence')
        if not self.audit_valid(run):
            missing.append('audit: stale or changed inputs')
        if not run.get('builtFiles'):
            missing.append('built files: no fingerprints')
        for file, sha in run.get('builtFiles', {}).items():
            if not Path(file).exists() or digest(file) != sha:
                missing.append('changed built file: ' + file)
        if run.get('steamStatus') not in {'UP_TO_DATE', 'PENDING_CONFIRMATION'}:
            missing.append('Steam not verified')
        if missing or run['blockers']:
            return 'BLOCKED', sorted(set(missing + run['blockers']))
        return ('PENDING_CONFIRMATION' if run['steamStatus'] == 'PENDING_CONFIRMATION' else 'COMPLETED'), []

    def execute(self, run):
        if run['status'] in TERMINAL:
            print('Already finalized; use start for a new run.'); return
        # A saved final result is immutable while notification/receipt are retried.
        if run.get('resultPath'):
            return self.deliver(run)
        run['blockers'] = []
        # Never let an earlier attempt's passed downstream step mask a failed retry.
        run['steps'] = {k: v for k, v in run['steps'].items() if k == 'audit'}
        run.pop('builtFiles', None)
        run.pop('steamStatus', None)
        dep = Path.home() / '.cache/codex-runtimes/codex-primary-runtime/dependencies'
        pwsh = shutil.which('pwsh') or str(dep / 'native/powershell/pwsh.exe')
        node = shutil.which('node') or str(dep / 'node/bin/node.exe')
        ps = lambda file, *args: [pwsh, '-NoProfile', '-File', self.root / file, *args]
        plugins = Path.home() / '.codex/plugins/cache'
        deliverers = sorted(plugins.glob('**/skills/build-report/scripts/deliver_portable_artifact.mjs'))
        preflight = bool(deliverers) and Path(pwsh).exists() and Path(node).exists()
        run['steps']['preflight'] = {'status': 'passed' if preflight else 'failed', 'at': now(),
                                    'detail': str(deliverers[-1]) if deliverers else 'Missing trusted deliver_portable_artifact.mjs'}
        if not preflight:
            run['blockers'].append('Обязательный штатный сборщик deliver_portable_artifact.mjs недоступен; дата отчёта не обновлена.')
        if not self.audit_valid(run):
            run['blockers'].append('Полный актуальный аудит не подтверждён.')
        self.save(run)
        rebuilt = False
        if preflight and self.audit_valid(run):
            build = [('timestamp', ps('automation/refresh_last_content_update.ps1'), ['LAST_CONTENT_UPDATE=']),
                     ('markdown', ps('automation/render_season_markdown.ps1'), []),
                     ('artifact', ps('reports/build_artifact.ps1'), []),
                     ('portable', [node, deliverers[-1], '--input', self.root / 'reports/artifact.json', '--output', self.root / 'reports/current-week.html'], []),
                     ('html', [node, self.root / 'reports/enhance_portable_html.mjs'], []),
                     ('structure', ps('automation/validate_season.ps1'), ['STRUCTURE_OK'])]
            for name, argv, markers in build:
                ok, output = self.command(run, name, argv, markers)
                if not ok:
                    break
                if name == 'portable' and not ('validation' in output and 'package' in output and 'passed' in output):
                    run['steps'][name]['status'] = 'failed'
                    run['blockers'].append('Portable receipt must explicitly confirm validation and package passed.')
                    self.save(run); break
            rebuilt = run['steps'].get('structure', {}).get('status') == 'passed'
            if rebuilt:
                state = read(self.state_path)
                run['builtFiles'] = {str(self.root / file): digest(self.root / file) for file in
                                     ['data/current-season.json', 'CURRENT_WEEK.md', state['season']['archiveFile'],
                                      'reports/artifact.json', 'reports/current-week.html']}
                self.save(run)
        # Failed preflight may verify/publish code and audit notes, never changed report bytes.
        report_clean = subprocess.run(['git', 'diff', '--quiet', 'HEAD', '--', 'data/current-season.json',
                        'reports/artifact.json', 'reports/current-week.html', 'CURRENT_WEEK.md', 'seasons'], cwd=self.root).returncode == 0
        if rebuilt or report_clean:
            self.command(run, 'publish', ps('automation/publish_to_github.ps1', '-CommitMessage', 'FH6 guarded run ' + run['runDate']), ['PUBLISHED_SHA=', 'PAGES_URL='], timeout=420)
        else:
            run['blockers'].append('Unfinished report build: publication withheld to preserve public version.')
        if self.command(run, 'steam_render', ps('automation/render_steam_guide.ps1'), ['STEAM_GUIDE_CHARACTERS='])[0]:
            ok, output = self.command(run, 'steam_check', ps('automation/check_steam_guide.ps1'), ['STEAM_STATUS='])
            if ok and 'STEAM_STATUS=UP_TO_DATE' in output and 'STEAM_VERIFICATION=PUBLIC_AND_LOCAL' in output:
                run['steamStatus'] = 'UP_TO_DATE'
            elif ok and 'STEAM_STATUS=UPDATE_REQUIRED' in output:
                run['steamStatus'] = 'PENDING_CONFIRMATION'
            else:
                run['steamStatus'] = 'BLOCKED'
                run['blockers'].append('Публичный Steam не подтверждён.')
        self.command(run, 'metrics', ps('automation/collect_publication_metrics.ps1', '-RunId', run['runId']), ['PUBLIC_METRICS_STATUS=OK'])
        self.save(run)
        self.prepare_result(run)
        self.deliver(run)

    def prepare_result(self, run):
        outcome, reasons = self.outcome(run)
        state = read(self.state_path)
        metrics_path = self.root / 'automation/runs/publication-metrics-state.json'
        metrics = read(metrics_path) if metrics_path.exists() else None
        if not metrics or metrics.get('runId') != run['runId']:
            metrics = None
        lines = ['FH6: ' + {'COMPLETED': 'проверка завершена', 'PENDING_CONFIRMATION': 'нужно подтверждение Steam', 'BLOCKED': 'обновление заблокировано'}[outcome],
                 state['season']['reportTitle'], 'Дедлайн: ' + state['season']['endAt'],
                 'Обновлено в сводке: ' + state['lastContentUpdate'],
                 f"Карточек: {len(state['activities'])}; открытых пунктов: {len(state['openItems'])}.",
                 'Steam: ' + run.get('steamStatus', 'BLOCKED')]
        html = self.root / 'reports/current-week.html'
        lines.append('HTML: ' + str(html.stat().st_size) + ' байт.')
        publication = run['steps'].get('publish', {})
        if publication.get('status') == 'passed':
            text = Path(publication['log']).read_text(encoding='utf-8')
            published = re.search(r'PUBLISHED_SHA=([0-9a-f]{40})', text)
            if published:
                lines.append('GitHub-коммит: ' + published.group(1))
        if outcome == 'COMPLETED':
            lines.append('Полный цикл выполнен; актуальность подтверждена.')
            if content_digest(state) == run.get('initialContentSha256'):
                lines.append('Сводка актуальна, содержательных изменений не требуется; дата проверки обновлена.')
        if reasons:
            lines += ['Причина: ' + r for r in run['blockers']]
            if not run['blockers']:
                lines.append('Не завершены этапы: ' + ', '.join(reasons))
        if metrics:
            lines += [f"Steam: просмотры {metrics['steam']['viewsAdded']:+d} (всего {metrics['steam']['views']}), избранное {metrics['steam']['favoritesAdded']:+d} (всего {metrics['steam']['favorites']}).",
                      f"GitHub-сводка: просмотры {metrics['github']['viewsAdded']:+d} (всего {metrics['github']['viewsTotal']})."]
            if metrics['baselineCreated']:
                lines.append('Создан начальный снимок статистики; прирост пока не измерен.')
        else:
            lines.append('Статистика этого запуска недоступна; старые значения не подставлены.')
        result = {'schemaVersion': 1, 'runId': run['runId'], 'runDate': run['runDate'], 'status': outcome,
                  'notificationType': {'COMPLETED': 'UpToDate', 'PENDING_CONFIRMATION': 'UpdateRequired', 'BLOCKED': 'CheckBlocked'}[outcome],
                  'message': '\n'.join(lines), 'metrics': metrics, 'reasons': reasons, 'createdAt': now()}
        path = self.base / run['runId'] / 'result.json'
        atomic(path, result)
        run['resultPath'], run['resultSha256'] = str(path), digest(path)
        run['status'] = 'AWAITING_DELIVERY'
        run['nextAction'] = 'Deliver checked result to HA and confirm receipt; then return this same result in chat.'
        self.save(run)

    def deliver(self, run):
        if digest(run['resultPath']) != run['resultSha256']:
            raise RuntimeError('Final result changed; refusing unverified notification.')
        result = read(run['resultPath'])
        dep = Path.home() / '.cache/codex-runtimes/codex-primary-runtime/dependencies'
        pwsh = shutil.which('pwsh') or str(dep / 'native/powershell/pwsh.exe')
        if not run.get('notification'):
            ok, output = self.command(run, 'notification', [pwsh, '-NoProfile', '-File', self.root / 'automation/send_home_assistant_notification.ps1', '-Status', result['notificationType'], '-RunId', run['runId'], '-ResultPath', run['resultPath']], ['HA_NOTIFICATION_STATUS='])
            if not ok or not any(x in output for x in ['HA_NOTIFICATION_STATUS=SENT', 'HA_NOTIFICATION_STATUS=ALREADY_SENT']):
                self.save(run); return
            run['notification'] = 'ALREADY_SENT' if 'HA_NOTIFICATION_STATUS=ALREADY_SENT' in output else 'SENT'
            self.save(run)
        ok, output = self.command(run, 'ha_receipt', [pwsh, '-NoProfile', '-File', self.root / 'automation/ha_refresh_watchdog.ps1', '-Action', 'Receipt', '-ResultPath', run['resultPath']], ['HA_RECEIPT_STATUS=CONFIRMED'])
        if not ok:
            run['nextAction'] = 'Retry HA receipt only; final notification is already sent. Do not mark completed.'
            self.save(run); return
        run['haReceipt'] = 'CONFIRMED'
        run['status'], run['finishedAt'] = result['status'], now()
        run['nextAction'] = 'Return result.json.message in chat. No further execution for this run.'
        self.save(run)
        summary = result['message'] + '\nHA_NOTIFICATION_STATUS=' + run['notification'] + '\nHA_RECEIPT_STATUS=CONFIRMED\nRUN_ID=' + run['runId'] + '\n'
        (self.base / run['runId'] / 'summary.txt').write_text(summary, encoding='utf-8')
        print('RUN_FINAL_STATUS=' + run['status'] + '\n' + summary, flush=True)

def main():
    parser = argparse.ArgumentParser()
    parser.add_argument('action', choices=['start', 'status', 'audit', 'execute'])
    parser.add_argument('--root', default=str(Path(__file__).resolve().parents[1]))
    parser.add_argument('--input')
    args = parser.parse_args()
    guard = Guard(args.root)
    # Atomic replacement permits observers during an active executor; only mutations lock.
    with (contextlib.nullcontext() if args.action == 'status' else exclusive(guard.base / 'process.lock')):
        run = guard.start() if args.action == 'start' else guard.load()
        if args.action == 'audit':
            guard.audit(run, args.input)
        elif args.action == 'execute':
            guard.execute(run)
        print(json.dumps({'runId': run['runId'], 'status': run['status'], 'task': run['task'], 'nextAction': run['nextAction'],
                          'steps': {k: v['status'] for k, v in run['steps'].items()}}, ensure_ascii=False, indent=2))

if __name__ == '__main__':
    try:
        main()
    except Exception as exc:
        print('REFRESH_GUARD_ERROR=' + str(exc), file=sys.stderr)
        sys.exit(2)
