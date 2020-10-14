import socket
from model.request import Request
from model.response import Response

HOST = 'localhost'  # Standard loopback interface address (localhost)
PORT = 80        # Port to listen on (non-privileged ports are > 1023)


def run():
    with socket.socket(socket.AF_INET, socket.SOCK_STREAM) as s:
        s.bind((HOST, PORT))
        s.listen()
        print(f'Server started! Host:{HOST}, port:{PORT}')
        while True:
            conn, addr = s.accept()
            with conn:
                print('Connected by', addr)
                while True:
                    data = conn.recv(2**20)
                    print(data.decode('utf-8'))
                    request = Request(data)
                    response = Response(request)
                    recv = response.get_response()
                    print(recv)
                    conn.sendall(recv)
                    break


if __name__ == '__main__':
    run()
