from ws_exceptions.ws_exceptions import BadRequest


class Request:
    def __init__(self, client_request: bytes) -> None:
        self.method = ''
        self.uri = ''
        self.version = ''
        self.headers = dict()
        self.data = ''
        self._parse_request(client_request.decode('utf-8'))

    def _parse_request(self, str_request: str) -> None:
        is_first_line = True
        is_data_body = False
        for line in str_request.split('\r\n'):
            if line == '':
                is_data_body = True
                continue
            if is_first_line:
                if not self._is_correct_first_line(line):
                    return
            elif not is_data_body:
                kv = line.split(': ', maxsplit=1)
                if len(kv) != 2:
                    continue
                self.headers[kv[0]] = kv[1]
            if is_data_body:
                self.data = line

            is_first_line = False

    def _is_correct_first_line(self, line: str) -> bool:
        first_line = line.split(' ')
        if len(first_line) != 3:
            return False
        self.method = first_line[0]
        self.uri = first_line[1]
        self.version = first_line[2]
        return True


if __name__ == '__main__':
    pass
