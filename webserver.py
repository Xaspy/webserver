import time
import socket
import asyncio
from async_timeout import timeout
from model.request import Request
from model.response import Response
from model.routes import Route, Routes
from ws_logging.ws_logging import Logger
from ws_exceptions.ws_exceptions import BadRequest


DEFAULT_TIMEOUT = 10
QUEUE_SIZE = 5
IS_BLOCKING = False


class Xio:
    def __init__(self, name) -> None:
        """
        Initialize new object of server
        :param name: name of server
        """
        self.name = name
        self.routes = Routes()
        self.loop = asyncio.get_event_loop()
        self.logger = Logger()

    def run(self, port=80, host='localhost', is_debug=False) -> None:
        """
        Will begin listen to host:port address
        :param port: port of server
        :param host: address of server
        :param is_debug: debug mode which can give you more information about working server
        """
        if is_debug:
            self.logger.set_debug_mode()

        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as sock:
            sock.bind((host, port))
            sock.listen(QUEUE_SIZE)
            sock.setblocking(IS_BLOCKING)
            self.logger.server_starts(host)
            self.loop.run_until_complete(self._run_async(sock))

    async def _run_async(self, sock) -> None:
        """
        Start listening and handle requests
        :param sock: socket object of server
        """
        while True:
            client, addr = await self.loop.sock_accept(sock)
            self.logger.client_connect(addr)
            self.loop.create_task(self._handle_client(client, addr))

    async def _handle_client(self, client, addr) -> None:
        """
        Directly getting request and handling timeout of connect
        :param client: client object of connected client
        :param addr: address of connected client
        """
        while True:
            try:
                async with timeout(DEFAULT_TIMEOUT):
                    data = await self.loop.sock_recv(client, 2 ** 20)
                    if data != b'':
                        if await self._handle_request(client, addr, data):
                            break
            except asyncio.TimeoutError:
                break
        client.close()
        self.logger.client_disconnect(addr)

    async def _handle_request(self, client, addr, data: bytes) -> bool:
        """
        Directly handling request
        :param client: client object of connected client
        :param addr: address of connected client
        :param data: request data
        :return: is close connection by client
        """
        request = Request(data)
        response = Response(request, self.routes)
        sending_data = response.bytes_response()

        await self.loop.sock_sendall(client, sending_data)
        self.logger.server_response(addr, sending_data)

        return response.is_close_connection()

    def route(self, path: str, methods=('GET',)):
        """
        Create route to sending respond what you wanna
        :param path: path to your data
        :param methods: methods which supports on this route
        """
        def decorator(func):
            route = Route(func, methods)
            self.routes.add_route(path, route)
        return decorator


if __name__ == '__main__':
    pass
