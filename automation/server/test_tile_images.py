"""Offline current-section extraction and byte handoff tests."""
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
import json,os,pwd,shutil
import tile_images as images

URL='https://cdn.sanity.io/images/jr6fd40q/production/'+'a'*40+'-884x1416.png'
PNG=b'\x89PNG\r\n\x1a\noriginal-fixture'


class Tests(unittest.TestCase):
    def state(self):
        return {'season':{'season':'winter','startAt':'2026-10-22T21:30:00+07:00'}}
    def page(self):
        return ('<article id="autumn-2026-10-15"><img src="'+URL+'" alt="Wrong week"></article>'
                '<article id="winter-2026-10-22"><article><img src="'+URL+'?w=720" alt="Current tile"></article></article>'
                '<article id="summer-2026-10-08"><img src="'+URL+'" alt="Wrong week"></article>').encode()
    def test_exact_section_and_original_url_only(self):
        parser=images.Images('winter-2026-10-22');parser.feed(self.page().decode())
        self.assertEqual(parser.items,[dict(url=URL,label='Current tile')])
    def test_no_guessing_when_section_absent(self):
        parser=images.Images('winter-2026-11-01');parser.feed(self.page().decode())
        self.assertFalse(parser.found);self.assertEqual(parser.items,[])
    def test_untrusted_origins_ports_and_traversal_rejected(self):
        for url in ('http://127.0.0.1/x','https://cdn.sanity.io.evil.test'+images.PREFIX+'x.png',
                    URL.replace('cdn.sanity.io','cdn.sanity.io:444'),URL.replace('/production/','/production/../')):
            with self.assertRaises(ValueError):images.original_url(url)
    def test_download_is_byte_exact_evidence_not_an_accepted_tile(self):
        with tempfile.TemporaryDirectory() as d,patch.object(images,'fetch',side_effect=[(self.page(),'text/html'),(PNG,'image/png')]):
            cache,index=images.collect(Path(d),Path(d),self.state())
            self.assertEqual(index['status'],'AVAILABLE');self.assertEqual(len(index['entries']),1)
            row=index['entries'][0]
            self.assertEqual((cache/row['path']).read_bytes(),PNG)
            self.assertEqual(row['url'],URL);self.assertNotIn('confirmed',row)
    def test_html_error_response_is_not_saved_as_image(self):
        with tempfile.TemporaryDirectory() as d,patch.object(images,'fetch',side_effect=[(self.page(),'text/html'),(b'<html>error</html>','text/html')]):
            cache,index=images.collect(Path(d),Path(d),self.state())
            self.assertEqual(index['status'],'UNAVAILABLE');self.assertFalse(index['entries'])
            self.assertEqual(len(index['errors']),1)
    def test_download_failures_are_not_missing_tiles(self):
        with tempfile.TemporaryDirectory() as d,patch.object(images,'fetch',side_effect=OSError('PRIVATE_NETWORK_ERROR')):
            cache,index=images.collect(Path(d),Path(d),self.state())
            self.assertEqual(index['status'],'UNAVAILABLE')
            self.assertNotIn('PRIVATE_NETWORK_ERROR',str(index))
    def test_cached_original_survives_a_transient_cdn_failure(self):
        with tempfile.TemporaryDirectory() as d:
            with patch.object(images,'fetch',side_effect=[(self.page(),'text/html'),(PNG,'image/png')]):
                cache,index=images.collect(Path(d),Path(d),self.state())
            # A new page check still proves this URL belongs to the active week.
            # No second CDN download is needed for already verified raw bytes.
            with patch.object(images,'fetch',return_value=(self.page(),'text/html')) as fetch:
                _,current=images.collect(Path(d),Path(d),self.state())
                self.assertEqual(fetch.call_count,1)
            self.assertEqual(current['status'],'AVAILABLE');self.assertTrue(current['entries'][0]['reused'])
            self.assertEqual(current['entries'][0]['sha256'],index['entries'][0]['sha256'])
    def test_changed_cache_is_not_trusted(self):
        with tempfile.TemporaryDirectory() as d:
            with patch.object(images,'fetch',side_effect=[(self.page(),'text/html'),(PNG,'image/png')]):
                cache,index=images.collect(Path(d),Path(d),self.state())
            (cache/index['entries'][0]['path']).write_bytes(b'changed')
            with patch.object(images,'fetch',side_effect=[(self.page(),'text/html'),(PNG,'image/png')]) as fetch:
                _,current=images.collect(Path(d),Path(d),self.state());self.assertEqual(fetch.call_count,2)
            self.assertEqual(current['status'],'AVAILABLE');self.assertNotIn('reused',current['entries'][0])
    def test_corrupt_receipt_falls_back_to_valid_index(self):
        with tempfile.TemporaryDirectory() as d:
            with patch.object(images,'fetch',side_effect=[(self.page(),'text/html'),(PNG,'image/png')]):
                cache,index=images.collect(Path(d),Path(d),self.state())
            next(cache.glob('source-*.json')).write_text('[]')
            with patch.object(images,'fetch',return_value=(self.page(),'text/html')) as fetch:
                _,current=images.collect(Path(d),Path(d),self.state());self.assertEqual(fetch.call_count,1)
            self.assertTrue(current['entries'][0]['reused'])
    def test_corrupt_index_uses_per_source_receipt(self):
        with tempfile.TemporaryDirectory() as d:
            with patch.object(images,'fetch',side_effect=[(self.page(),'text/html'),(PNG,'image/png')]):
                cache,index=images.collect(Path(d),Path(d),self.state())
            (cache/'index.json').write_text('[]')
            with patch.object(images,'fetch',return_value=(self.page(),'text/html')) as fetch:
                _,current=images.collect(Path(d),Path(d),self.state());self.assertEqual(fetch.call_count,1)
            self.assertEqual(current['status'],'AVAILABLE')
    def test_partial_download_reports_transport_problem_and_keeps_good_bytes(self):
        other=URL.replace('a'*40,'b'*40)
        page=self.page().decode().replace('</article><article id="summer',
            '<img src="'+other+'" alt="Other"></article><article id="summer').encode()
        with tempfile.TemporaryDirectory() as d,patch.object(images.time,'sleep'),\
             patch.object(images,'fetch',side_effect=[(page,'text/html'),(PNG,'image/png'),OSError('fixture'),OSError('fixture')]):
            cache,index=images.collect(Path(d),Path(d),self.state())
            self.assertEqual(index['status'],'PARTIAL');self.assertEqual(len(index['entries']),1)
            self.assertEqual((cache/index['entries'][0]['path']).read_bytes(),PNG)
    def test_actual_handoff_checks_hashes_and_section(self):
        with tempfile.TemporaryDirectory() as d,patch.object(images,'fetch',side_effect=[(self.page(),'text/html'),(PNG,'image/png')]):
            cache,index=images.collect(Path(d),Path(d),self.state())
            self.assertEqual(images.verify_handoff(cache,index['section'],user=None),1)
            with self.assertRaises(images.HandoffError):images.verify_handoff(cache,'wrong-week',user=None)
            (cache/index['entries'][0]['path']).write_bytes(b'changed')
            with self.assertRaises(images.HandoffError):images.verify_handoff(cache,index['section'],user=None)
    @unittest.skipUnless(os.geteuid()==0 and shutil.which('runuser'),'Requires unprivileged reader fixture')
    def test_handoff_is_checked_as_actual_editor_user(self):
        with tempfile.TemporaryDirectory() as d,patch.object(images,'fetch',side_effect=[(self.page(),'text/html'),(PNG,'image/png')]):
            Path(d).chmod(0o755)
            cache,index=images.collect(Path(d),Path(d),self.state())
            bundle=Path(d)/'editor-bundle';shutil.copytree(cache,bundle)
            user=pwd.getpwnam('fh6-editor')
            for file in [bundle,*bundle.iterdir()]:os.chown(file,user.pw_uid,user.pw_gid)
            self.assertEqual(images.verify_handoff(bundle,index['section']),1)
            (bundle/index['entries'][0]['path']).chmod(0)
            with self.assertRaises(images.HandoffError):images.verify_handoff(bundle,index['section'])


if __name__=='__main__':unittest.main()
