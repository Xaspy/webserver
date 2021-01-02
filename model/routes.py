import re
from ws_exceptions.ws_exceptions import BadParamPath


class Route:
    def __init__(self, func, methods: list) -> None:
        self.funcs = {}
        self.methods = methods
        for method in methods:
            self.funcs[method] = func


class ParamRoute:
    def __init__(self, route: Route, path: str) -> None:
        self.route = route
        self.kwargs = []
        self._make_kwargs(path)

    def _make_kwargs(self, path: str):
        parts = path.split('/')
        i = 0
        for part in parts:
            if '<' in part:
                i += 1
                self.kwargs.append(part[1:-1])
        self.number = i


class Routes:
    def __init__(self) -> None:
        self.routes = {}
        self.param_routes = {}

    def add_route(self, path_r: str, route: Route) -> None:
        self.routes[path_r] = route

    def add_param_route(self, path_r: str, route: Route) -> None:
        opens = len(re.findall(r'<', path_r))
        closes = len(re.findall(r'>', path_r))
        if opens != closes:
            raise BadParamPath('opens not equals closes')
        param_route = ParamRoute(route, path_r)
        self.param_routes[path_r] = param_route

    async def execute_route(self, path_r: str, method: str, *args, **kwargs):
        if path_r in self.routes.keys():
            if method in self.routes[path_r].funcs:
                if method in ('PUT', 'POST'):
                    data = str(await self.routes[path_r].funcs[method](
                        *args, **kwargs))
                else:
                    data = str(await self.routes[path_r].funcs[method]())
                return data
            else:
                return 405
        else:
            return await self._check_param_routes(path_r, method, *args, **kwargs)

    async def _check_param_routes(self, path: str, method: str, *args, **kwargs):
        parts = path.split('/')
        param_kwargs = {}
        for route in self.param_routes.keys():
            r_parts = route.split('/')
            if len(parts) != len(r_parts):
                continue
            if method not in self.param_routes[route].route.funcs:
                continue
            i = 1
            is_first = True
            for r_part in r_parts:
                if is_first:
                    is_first = False
                    continue
                if r_part[0] == '<':
                    param_kwargs[r_part[1:-1]] = parts[i]
                elif r_part != parts[i]:
                    break
                i += 1
            if i == len(r_parts):
                if method in ('PUT', 'POST'):
                    data = str(await self.param_routes[route].route.funcs[method](
                        *args, **kwargs))
                else:
                    data = str(await self.param_routes[route].route.funcs[method](**param_kwargs))
                return data
        return 404
