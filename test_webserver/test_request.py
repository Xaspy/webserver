import unittest
from request.request import Request


class TestParseRequest(unittest.TestCase):
    @classmethod
    def setUpClass(cls) -> None:
        cls.bytes_right_request = b'''GET /index HTTP/1.1
        Host: test.lol
        User-Agent: Xaspy
        Connection: close
        '''

    def test_correct_start(self):
        request = Request(self.bytes_right_request)
        self.assertEqual(request.method, 'GET')
        self.assertEqual(request.uri, '/index')
        self.assertEqual(request.version, 'HTTP/1.1')

    def test_correct_headers(self):
        request = Request(self.bytes_right_request)
        self.assertEqual(request.headers['Host'], 'test.lol')
        self.assertEqual(request.headers['User-Agent'], 'Xaspy')
        self.assertEqual(request.headers['Connection'], 'close')


if __name__ == '__main__':
    unittest.main()
