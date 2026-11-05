"""Read-only, allowlisted FH6 runtime snapshot. No network, logs or credentials.

Run as root inside CT109. Never starts a guard, inference, publication or service.
"""
import argparse
from datetime import datetime
import json
import os
from pathlib import Path
import re
import shutil
import subprocess


def load(path):
    try:
        value = json.loads(path.read_text(encoding='utf-8-sig'))
        return value if isinstance(value, dict) else {}
    except (OSError, ValueError):
        return {}


def enum(value, allowed):
    return value if isinstance(value, str) and value in allowed else 'UNKNOWN'


def stamp(value):
    if not isinstance(value, str):
        return None
    try:
        return datetime.fromisoformat(value).isoformat()
    except ValueError:
        return None


def probe(argv):
    try:
        result = subprocess.run(argv, capture_output=True, text=True, timeout=15)
        return result.returncode, result.stdout.strip()
    except (OSError, subprocess.TimeoutExpired):
        return None, ''


def snapshot(root, store):
    state = load(root / 'data/current-season.json')
    season = state.get('season', {})
    season = season if isinstance(season, dict) else {}
    project = load(root / 'data/project.json')
    active = load(root / 'automation/runs/refresh/active.json')
    steps = active.get('steps', {})
    steps = steps if isinstance(steps, dict) else {}
    known_steps = ['audit', 'preflight', 'rollover_preflight', 'visual_queue',
                   'timestamp', 'markdown', 'artifact', 'portable', 'html',
                   'structure', 'browser_qa', 'publish', 'steam_render',
                   'steam_check', 'metrics']
    report = {
        'schemaVersion': 1,
        'mode': 'READ_ONLY_NO_NETWORK_NO_INFERENCE',
        'stateReadable': bool(state),
        'season': enum(season.get('season'), {'summer', 'autumn', 'winter', 'spring'}),
        'seasonEndAt': stamp(season.get('endAt')),
        'lastContentUpdate': stamp(state.get('lastContentUpdate')),
        'activityCount': len(state.get('activities', [])) if isinstance(state.get('activities'), list) else None,
        'requiredSourceCount': len(project.get('requiredSources', [])) if isinstance(project.get('requiredSources'), list) else None,
        'guardStatus': enum(active.get('status'), {'RUNNING', 'COMPLETED', 'BLOCKED', 'PENDING_CONFIRMATION', 'AWAITING_DELIVERY'}),
        'guardStartedAt': stamp(active.get('startedAt')),
        'guardFinishedAt': stamp(active.get('finishedAt')),
        'steps': {name: enum(steps[name].get('status'), {'passed', 'failed', 'running'})
                  for name in known_steps if isinstance(steps.get(name), dict)},
        'notificationRecorded': bool(active.get('notification')),
        'haReceiptRecorded': bool(active.get('haReceipt')),
        'editorStatus': enum(load(store / 'editor-status.json').get('status'),
                             {'AUTH_REQUIRED', 'FINISHED', 'FAILED'}),
        'reviewRequiredFilePresent': (store / 'review-required.json').is_file(),
        'editorAuditFilePresent': (root / 'automation/editor-audit.json').is_file(),
        'baselinesReadable': {name: bool(load(root / 'automation/runs' / name))
                              for name in ['steam-publication-state.json',
                                           'steam-publication-state-en.json',
                                           'publication-metrics-state.json']},
        'runtimesPresent': {name: bool(shutil.which(name)) for name in ['python3', 'node', 'pwsh']},
    }
    code, sha = probe(['git', '-c', 'safe.directory=' + str(root), '-C', str(root), 'rev-parse', 'HEAD'])
    report['commit'] = sha if code == 0 and re.fullmatch(r'[0-9a-f]{40}', sha) else None
    report['systemd'] = {}
    for unit in ['fh6-refresh.timer', 'fh6-refresh.service', 'fh6-preflight.timer',
                 'fh6-delivery.timer', 'fh6-phone.service', 'fh6-editor-login.path', 'fh6-manual.path']:
        _, status = probe(['systemctl', 'is-active', unit])
        report['systemd'][unit] = enum(status, {'active', 'inactive', 'failed', 'activating', 'deactivating'})
    # Capture only the exit code; CLI output/config/auth files never leave CT109.
    if os.name == 'posix' and os.geteuid() == 0:
        code, _ = probe(['runuser', '-u', 'fh6-editor', '--', '/usr/local/bin/codex', 'login', 'status'])
        report['editorAuth'] = 'CREDENTIALS_PRESENT_NOT_LIVE_VERIFIED' if code == 0 else 'LOGIN_CHECK_FAILED'
    else:
        report['editorAuth'] = 'NOT_CHECKED_RUN_AS_ROOT_IN_CT109'
    return report


if __name__ == '__main__':
    parser = argparse.ArgumentParser(description=__doc__)
    parser.add_argument('--root', type=Path, default=Path('/opt/fh6/repo'))
    parser.add_argument('--store', type=Path, default=Path('/var/lib/fh6'))
    args = parser.parse_args()
    print(json.dumps(snapshot(args.root, args.store), ensure_ascii=False, indent=2))
