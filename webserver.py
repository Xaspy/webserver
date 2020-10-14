import socket
from model.request import Request
from model.response import Response


class Xio:
    def __init__(self, name, host='localhost') -> None:
        self.name = name
        self.host = host
        self.port = 80

    def run(self, is_debug=False) -> None:
        with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
            s.bind((self.host, self.port))
            s.listen()
            print(f'Xio server started! Link: http://{self.host}')
            while True:
                conn, addr = s.accept()
                with conn:
                    print('Connected by', addr)
                    while True:
                        data = conn.recv(2 ** 20)
                        if is_debug:
                            print(data.decode('utf-8'))
                        request = Request(data)
                        response = Response(request)
                        recv = response.get_response()
                        if is_debug:
                            print(recv)
                        conn.sendall(recv)
                        break


if __name__ == '__main__':
    pass
