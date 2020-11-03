from os import path
from model.routes import Routes
from model.request import Request
from model.header_handler import HeaderHandler


patterns_path = path.join(path.dirname(path.abspath(__file__)), 'patterns')
RESPONSE_CODES = {
    200: 'OK',
    400: 'Bad Request',
    404: 'Not Found',
    405: 'Method Not Allowed'
}


class Response:
    def __init__(self, req: Request, routes: Routes) -> None:
        self._is_bad_resp = _is_bad_request(req)

        self._hh = HeaderHandler(req.headers)
        if self._is_bad_resp:
            self._message_body = 400
        else:
            self._message_body = routes.execute_route(req.uri, req.method, req.data)

    def bytes_response(self) -> bytes:
        if isinstance(self._message_body, int):
            return self._get_error_resp(self._message_body)
        else:
            page = self._message_body
            self._hh.set_content_length(len(page))
            headers = self._hh.get_string_headers()
            result = f'HTTP/1.1 200 OK\r\n' \
                     f'{headers}\r\n' \
                     f'{page}'
            return bytes(result, encoding='utf-8')

    def _get_error_resp(self, error):
        with open(path.join(patterns_path, f'{error}.html'), 'r') as f:
            page = f.read()
        self._hh.set_content_length(len(page))
        headers = self._hh.get_string_headers()
        result = f'HTTP/1.1 {error} {RESPONSE_CODES[error]}\r\n' \
                 f'{headers}\r\n' \
                 f'{page}'
        return bytes(result, encoding='utf-8')

    def is_close_connection(self) -> bool:
        return self._hh.is_close_connection()

    def is_can_handle_gzip(self) -> bool:
        return self._hh.is_can_handle_gzip()


def _is_bad_request(req: Request) -> bool:
    if req.method == '':
        return True
    if not req.uri.startswith('/'):
        return True
    if not req.version.startswith('HTTP/'):
        return True


if __name__ == '__main__':
    pass
