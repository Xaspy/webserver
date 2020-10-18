import time
import requests
from urllib import request, parse
import urllib3
import unittest
from webserver import Xio
from multiprocessing import Process
from test_webserver.create_ws import start_server


class TestMakeResponse(unittest.TestCase):
    p = Process()

    @classmethod
    def setUpClass(cls) -> None:
        cls.app = Xio(__name__)

        for i in range(10):
            cls.port = 5000 + i
            cls.p = Process(target=start_server, args=(cls.port,))
            cls.p.start()
            time.sleep(0.5)
            if cls.p.is_alive():
                break

    def test_not_found_page(self):
        http = urllib3.PoolManager()
        response_b = http.request('GET', f'http://localhost:{self.port}/')
        response = response_b.status
        self.assertEqual(response, 404)

    def test_bad_request(self):
        http = urllib3.PoolManager()
        response_b = http.request('GUT', f'http://localhost:{self.port}/')
        response = response_b.status
        self.assertEqual(response, 400)

    def test_correct_response(self):
        http = urllib3.PoolManager()
        response_b = http.request('GET', f'http://localhost:'
                                         f'{self.port}/test-page-get')
        response = response_b.data.decode('utf-8')
        self.assertEqual(response, 'get ok')

    def test_get_correct_response(self):
        data = parse.urlencode({'val': 'lol'}).encode()
        req = request.Request(f'http://localhost:'
                              f'{self.port}/test-page-post', data=data)
        resp = request.urlopen(req)
        response = resp.read().decode('utf-8')
        self.assertEqual(response, 'post ok val=lol')

    def test_post_correct_response(self):
        http = urllib3.PoolManager()
        response_b = http.request('GET', f'http://localhost:'
                                         f'{self.port}/test-page')
        response = response_b.data.decode('utf-8')
        self.assertEqual(response, 'all-right')

    @classmethod
    def tearDownClass(cls):
        cls.p.terminate()


if __name__ == '__main__':
    unittest.main()
