import socket
import asyncio
from model.request import Request
from model.routes import Route, Routes
from ws_logging.ws_logging import Logger
from model.header_handler import HeaderHandler
from ws_exceptions.ws_exceptions import BadRequest


class Xio:
    def __init__(self, name) -> None:
        self.name = name
        self.routes = Routes()
        self.loop = asyncio.get_event_loop()
        self.logger = Logger()

    def run(self, port=80, host='localhost', is_debug=False) -> None:
        if is_debug:
            self.logger.set_debug_mode()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind((host, port))
            sock.listen(10)
            sock.setblocking(False)
            self.logger.server_starts(host)
            self.loop.run_until_complete(self._run_async(sock))

    async def _run_async(self, sock):
        while True:
            client, addr = await self.loop.sock_accept(sock)
            self.loop.create_task(self._handle_client(client, addr))

    async def _handle_client(self, client, addr):
        with client:
            self.logger.client_connect(addr)
            while True:
                data = await self.loop.sock_recv(client, 2**20)
                try:
                    request = Request(data)
                    hh = HeaderHandler(request.headers)
                    if request.method == 'POST':
                        recv = self.routes.execute_route(request.uri,
                                                         request.method,
                                                         hh,
                                                         request.data)
                    else:
                        recv = self.routes.execute_route(request.uri,
                                                         request.method,
                                                         hh)
                    self.logger.client_request(addr, request.method,
                                               request.uri, data)
                except BadRequest:
                    recv = self.routes.get_bad_request_page(hh)
                    self.logger.client_request(addr, 'BAD', 'BAD', 'BAD')
                self.logger.server_response(addr, recv)
                await self.loop.sock_sendall(client, recv)
                break

    def route(self, path: str, methods=('GET',)):
        def decorator(func):
            route = Route(func, methods)
            self.routes.add_route(path, route)
        return decorator


if __name__ == '__main__':
    pass
