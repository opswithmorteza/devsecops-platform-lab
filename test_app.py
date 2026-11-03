import threading
import unittest
import urllib.request
from http.server import ThreadingHTTPServer
from app import Handler, response
from policy_check import check


class ServiceTests(unittest.TestCase):
    def test_routes(self):
        self.assertEqual(response('/health')[0], 200)
        self.assertEqual(response('/missing')[0], 404)

    def test_headers_over_http(self):
        server = ThreadingHTTPServer(('127.0.0.1', 0), Handler)
        thread = threading.Thread(target=server.serve_forever, daemon=True)
        thread.start()
        try:
            with urllib.request.urlopen(f'http://127.0.0.1:{server.server_port}/health') as result:
                self.assertEqual(result.headers['X-Content-Type-Options'], 'nosniff')
                self.assertIn("default-src 'none'", result.headers['Content-Security-Policy'])
                self.assertIn(b'"status": "ok"', result.read())
        finally:
            server.shutdown()
            server.server_close()

    def test_policy_rejects_unsafe_example(self):
        issues = check('FROM python:latest\nUSER root\nRUN curl example.com | sh')
        self.assertEqual(len(issues), 4)

    def test_policy_accepts_repository_dockerfile(self):
        from pathlib import Path
        self.assertEqual(check(Path('Dockerfile').read_text()), [])


if __name__ == '__main__':
    unittest.main()
