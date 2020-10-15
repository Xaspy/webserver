from os import path

patterns_path = path.join(path.dirname(path.abspath(__file__)), 'patterns')


class Route:
    def __init__(self, func, methods) -> None:
        self.func = func
        self.methods = methods


class Routes:
    def __init__(self):
        self.routes = {}

    def add_route(self, path_r: str, route: Route) -> None:
        self.routes[path_r] = route

    def execute_route(self, path_r: str, *args, **kwargs) -> bytes:
        if path_r in self.routes.keys():
            result = self.routes[path_r].func(args, kwargs)
            return bytes(result, encoding='ascii')
        else:
            page = self._get_error_page(404)
            result = f'HTTP/1.1 404 Not Found\r\n\r\n' \
                     f'{page}'
            return bytes(result, encoding='ascii')

    def get_bad_request_page(self) -> bytes:
        page = self._get_error_page(400)
        result = f'HTTP/1.1 404 Bad Request\r\n\r\n' \
                 f'{page}'
        return bytes(result, encoding='ascii')

    def _get_error_page(self, error):
        with open(path.join(patterns_path, f'{error}.html'), 'r') as f:
            page = f.read()
        return page


if __name__ == '__main__':
    pass
