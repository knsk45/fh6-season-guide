"""Opt-in periodic tile research. Uses the existing runner and sole publisher."""
import copy
import time
import uuid
from pathlib import Path
from phone_tasks import read, save, lock

INTERVAL = 3 * 60 * 60
STATUSES = {'SEARCHING', 'NO_NEW_TILES', 'UPDATED', 'COMPLETE', 'BUSY',
            'AUTH_REQUIRED', 'FAILED', 'STOPPED', 'WAITING'}


def policy(store):
    value = read(Path(store) / 'tile-search.json')
    return dict(enabled=value.get('enabled') is True, version=value.get('version'))


def set_enabled(store, enabled):
    # UI owns only this policy; the root worker owns its separate result file.
    save(Path(store) / 'tile-search.json',
         dict(enabled=bool(enabled), version=uuid.uuid4().hex, updatedAt=time.time()))


def still_enabled(store, version):
    current = policy(store)
    return current['enabled'] and current['version'] == version


def missing(state):
    return [a['id'] for a in state.get('activities', [])
            if a.get('kind') != 'daily' and
            (not a.get('visual', {}).get('image') or
             not a.get('visual', {}).get('sourceImage') or
             a.get('completeness', {}).get('visual') == 'missing')]


def improvements(before, after):
    """A tile-only pass cannot roll over, change facts or discard known tiles."""
    def facts(state):
        result = copy.deepcopy(state)
        result.pop('openItems', None)
        for card in result.get('activities', []):
            card.pop('visual', None)
            card['missingFields'] = [f for f in card.get('missingFields', []) if f != 'visual']
            card.get('completeness', {}).pop('visual', None)
        return result
    if facts(before) != facts(after):
        raise ValueError('Tile search changed season facts')
    old = {a['id']: a for a in before['activities']}
    new = {a['id']: a for a in after['activities']}
    unresolved = set(missing(before))
    for key, card in old.items():
        if key not in unresolved and card.get('visual') != new[key].get('visual'):
            raise ValueError('Tile search replaced preserved evidence')
    if set(missing(after)) - unresolved:
        raise ValueError('Tile search lost existing evidence')
    gained = unresolved - set(missing(after))
    for key in gained:
        visual = new[key]['visual']
        if not str(visual.get('sourceUrl', '')).startswith(('https://', 'http://')):
            raise ValueError('Network tile needs its original source URL')
    return len(gained)


def snapshot(root, store):
    setting = policy(store)
    result = read(Path(store) / 'tile-search-status.json')
    current = result if result.get('version') == setting['version'] else {}
    return dict(enabled=setting['enabled'],
                status=(current.get('status', 'WAITING') if setting['enabled'] else 'STOPPED'),
                missingCount=len(missing(read(Path(root) / 'data/current-season.json'))),
                lastCheckedAt=result.get('finishedAt'),
                nextAttemptAt=current.get('nextAttemptAt'), foundCount=current.get('foundCount', 0))


def tick(root, store):
    root, store = Path(root), Path(store)
    if not policy(store)['enabled']:
        return
    try:
        with lock(store / 'tile-search-worker.lock'):
            setting = policy(store)
            if not setting['enabled']:
                return
            previous = read(store / 'tile-search-status.json')
            if previous.get('version') == setting['version'] and previous.get('nextAttemptAt', 0) > time.time():
                return
            result = dict(version=setting['version'], status='SEARCHING',
                          startedAt=time.time(), nextAttemptAt=time.time() + INTERVAL)
            save(store / 'tile-search-status.json', result)
            found = 0
            try:
                if not missing(read(root / 'data/current-season.json')):
                    status = 'COMPLETE'
                else:
                    import runner
                    status, found = runner.run_tiles(setting['version'])
            except BlockingIOError:
                status = 'BUSY'
            except Exception:
                status = 'FAILED'  # Never expose model output, URLs or private logs.
            result.update(status=status if status in STATUSES else 'FAILED',
                          finishedAt=time.time(), foundCount=found)
            if status == 'BUSY':
                result['nextAttemptAt'] = time.time() + 60
            save(store / 'tile-search-status.json', result)
    except BlockingIOError:
        return  # A single worker already holds the search lock.


if __name__ == '__main__':
    import os
    tick(os.environ.get('FH6_ROOT', '/opt/fh6/repo'),
         os.environ.get('FH6_STORE', '/var/lib/fh6'))
