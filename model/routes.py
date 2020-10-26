from os import path
from model.header_handler import HeaderHandler

patterns_path = path.join(path.dirname(path.abspath(__file__)), 'patterns')


class Route:
    def __init__(self, func, methods: list) -> None:
        self.funcs = {}
        self.methods = methods
        for method in methods:
            self.funcs[method] = func


class Routes:
    def __init__(self):
        self.routes = {}

    def add_route(self, path_r: str, route: Route) -> None:
        self.routes[path_r] = route

    def execute_route(self, path_r: str, method: str,
                      hh: HeaderHandler, *args, **kwargs) -> bytes:
        if method == '':
            return b''
        if path_r in self.routes.keys():
            if method in self.routes[path_r].funcs:
                data = str(self.routes[path_r].funcs[method](*args, **kwargs))
                hh.set_content_length(len(data))
                headers = hh.get_string_headers()
                result = f'HTTP/1.1 200 OK\r\n' \
                         f'{headers}\r\n' \
                         f'{data}'
                return bytes(result, encoding='utf-8')

        page = _get_error_page(404)
        hh.set_content_length(len(page))
        headers = hh.get_string_headers()
        result = f'HTTP/1.1 404 Not Found\r\n' \
                 f'{headers}\r\n' \
                 f'{page}'
        return bytes(result, encoding='utf-8')

    def get_bad_request_page(self, hh: HeaderHandler) -> bytes:
        page = _get_error_page(400)
        hh.set_content_length(len(page))
        headers = hh.get_string_headers()
        result = f'HTTP/1.1 400 Bad Request\r\n' \
                 f'{headers}\r\n' \
                 f'{page}'
        return bytes(result, encoding='utf-8')


def _get_error_page(error):
    with open(path.join(patterns_path, f'{error}.html'), 'r') as f:
        page = f.read()
    return page


if __name__ == '__main__':
    pass
