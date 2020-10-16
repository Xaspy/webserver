import unittest
from model.request import Request
from ws_exceptions.ws_exceptions import BadRequest


class TestParseRequest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.bytes_correct_request = b'GET /index HTTP/1.1\r\n' \
                                    b'Host: test.lol\r\n' \
                                    b'User-Agent: Xaspy\r\n' \
                                    b'Connection: close\r\n\r\n' \
                                    b'Hi, my ancient friend!'
        cls.bytes_dh_request = b'GET /index HTTP/1.1\r\n' \
                               b'Host: test.lol\r\n' \
                               b'User-Agent: Xaspy\r\n' \
                               b'Connection_ close\r\n\r\n'
        cls.bytes_ds_request = b'G_T /index HTTP/1.1\r\n' \
                               b'Host: test.lol\r\n' \
                               b'User-Agent: Xaspy\r\n' \
                               b'Connection: close\r\n\r\n'

    def test_correct_start(self):
        request = Request(self.bytes_correct_request)
        self.assertEqual(request.method, 'GET')
        self.assertEqual(request.uri, '/index')
        self.assertEqual(request.version, 'HTTP/1.1')

    def test_correct_headers(self):
        request = Request(self.bytes_correct_request)
        self.assertEqual(request.headers['Host'], 'test.lol')
        self.assertEqual(request.headers['User-Agent'], 'Xaspy')
        self.assertEqual(request.headers['Connection'], 'close')

    def test_damaged_header_correct_start(self):
        request = Request(self.bytes_dh_request)
        self.assertEqual(request.method, 'GET')
        self.assertEqual(request.uri, '/index')
        self.assertEqual(request.version, 'HTTP/1.1')

    def test_damaged_header_fade_away(self):
        request = Request(self.bytes_dh_request)
        self.assertEqual(request.headers['Host'], 'test.lol')
        self.assertEqual(request.headers['User-Agent'], 'Xaspy')
        self.assertFalse('Connection' in request.headers.keys())

    def test_damaged_start_raise_exc(self):
        self.assertRaises(BadRequest, Request, self.bytes_ds_request)

    def test_correct_data_body(self):
        request = Request(self.bytes_correct_request)
        self.assertEqual(request.data, 'Hi, my ancient friend!')


if __name__ == '__main__':
    unittest.main()
