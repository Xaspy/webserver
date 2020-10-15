import unittest
from model.request import Request
from model.response import Response


class TestMakeResponse(unittest.TestCase):
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

    def test_correct_response(self):
        request = Request(self.bytes_correct_request)
        response = Response(request)
        expected_result = b'''HTTP/1.1 200 OK\r\n\r\n'''
        result = response.get_response()
        self.assertTrue(result.startswith(expected_result))


if __name__ == '__main__':
    unittest.main()
