from ws_exceptions.ws_exceptions import BadRequest


class Request:
    def __init__(self, client_request: bytes) -> None:
        self.method = ''
        self.uri = ''
        self.version = ''
        self.headers = dict()
        self.data = ''
        if client_request != b'':
            self.is_empty_request = False
            self._parse_request(client_request.decode('utf-8'))
            self._check_request()
        else:
            self.is_empty_request = True

    def _parse_request(self, str_request: str) -> None:
        is_first_line = True
        is_data_body = False
        for line in str_request.split('\r\n'):
            if line == '':
                is_data_body = True
                continue
            if is_first_line:
                first_line = line.split(' ')
                if len(first_line) != 3:
                    raise BadRequest('Very short starts line in model')
                self.method = first_line[0]
                self.uri = first_line[1]
                self.version = first_line[2]
            elif not is_data_body:
                kv = line.split(': ', maxsplit=1)
                if len(kv) != 2:
                    continue
                self.headers[kv[0]] = kv[1]
            if is_data_body:
                self.data = line

            is_first_line = False

    def _check_request(self) -> None:
        if self.method not in ('GET', 'POST', 'PUT', 'DELETE'):
            raise BadRequest('Bad method in model')
        if not self.uri.startswith('/'):
            raise BadRequest('Bad uri in model')
        if not self.version.startswith('HTTP/'):
            raise BadRequest('Bad version in model')


if __name__ == '__main__':
    pass
