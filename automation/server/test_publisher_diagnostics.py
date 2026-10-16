"""Static contract for publisher observability; no network or Git writes."""
import re
import unittest
from pathlib import Path
import incident_reports


class Tests(unittest.TestCase):
    def test_publisher_phases_are_fixed_and_exportable(self):
        source=(Path(__file__).resolve().parents[1]/'publish_to_github.ps1').read_text(encoding='utf-8-sig')
        phases=re.findall(r"Set-PublishPhase '([a-z_]+)'",source)
        self.assertEqual(set(phases),incident_reports.PUBLISH_PHASES)
        self.assertEqual(len(phases),len(set(phases)))
        self.assertIn('FH6_PUBLISH_NATIVE_EXIT=$LASTEXITCODE',source)
        self.assertIn('FH6_PUBLISH_EXCEPTION=',source)
        self.assertRegex(source,r'(?s)catch \{\s*# Only a static phase.*?\n    throw\n\}\nfinally')

    def test_publication_success_is_not_replaced_by_diagnostic_markers(self):
        source=(Path(__file__).resolve().parents[1]/'refresh_guard.py').read_text()
        self.assertIn("['PUBLISHED_SHA=', 'PAGES_URL=']",source)
        publisher=(Path(__file__).resolve().parents[1]/'publish_to_github.ps1').read_text(encoding='utf-8-sig')
        self.assertNotIn('--force',publisher)
        self.assertIn('build_portable_report.py',publisher)
        self.assertIn('& $Validator -StatePath $StatePath',publisher)


if __name__=='__main__':unittest.main()
