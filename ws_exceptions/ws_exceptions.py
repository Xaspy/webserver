
class BadRequest(Exception):
    def __init__(self, message):
        self.message = message


class BadResponse(Exception):
    def __init__(self, message):
        self.message = message


if __name__ == '__main__':
    pass
