

class Route:
    def __init__(self, func, methods: list) -> None:
        self.funcs = {}
        self.methods = methods
        for method in methods:
            self.funcs[method] = func


class Routes:
    def __init__(self) -> None:
        self.routes = {}

    def add_route(self, path_r: str, route: Route) -> None:
        self.routes[path_r] = route

    def execute_route(self, path_r: str, method: str, *args, **kwargs):
        if path_r in self.routes.keys():
            if method in self.routes[path_r].funcs:
                if method in ('PUT', 'POST'):
                    data = str(self.routes[path_r].funcs[method](*args,
                                                                 **kwargs))
                else:
                    data = str(self.routes[path_r].funcs[method]())
                return data
            else:
                return 405
        else:
            return 404


if __name__ == '__main__':
    pass
