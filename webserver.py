import socket
import asyncio
from async_timeout import timeout
from model.request import Request
from model.response import Response
from model.routes import Route, Routes
from ws_logging.ws_logging import Logger
from gzip import compress


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
        self.is_comp = False

    def run(
            self,
            port=80,
            host='localhost',
            is_debug=False,
            is_comp=False
            ) -> None:
        """
        Will begin listen to host:port address
        :param port: port of server
        :param host: address of server
        :param is_debug: debug mode which can give you more
         information about working server
        :param is_comp: compress mode which can compress data by gzip
        """
        if is_debug:
            self.logger.set_debug_mode()
        else:
            self.logger.set_info_mode()

        self.is_comp = is_comp

        self.loop.create_task(asyncio.start_server(self._handle_client, host, port))
        self.logger.server_starts(host, port)
        self.loop.run_forever()

    async def _handle_client(self, reader, writer) -> None:
        addr = writer.get_extra_info('peername')
        self.logger.client_connect(addr)
        while True:
            try:
                request = await asyncio.wait_for(reader.read(1024), timeout=DEFAULT_TIMEOUT)
                if request != b'':
                    response, is_close_conn = await self._handle_request(request, addr)
                    writer.write(response)
                    await writer.drain()
                    if is_close_conn:
                        break
            except asyncio.exceptions.TimeoutError:
                break
        writer.close()
        self.logger.client_disconnect(addr)

    async def _handle_request(self, data: bytes, addr) -> (bytes, bool):
        request = Request(data)
        self.logger.client_request(addr, request.method, request.uri, request. data)
        response = Response(request, self.routes)
        await response.get_resp(request, self.routes)
        sending_data = response.bytes_response()
        is_close_conn = response.is_close_connection()

        if self.is_comp:
            sending_data = compress(sending_data)
            self.logger.server_response(addr, b'compressed data')
        else:
            self.logger.server_response(addr, sending_data)

        return sending_data, is_close_conn

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

    """
    Some usual methods by one decorator:
    """
    def get(self, path: str):
        self.route(path, ('GET',))

    def post(self, path: str):
        self.route(path, ('POST',))

    def options(self, path: str):
        self.route(path, ('OPTIONS',))

    def head(self, path: str):
        self.route(path, ('HEAD',))

    def put(self, path: str):
        self.route(path, ('PUT',))

    def delete(self, path: str):
        self.route(path, ('DELETE',))

    def trace(self, path: str):
        self.route(path, ('TRACE',))

    def connect(self, path: str):
        self.route(path, ('CONNECT',))
