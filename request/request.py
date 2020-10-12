from ws_exceptions.ws_exceptions import BadRequest


class Request:
    def __init__(self, client_request: bytes):
        self._parse_request(client_request.decode('utf-8'))
        self._check_request()

    def _parse_request(self, str_request: str) -> None:
        is_first_line = True
        self.headers = dict()
        for line in str_request.splitlines():
            line = line.strip().lstrip()
            if line == '':
                continue
            if line.startswith(('GET', 'POST', 'PUT', 'DELETE')) and\
                    is_first_line:
                first_line = line.split(' ')
                self.method = first_line[0]
                self.uri = first_line[1]
                self.version = first_line[2]
                is_first_line = False
            elif is_first_line:
                break
            else:
                kv = line.split(': ', maxsplit=1)
                self.headers[kv[0]] = kv[1]

    def _check_request(self) -> None:
        if self.method not in ('GET', 'POST', 'PUT', 'DELETE'):
            raise BadRequest('Bad method in request')
        if not self.uri.startswith('/'):
            raise BadRequest('Bad uri in request')
        if not self.version.startswith('HTTP/'):
            raise BadRequest('Bad version in request')


if __name__ == '__main__':
    pass
