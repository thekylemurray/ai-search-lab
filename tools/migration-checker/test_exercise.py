import tempfile
import threading
import unittest
from pathlib import Path
from http.server import ThreadingHTTPServer
from urllib.request import Request, urlopen
from urllib.parse import urlencode
from app import TOKEN
from exercise import ExerciseHandler, run_benchmark


class ExerciseTest(unittest.TestCase):
    @classmethod
    def setUpClass(cls):
        cls.server = ThreadingHTTPServer(('127.0.0.1', 0), ExerciseHandler)
        cls.thread = threading.Thread(target=cls.server.serve_forever, daemon=True)
        cls.thread.start()
        cls.base = f'http://127.0.0.1:{cls.server.server_port}'

    @classmethod
    def tearDownClass(cls):
        cls.server.shutdown()
        cls.server.server_close()
        cls.thread.join()

    def get(self, path):
        with urlopen(self.base + path) as response:
            return response.read().decode('utf-8')

    def test_benchmark_and_exports(self):
        with tempfile.TemporaryDirectory() as folder:
            self.assertTrue(run_benchmark(self.base, Path(folder)))
            self.assertEqual(len(list(Path(folder).glob('*.csv'))), 4)

    def test_blind_spots_are_real_and_restored(self):
        for slug, text in [('hours', 'Open Monday to Friday'), ('transport', 'name="description"')]:
            self.assertIn(text, self.get('/exercise/before/' + slug))
            self.assertNotIn(text, self.get('/exercise/broken/new/' + slug))
            self.assertIn(text, self.get('/exercise/fixed/new/' + slug))

    def test_browser_workflow(self):
        self.assertIn('flawed migration mapping', self.get('/exercise/'))
        for mode, counts in [('broken', ['12 PASS','5 FAIL','3 REVIEW']), ('fixed', ['20 PASS','0 FAIL','0 REVIEW'])]:
            mapping = self.get(f'/exercise/{mode}.csv')
            data = urlencode({'token': TOKEN, 'mapping': mapping}).encode()
            with urlopen(Request(self.base + '/check', data=data)) as response:
                body = response.read().decode()
            for count in counts:
                self.assertIn(count, body)
            self.assertIn('download="migration-report.csv"', body)
        self.assertIn('outside checker scope', self.get('/exercise/answers'))


if __name__ == '__main__':
    unittest.main()
