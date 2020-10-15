from ws_exceptions.ws_exceptions import BadResponse
from model.request import Request
from os import path


patterns_path = path.join(path.dirname(path.abspath(__file__)), 'patterns')


class Response:
    def __init__(self, request: Request) -> None:
        if self._is_empty_request(request):
            self.route = ''
            return
        self.route = request.uri

    def _is_empty_request(self, request: Request) -> bool:
        if request.method == '' and request.version == '' and request.uri == '':
            self.version = ''
            self.code = ''
            self.headers = ''
            self.web_page = ''
            return True
        return False

    def get_response(self) -> bytes:
        if self.code == '':
            return b''
        response = f'{self.version} {self.code}\r\n\r\n' \
                   f'{self.web_page}'
        return bytes(response, encoding='ascii')


if __name__ == '__main__':
    pass
