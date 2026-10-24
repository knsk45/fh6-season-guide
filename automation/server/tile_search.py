"""Opt-in periodic tile research. Uses the existing runner and sole publisher."""
import copy
from datetime import datetime
import time
import uuid
from pathlib import Path
from phone_tasks import read, save, lock
from tile_images import HandoffError

INTERVAL = 3 * 60 * 60
RETRY_DELAYS=(300,900,3600)
STATUSES = {'SEARCHING', 'NO_NEW_TILES', 'UPDATED', 'COMPLETE', 'BUSY',
            'AUTH_REQUIRED', 'FAILED', 'STOPPED', 'WAITING', 'SOURCE_UNAVAILABLE','HANDOFF_FAILED'}


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


def source_index(root,store):
    try:
        from tile_images import section_key
        state=read(Path(root)/'data/current-season.json')
        value=read(Path(store)/'tile-image-cache'/section_key(state)/'index.json')
        return value if isinstance(value,dict) and isinstance(value.get('entries',[]),list) else {}
    except (KeyError,ValueError,TypeError):return {}


def snapshot(root, store):
    setting = policy(store)
    result = read(Path(store) / 'tile-search-status.json')
    current = result if result.get('version') == setting['version'] else {}
    downloads=source_index(root,store)
    state=read(Path(root) / 'data/current-season.json')
    return dict(enabled=setting['enabled'],
                status=(current.get('status', 'WAITING') if setting['enabled'] else 'STOPPED'),
                missingCount=len(missing(state)), downloadedCount=len(downloads.get('entries',[])),
                lastCheckedAt=result.get('finishedAt'),
                nextAttemptAt=current.get('nextAttemptAt'), foundCount=current.get('foundCount', 0),
                retryCount=current.get('retryCount',0),retryLimitReached=current.get('retryLimitReached',False))


def schedule_retry(result,previous,transport_failed):
    day=datetime.now().astimezone().date().isoformat()
    count=previous.get('retryCount',0) if previous.get('retryDay')==day else 0
    if type(count) is not int or not 0<=count<=len(RETRY_DELAYS):count=0
    result.update(retryDay=day,retryCount=count,retryLimitReached=False)
    if transport_failed:
        if count<len(RETRY_DELAYS):
            result.update(nextAttemptAt=time.time()+RETRY_DELAYS[count],retryCount=count+1)
        else:result['retryLimitReached']=True


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
            except HandoffError:
                status = 'HANDOFF_FAILED'
            except Exception:
                status = 'FAILED'  # Never expose model output, URLs or private logs.
            result.update(status=status if status in STATUSES else 'FAILED',
                          finishedAt=time.time(), foundCount=found)
            if status == 'BUSY':
                result['nextAttemptAt'] = time.time() + 60
            transport_failed=status in {'SOURCE_UNAVAILABLE','HANDOFF_FAILED'}
            if status=='UPDATED' and missing(read(root/'data/current-season.json')):
                index=source_index(root,store)
                transport_failed=bool(index.get('errors'))
            schedule_retry(result,previous,transport_failed)
            save(store / 'tile-search-status.json', result)
    except BlockingIOError:
        return  # A single worker already holds the search lock.


if __name__ == '__main__':
    import os
    tick(os.environ.get('FH6_ROOT', '/opt/fh6/repo'),
         os.environ.get('FH6_STORE', '/var/lib/fh6'))
