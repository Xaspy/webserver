import unittest
from request.request import Request
from ws_exceptions.ws_exceptions import BadRequest


class TestParseRequest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.bytes_correct_request = b'''
        GET /index HTTP/1.1
        Host: test.lol
        User-Agent: Xaspy
        Connection: close
        '''
        cls.bytes_dh_request = b'''
        GET /index HTTP/1.1
        Host: test.lol
        User-Agent: Xaspy
        Connection_ close
        '''
        cls.bytes_ds_request = b'''
        G_T /index HTTP/1.1
        Host: test.lol
        User-Agent: Xaspy
        Connection: close
        '''

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


if __name__ == '__main__':
    unittest.main()
