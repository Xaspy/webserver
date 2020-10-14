from ws_exceptions.ws_exceptions import BadResponse
from model.request import Request


methods = []


class Response:
    def __init__(self, request: Request):
        if self._is_empty_request(request):
            return
        if request.method not in ('GET', 'POST', 'PUT', 'DELETE'):
            self._make_bad_request()
            self._load_web_page()
        else:
            self._make_ok()
            self._load_web_page()

    def _is_empty_request(self, request: Request) -> bool:
        if request.method == '' and request.version == '' and request.uri == '':
            self.version = ''
            self.code = ''
            self.headers = ''
            self.web_page = ''
            return True
        return False

    def _make_ok(self):
        self.code = '200 OK'
        self.headers = self._fill_headers()
        self.version = self._get_server_ver()

    def _make_bad_request(self):
        self.code = '400 Bad Request'
        self.headers = self._fill_headers()
        self.version = self._get_server_ver()

    def _load_web_page(self):
        self.web_page = ''

    def _check_some_failures(self, method, request: Request):
        pass

    def _fill_headers(self) -> dict:
        return {}

    def _get_server_ver(self) -> str:
        return 'TEST_VER'

    def headers_str(self) -> str:
        result = ''
        for k in self.headers.keys():
            result = result + k + ': '
            result = result + self.headers[k] + "\r\n"
        return result

    def get_response(self):
        if self.code == '':
            return b''
        headers = self.headers_str()
        response = f'{self.version} {self.code}\r\n' \
                   f'{headers}\r\n' \
                   f'{self.web_page}'
        return bytes(response, encoding='ascii')


def create_response(method):
    methods.append(method)


if __name__ == '__main__':
    pass
