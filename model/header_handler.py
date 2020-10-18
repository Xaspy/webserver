import time


class HeaderHandler:
    def __init__(self, request_headers: dict):
        self.headers = {'Connection': 'keep-alive'}
        if 'Connection' in request_headers.keys():
            self.headers['Connection'] = request_headers['Connection']
        self.headers['Server'] = 'xio'
        self.headers['Date'] = _time_to_http_format(time.time())

    def get_string_headers(self) -> str:
        result = ''
        for key in self.headers.keys():
            result += f'{key}: {self.headers[key]}\r\n'
        return result

    def is_close_connection(self) -> bool:
        if self.headers['Connection'].lower() != 'keep-alive':
            return True
        return False

    def set_content_length(self, byte: int):
        self.headers['Content-Length'] = byte


def _time_to_http_format(seconds) -> str:
    s = seconds + time.timezone
    tuple_time = time.localtime(s)
    result = time.strftime('%a, %d %b %Y %X GMT', tuple_time)
    return result


if __name__ == '__main__':
    pass
