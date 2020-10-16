import socket
import asyncio
import logging
from model.request import Request
from model.routes import Route, Routes
from ws_logging.ws_logging import Logger
from ws_exceptions.ws_exceptions import BadRequest


class Xio:
    def __init__(self, name) -> None:
        self.name = name
        self.routes = Routes()
        self.loop = asyncio.get_event_loop()

    def run(self, port=80, host='localhost', is_debug=False) -> None:
        self.logger = Logger(is_debug)
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((host, port))
            s.listen(10)
            s.setblocking(False)
            self.logger.server_starts(host)
            self.loop.run_until_complete(self._run_async(s))

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
                    recv = self.routes.execute_route(request.uri,
                                                     request.method)
                except BadRequest:
                    recv = self.routes.get_bad_request_page()
                self.logger.client_request(addr, request.method,
                                           request.uri, request.data)
                self.logger.server_response(addr, recv)
                await self.loop.sock_sendall(client, recv)
                break

    def route(self, path: str, methods=('GET', 'POST', 'DELETE', 'PUT')):
        def decorator(func):
            route = Route(func, methods)
            self.routes.add_route(path, route)
        return decorator


if __name__ == '__main__':
    pass
