import sys
import logging


LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'


class Logger:
    def __init__(self) -> None:
        self.logger = logging.getLogger("webserver")
        stdout_handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(LOG_FORMAT)
        stdout_handler.setFormatter(formatter)

        self.logger.addHandler(stdout_handler)
        self.logger.setLevel(logging.INFO)

    def set_debug_mode(self) -> None:
        self.logger.setLevel(logging.DEBUG)

    def server_starts(self, host) -> None:
        self.logger.info(f'Xio server started! Link: http://{host}')

    def client_connect(self, address) -> None:
        self.logger.info(f'Connected by [{address[0]}:{address[1]}]')

    def client_disconnect(self, address) -> None:
        self.logger.info(f'Client [{address[0]}:{address[1]}] disconnected')

    def client_request(self, address, method, uri, data) -> None:
        self.logger.info(f'[{address[0]}:{address[1]}]'
                         f' ({method}) to {uri}')
        self.logger.debug(f'[{address[0]}:{address[1]}]'
                          f' request body:\n{data}')

    def server_response(self, address, response) -> None:
        self.logger.info(f'[{address[0]}:{address[1]}]'
                         f' {response[9:12].decode("utf-8")}')
        self.logger.debug(f'[{address[0]}:{address[1]}]'
                          f' response body:\n{response}')


if __name__ == '__main__':
    pass
