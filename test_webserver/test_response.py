import time
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
            cls.address = '127.0.0.2'
            cls.p = Process(target=start_server, args=(cls.port, cls.address,))
            cls.p.start()
            time.sleep(0.01)
            if cls.p.is_alive():
                break

    def test_not_found_page(self):
        http = urllib3.PoolManager()
        response_b = http.request('GET', f'http://{self.address}:{self.port}/',
                                  headers={'Connection': 'close'})
        response = response_b.status
        self.assertEqual(response, 404)

    def test_not_bad_request(self):
        http = urllib3.PoolManager()
        response_b = http.request('', f'http://{self.address}:{self.port}/',
                                  headers={'Connection': 'close'})
        response = response_b.status
        self.assertEqual(response, 400)

    def test_method_not_allowed(self):
        http = urllib3.PoolManager()
        response_b = http.request('GUT', f'http://{self.address}:'
                                         f'{self.port}/test-page-get',
                                  headers={'Connection': 'close'})
        response = response_b.status
        self.assertEqual(response, 405)

    def test_parametric_route(self):
        http = urllib3.PoolManager()
        response_b = http.request('GET', f'http://{self.address}:'
                                         f'{self.port}/lol/xio',
                                  headers={'Connection': 'close'})
        response = response_b.data.decode('utf-8')
        self.assertEqual(response, 'xio')

    def test_correct_response(self):
        http = urllib3.PoolManager()
        response_b = http.request('GET', f'http://{self.address}:'
                                         f'{self.port}/test-page-get',
                                  headers={'Connection': 'close'})
        response = response_b.data.decode('utf-8')
        self.assertEqual(response, 'get ok')

    def test_get_correct_response(self):
        data = parse.urlencode({'val': 'lol'}).encode()
        req = request.Request(f'http://{self.address}:'
                              f'{self.port}/test-page-post', data=data,
                              headers={'Connection': 'close'})
        resp = request.urlopen(req)
        response = resp.read().decode('utf-8')
        self.assertEqual(response, 'post ok val=lol')

    def test_post_correct_response(self):
        http = urllib3.PoolManager()
        response_b = http.request('GET', f'http://{self.address}:'
                                         f'{self.port}/test-page',
                                  headers={'Connection': 'close'})
        response = response_b.data.decode('utf-8')
        self.assertEqual(response, 'all-right')

    @classmethod
    def tearDownClass(cls):
        cls.p.terminate()


if __name__ == '__main__':
    unittest.main()
