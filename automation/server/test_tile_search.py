"""Disposable tile search policy/runner tests. Never research or publish live."""
import copy
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import tile_search as search
import runner


def season():
    return dict(season={'endAt':'2026-10-29T21:30:00+07:00'},
        openItems=['visual'], activities=[
            dict(id='photo',kind='photo',title='Exact week',visual={'image':'','sourceImage':''},
                 completeness={'visual':'missing'},missingFields=['visual']),
            dict(id='daily',kind='daily',visual={},missingFields=[]),
            dict(id='monthly',kind='monthly_rivals',visual={'image':'tile.png','sourceImage':'raw.png'},
                 completeness={'visual':'confirmed'},missingFields=[])])


class Tests(unittest.TestCase):
    def fixture(self,d):
        root=Path(d)/'repo';store=Path(d)/'store'
        (root/'data').mkdir(parents=True);store.mkdir()
        (root/'data/current-season.json').write_text(json.dumps(season()))
        return root,store

    def test_missing_excludes_daily_and_preserves_monthly(self):
        self.assertEqual(search.missing(season()),['photo'])

    def test_accepts_only_tile_improvements(self):
        before=season();after=copy.deepcopy(before)
        after['activities'][0].update(visual={'image':'tile.png','sourceImage':'raw.png',
            'sourceUrl':'https://example.org/exact-week.png'},completeness={'visual':'confirmed'},missingFields=[])
        after['openItems']=[]
        self.assertEqual(search.improvements(before,after),1)
        after['activities'][0]['title']='Changed fact'
        with self.assertRaises(ValueError):search.improvements(before,after)

    def test_rejects_rollover_and_replacement_of_monthly(self):
        for mutate in (lambda s:s['season'].update(endAt='2030-01-01'),
                       lambda s:s['activities'][2]['visual'].update(image='different.png')):
            before=season();after=copy.deepcopy(before);mutate(after)
            with self.assertRaises(ValueError):search.improvements(before,after)

    def test_disabled_performs_no_research(self):
        with tempfile.TemporaryDirectory() as d:
            root,store=self.fixture(d)
            with patch.object(runner,'run_tiles') as run:
                search.tick(root,store);run.assert_not_called()

    def test_cooldown_reenable_and_no_new_tiles(self):
        with tempfile.TemporaryDirectory() as d:
            root,store=self.fixture(d);search.set_enabled(store,True)
            with patch.object(runner,'run_tiles',return_value=('NO_NEW_TILES',0)) as run:
                search.tick(root,store);search.tick(root,store)
                self.assertEqual(run.call_count,1)
                self.assertEqual(search.snapshot(root,store)['status'],'NO_NEW_TILES')
                old=search.policy(store)['version']
                search.set_enabled(store,False)
                self.assertFalse(search.still_enabled(store,old))
                search.set_enabled(store,True);search.tick(root,store)
                self.assertEqual(run.call_count,2)

    def test_busy_retries_without_three_hour_delay(self):
        with tempfile.TemporaryDirectory() as d:
            root,store=self.fixture(d);search.set_enabled(store,True)
            with patch.object(runner,'run_tiles',side_effect=BlockingIOError):search.tick(root,store)
            status=search.snapshot(root,store)
            self.assertEqual(status['status'],'BUSY')
            self.assertLess(status['nextAttemptAt']-search.time.time(),61)

    def test_complete_does_not_invoke_model(self):
        with tempfile.TemporaryDirectory() as d:
            root,store=self.fixture(d);state=season();state['activities']=state['activities'][1:]
            (root/'data/current-season.json').write_text(json.dumps(state))
            search.set_enabled(store,True)
            with patch.object(runner,'run_tiles') as run:search.tick(root,store);run.assert_not_called()
            self.assertEqual(search.snapshot(root,store)['status'],'COMPLETE')

    def test_no_new_tiles_does_not_start_guard_or_publish(self):
        with tempfile.TemporaryDirectory() as d:
            root,store=self.fixture(d);search.set_enabled(store,True)
            with patch.object(runner,'ROOT',root),patch.object(runner,'STORE',store),\
                 patch.object(runner,'collect'),patch.object(runner,'editor',return_value=root),\
                 patch.object(runner,'guard') as guard,patch.object(runner,'promote_candidate') as promote:
                self.assertEqual(runner.run_tiles(search.policy(store)['version']),('NO_NEW_TILES',0))
                guard.assert_not_called();promote.assert_not_called()

    def test_disable_during_research_prevents_promotion(self):
        with tempfile.TemporaryDirectory() as d:
            root,store=self.fixture(d);search.set_enabled(store,True)
            version=search.policy(store)['version']
            def edit(**kwargs):search.set_enabled(store,False);return root
            with patch.object(runner,'ROOT',root),patch.object(runner,'STORE',store),\
                 patch.object(runner,'collect'),patch.object(runner,'editor',side_effect=edit),\
                 patch.object(runner,'guard') as guard:
                self.assertEqual(runner.run_tiles(version),('STOPPED',0));guard.assert_not_called()

    def test_unfinished_refresh_is_not_hijacked(self):
        with tempfile.TemporaryDirectory() as d:
            root,store=self.fixture(d);search.set_enabled(store,True)
            active=root/'automation/runs/refresh';active.mkdir(parents=True)
            (active/'active.json').write_text('{"status":"AWAITING_DELIVERY"}')
            with patch.object(runner,'ROOT',root),patch.object(runner,'STORE',store),patch.object(runner,'collect') as collect:
                self.assertEqual(runner.run_tiles(search.policy(store)['version']),('BUSY',0));collect.assert_not_called()

    def test_new_verified_tile_uses_existing_guard(self):
        with tempfile.TemporaryDirectory() as d:
            root,store=self.fixture(d);search.set_enabled(store,True)
            work=Path(d)/'candidate';(work/'data').mkdir(parents=True)
            after=season();after['activities'][0].update(
                visual={'image':'tile.png','sourceImage':'raw.png','sourceUrl':'https://example.org/current.png'},
                completeness={'visual':'confirmed'},missingFields=[])
            (work/'data/current-season.json').write_text(json.dumps(after))
            checkpoint=root/'automation/runs/refresh/active.json'
            def guard(action):
                if action=='execute':
                    checkpoint.parent.mkdir(parents=True,exist_ok=True)
                    checkpoint.write_text('{"status":"COMPLETED"}')
            with patch.object(runner,'ROOT',root),patch.object(runner,'STORE',store),\
                 patch.object(runner,'collect'),patch.object(runner,'editor',return_value=work),\
                 patch.object(runner,'safe_candidate',return_value=[]),\
                 patch.object(runner,'grant_candidate_read_access'),\
                 patch.object(runner,'validate_candidate_state') as validate,\
                 patch.object(runner,'validate_editor_handoff') as audit,\
                 patch.object(runner,'promote_candidate') as promote,\
                 patch.object(runner,'guard',side_effect=guard) as publish:
                self.assertEqual(runner.run_tiles(search.policy(store)['version']),('UPDATED',1))
                validate.assert_called_once_with(work);audit.assert_called_once_with(work)
                promote.assert_called_once_with(work,[])
                self.assertEqual([call.args for call in publish.call_args_list],[('start',),('execute',)])


if __name__=='__main__':unittest.main()
