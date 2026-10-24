"""Offline current-section extraction and byte handoff tests."""
from pathlib import Path
import tempfile
import unittest
from unittest.mock import patch
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


if __name__=='__main__':unittest.main()
