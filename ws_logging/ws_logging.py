import sys
import logging


LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'


class Logger:
    def __init__(self, is_debug=False):
        if is_debug:
            logging.basicConfig(level=logging.DEBUG, stream=sys.stdout,
                                format=LOG_FORMAT)
        else:
            logging.basicConfig(level=logging.INFO, stream=sys.stdout,
                                format=LOG_FORMAT)

    def server_starts(self, host):
        logging.info(f'Xio server started! Link: http://{host}')

    def client_connect(self, address):
        logging.info(f'Connected by [{address[0]}:{address[1]}]')

    def client_request(self, address, method, uri, data):
        logging.info(f'[{address[0]}:{address[1]}] ({method}) to {uri}')
        logging.debug(f'[{address[0]}:{address[1]}] request body:\n{data}')

    def server_response(self, address, response):
        logging.info(f'[{address[0]}:{address[1]}] {response[9:12].decode("utf-8")}')
        logging.debug(f'[{address[0]}:{address[1]}] response body:\n{response}')


if __name__ == '__main__':
    pass
