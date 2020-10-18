import sys
import logging


LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'


class Logger:
    def __init__(self):
        self.logger = logging.getLogger("webserver")
        stdout_handler = logging.StreamHandler(sys.stdout)
        formatter = logging.Formatter(LOG_FORMAT)
        stdout_handler.setFormatter(formatter)

        self.logger.addHandler(stdout_handler)
        self.logger.setLevel(logging.INFO)

    def set_debug_mode(self):
        self.logger.setLevel(logging.DEBUG)

    def server_starts(self, host):
        self.logger.info(f'Xio server started! Link: http://{host}')

    def client_connect(self, address):
        self.logger.info(f'Connected by [{address[0]}:{address[1]}]')

    def client_request(self, address, method, uri, data):
        self.logger.info(f'[{address[0]}:{address[1]}] ({method}) to {uri}')
        self.logger.debug(f'[{address[0]}:{address[1]}] request body:\n{data}')

    def server_response(self, address, response):
        self.logger.info(f'[{address[0]}:{address[1]}] {response[9:12].decode("utf-8")}')
        self.logger.debug(f'[{address[0]}:{address[1]}] response body:\n{response}')


if __name__ == '__main__':
    pass
