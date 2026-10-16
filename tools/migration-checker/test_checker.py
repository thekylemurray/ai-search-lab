import csv
import io
import threading
import unittest
from urllib.request import Request, urlopen
from urllib.error import HTTPError
from urllib.parse import urlencode
from http.server import ThreadingHTTPServer
from app import Handler, demo_csv, TOKEN
from checker import check, parse_csv, report_csv, Metadata, url_key


class CheckerTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = f'http://127.0.0.1:{cls.server.server_port}'

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def test_real_http_demo(self):
        rows = parse_csv(demo_csv(self.base))
        results = [check(row) for row in rows]
        self.assertEqual([r['result'] for r in results], ['PASS','FAIL','FAIL','FAIL','REVIEW','REVIEW','REVIEW','REVIEW'])
        self.assertIn('unexpected destination', results[1]['findings'])
        self.assertIn('404', results[2]['findings'])
        for text in ('title does not match', 'h1 does not match', 'Canonical does not match'):
            self.assertIn(text, results[3]['findings'])
        self.assertIn('Redirect loop', results[-1]['findings'])
        self.assertEqual(len(list(csv.DictReader(io.StringIO(report_csv(results))))), 8)

    def test_ui_and_download(self):
        with urlopen(self.base + '/?demo=1') as response:
            self.assertIn(b'Synthetic', response.read().replace(b'synthetic',b'Synthetic'))
        data = urlencode({'token': TOKEN, 'mapping': demo_csv(self.base)}).encode()
        with urlopen(Request(self.base + '/check', data=data)) as response:
            body = response.read()
            self.assertIn(b'1 PASS', body)
            self.assertIn(b'3 FAIL', body)
            self.assertIn(b'4 REVIEW', body)
            self.assertIn(b'download="migration-report.csv"', body)
        with self.assertRaises(HTTPError) as err:
            urlopen(Request(self.base + '/check', data=b'token=invalid&mapping=x'))
        self.assertEqual(err.exception.code, 403)
        err.exception.close()

    def test_bad_input(self):
        for data in ('old,new\nx,y', 'old_url,new_url\nfile:///etc/passwd,https://example.com', 'old_url,new_url\nhttps://example.com', 'old_url,new_url,typo\nx,y,z'):
            with self.assertRaises(ValueError): parse_csv(data)
        with self.assertRaises(ValueError): url_key('https://user:pass@example.com/')
        with self.assertRaises(ValueError): url_key('https://example.com/#part')
        self.assertNotEqual(url_key('https://example.com/new'), url_key('https://example.com/new/'))

    def test_html_and_formula(self):
        meta = Metadata()
        meta.feed('<title>A &amp; B</title><h1>Hello <span>world</span></h1><link rel="alternate CANONICAL" href="/x">')
        self.assertEqual(meta.titles, ['A & B'])
        self.assertEqual(meta.headings, ['Hello world'])
        self.assertEqual(meta.canonicals, ['/x'])
        self.assertIn("'=SUM", report_csv([{'actual_title': '=SUM(1)'}]))


if __name__ == '__main__':
    unittest.main()
