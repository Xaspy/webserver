import sys
import os
from datetime import datetime
import logging
from logging import handlers


LOG_FORMAT = '%(asctime)s - %(levelname)s - %(message)s'
LOGS_PATH = os.path.abspath(os.path.join(os.path.dirname(__file__), '..', 'logs'))


def _get_current_date() -> str:
    return datetime.now().strftime('%d_%m_%Y')


class Logger:
    def __init__(self) -> None:
        self._current_date = _get_current_date()
        self.logger = logging.getLogger("webserver")
        self.formatter = logging.Formatter(LOG_FORMAT)

        self._upload_handlers()

    def set_debug_mode(self) -> None:
        self.logger.setLevel(logging.DEBUG)

    def server_starts(self, host, port) -> None:
        if self._current_date != _get_current_date():
            self._upload_handlers()
        self.logger.info(f'Xio server started! Link: http://{host}:{port}')

    def client_connect(self, address) -> None:
        if self._current_date != _get_current_date():
            self._upload_handlers()
        self.logger.info(f'Connected by [{address[0]}:{address[1]}]')

    def client_disconnect(self, address) -> None:
        if self._current_date != _get_current_date():
            self._upload_handlers()
        self.logger.info(f'Client [{address[0]}:{address[1]}] disconnected')

    def client_request(self, address, method, uri, data) -> None:
        if self._current_date != _get_current_date():
            self._upload_handlers()
        self.logger.info(f'[{address[0]}:{address[1]}]'
                         f' ({method}) to {uri}')
        self.logger.debug(f'[{address[0]}:{address[1]}]'
                          f' request body:\n{data}')

    def server_response(self, address, response) -> None:
        if self._current_date != _get_current_date():
            self._upload_handlers()
        self.logger.info(f'[{address[0]}:{address[1]}]'
                         f' {response[9:12].decode("utf-8")}')
        self.logger.debug(f'[{address[0]}:{address[1]}]'
                          f' response body:\n{response}')

    def _upload_handlers(self):
        self._current_date = _get_current_date()
        for handler in self.logger.handlers[:]:
            logging.root.removeHandler(handler)

        stdout_handler = logging.StreamHandler(sys.stdout)
        stdout_handler.setFormatter(self.formatter)
        file_handler = logging.FileHandler(os.path.join(LOGS_PATH,
                                                        self._current_date +
                                                        ".log"))
        file_handler.setFormatter(self.formatter)

        mem_handler = handlers.MemoryHandler(10, flushLevel=logging.INFO,
                                             target=file_handler)

        self.logger.addHandler(stdout_handler)
        self.logger.addHandler(mem_handler)
        if self.logger.level == logging.INFO:
            self.logger.setLevel(logging.INFO)
        else:
            self.logger.setLevel(logging.DEBUG)


if __name__ == '__main__':
    print(LOGS_PATH)