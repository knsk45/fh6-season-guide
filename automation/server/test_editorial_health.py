"""Missing English regression and bounded content repair; no live inference."""
import copy
from datetime import timedelta
import hashlib
import json
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import editorial_health as health
import incident_reports
import recovery
import runner
import phone_view

ERROR='Error: English locale is missing howHtml for activity_01_weekly'


def fixture():
    return dict(activities=[dict(id='activity_01_weekly')],locales={'en':dict(
        reportTitle='Winter',seasonDisplay='Winter',activities={'activity_01_weekly':{
            name:'Verified translation' for name in health.FIELDS}})})


class Tests(unittest.TestCase):
    def test_all_renderer_fields_checked_before_promotion(self):
        health.validate_locale(fixture())
        for field in health.FIELDS:
            for value in ('',' ',None,42):
                with self.subTest(field=field,value=value):
                    state=fixture();state['locales']['en']['activities']['activity_01_weekly'][field]=value
                    with self.assertRaisesRegex(ValueError,field):health.validate_locale(state)

    def test_missing_complete_locale_is_repairable(self):
        for state in ({'activities':[]},dict(fixture(),locales={'en':{}})):
            with self.assertRaises(ValueError) as error:health.validate_locale(state)
            self.assertTrue(health.locale_failure(str(error.exception)))

    def test_diagnostic_exposes_fixed_field_not_private_lines(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d);store=root/'store';store.mkdir()
            rid='fh6-20261022-142804-734179';base=root/'automation/runs/refresh'/rid;base.mkdir(parents=True)
            raw=(ERROR+'\nCookie: PRIVATE_SECRET\nPORTABLE_BUILD_FAILED=PRIVATE_SECRET').encode()
            (base/'portable.log').write_bytes(raw)
            run=dict(runId=rid,status='BLOCKED',steps={'portable':dict(status='failed',sha256=hashlib.sha256(raw).hexdigest())})
            report=incident_reports.report(root,store,run)['text']
            self.assertIn('LOCALIZATION_INCOMPLETE',report)
            self.assertIn('English field: howHtml; activity: activity_01_weekly',report)
            self.assertNotIn('PRIVATE_SECRET',report);self.assertNotIn('PORTABLE_RECEIPT',report)
            run['steps']['portable']['sha256']='changed'
            self.assertNotIn('English field:',incident_reports.report(root,store,run)['text'])

    def test_generic_portable_failure_never_claims_receipt_failure(self):
        self.assertFalse(health.locale_failure('English locale is missing PRIVATE_SECRET for ../secret'))
        self.assertEqual(health.locale_context('Cookie: PRIVATE_SECRET'),[])
        self.assertNotIn('PORTABLE_RECEIPT',[v['code'] for v in incident_reports.classify('PORTABLE_BUILD_FAILED=unknown')])

    def test_known_locale_failure_gets_bounded_delayed_repair(self):
        from datetime import datetime
        at=datetime.fromisoformat('2026-10-24T10:00:00+07:00')
        run=dict(runId='fh6-20261024-100000-123456',runDate='2026-10-24',status='BLOCKED',steps={'portable':{'status':'failed'}})
        state,queue=recovery.decision(run,{}, {},ERROR,at)
        self.assertEqual(state['reason'],'LOCALIZATION_INCOMPLETE')
        self.assertEqual(state['status'],'WAITING');self.assertFalse(queue)
        state,queue=recovery.decision(run,state,{},ERROR,at+timedelta(seconds=300))
        self.assertTrue(queue);self.assertEqual(state['retryCount'],1)
        state['retryCount']=3
        state,queue=recovery.decision(run,state,{},ERROR,at+timedelta(hours=2))
        self.assertFalse(queue);self.assertEqual(state['status'],'LIMIT_REACHED')
        run['runDate']='2026-10-22'
        state,queue=recovery.decision(run,{}, {},ERROR,at)
        self.assertFalse(queue);self.assertEqual(state['status'],'IDLE')

    def test_unknown_structural_error_stays_blocked(self):
        run={'status':'BLOCKED','steps':{'portable':{'status':'failed'}}}
        self.assertEqual(recovery.failure(run,{},'PORTABLE_BUILD_FAILED=unknown HTTP 503'),'REVIEW_REQUIRED')

    def test_handoff_missing_translation_does_not_touch_audit_or_canonical(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)/'root';work=Path(d)/'work'
            for folder in (root,work):
                (folder/'data').mkdir(parents=True);(folder/'data/project.json').write_text('{}')
            state=fixture();state['locales']['en']['activities']['activity_01_weekly']['howHtml']=''
            (work/'data/current-season.json').write_text(json.dumps(state))
            with patch.object(runner,'ROOT',root),patch.object(runner,'safe_candidate'),\
                 patch.object(runner,'grant_candidate_read_access') as permissions,patch.object(runner,'Guard') as guard:
                with self.assertRaisesRegex(ValueError,'howHtml'):runner.validate_editor_handoff(work)
                guard.assert_not_called();permissions.assert_not_called()

    def test_newer_run_displays_current_state_and_archives_original_failure(self):
        old=dict(id='old',runId='fh6-20261022-142804-734179',status='BLOCKED',steps={'portable':'failed'})
        active=dict(runId='fh6-20261024-060007-948343',status='COMPLETED',steps={'publish':{'status':'passed'}})
        body=phone_view.refresh_history([old],active)
        self.assertLess(body.index('Проверка завершена'),body.index('История запросов'))
        self.assertGreater(body.index('Проверка остановлена'),body.index('История запросов'))
        self.assertIn('Сборка сайта: ошибка',body)

    def test_recovery_repairs_editorial_content_instead_of_rebuilding_same_bad_audit(self):
        with tempfile.TemporaryDirectory() as d:
            root=Path(d)/'root';store=Path(d)/'store';store.mkdir()
            active=root/'automation/runs/refresh/active.json';active.parent.mkdir(parents=True)
            run=dict(runId='fh6-20261024-100000-123456',status='BLOCKED',steps={})
            active.write_text(json.dumps(run))
            (store/'recovery.json').write_text(json.dumps(dict(runId=run['runId'],reason='LOCALIZATION_INCOMPLETE')))
            (root/'data').mkdir();(root/'data/current-season.json').write_text('{}')
            with patch.object(runner,'ROOT',root),patch.object(runner,'STORE',store),\
                 patch.object(runner,'guard'),patch.object(runner,'Guard') as audit,\
                 patch.object(runner,'collect'),patch.object(runner,'editor',return_value=None) as editor,\
                 patch.object(runner,'queue_incident_analysis'):
                runner.run(recovery_run_id=run['runId'])
                editor.assert_called_once_with(repair_locale=True)
                audit.assert_not_called()


if __name__=='__main__':unittest.main()
