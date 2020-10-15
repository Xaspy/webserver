import socket
from model.routes import Route, Routes
from model.request import Request
from ws_exceptions.ws_exceptions import BadRequest


class Xio:
    def __init__(self, name) -> None:
        self.name = name
        self.routes = Routes()

    def run(self, port=80, host='localhost', is_debug=False) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((host, port))
            s.listen()
            print(f'Xio server started! Link: http://{host}')
            while True:
                conn, addr = s.accept()
                with conn:
                    print(f'Connected by {addr}\n')
                    while True:
                        data = conn.recv(2 ** 20)
                        e = 'nothing'
                        try:
                            request = Request(data)
                            if request.is_empty_request:
                                recv = b''
                            else:
                                recv = self.routes\
                                    .execute_route(request.uri,
                                                   request.method)
                        except BadRequest as e:
                            recv = self.routes.get_bad_request_page()
                        if is_debug:
                            print(f'Request is {data}')
                            print(f'Response is {recv}')
                            print(f'Except: {e}\n')
                        else:
                            print(f'Receive to {addr} response starts with:'
                                  f' "{recv[:24]}..."\n')
                        conn.sendall(recv)
                        break

    def route(self, path: str, methods=('GET', 'POST', 'DELETE', 'PUT')):
        def decorator(func):
            route = Route(func, methods)
            self.routes.add_route(path, route)
        return decorator


if __name__ == '__main__':
    pass
