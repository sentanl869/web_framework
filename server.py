import socket
from utiles import log


def process_connection(connection: socket.socket):
    with connection:
        buffer_size = 1024
        request = b''
        while True:
            r = connection.recv(buffer_size)
            request += r
            if len(r) < buffer_size:
                log(request)
                log(request.decode())
                break

        http_response = "HTTP/1.1 200 OK\r\n\r\n<h1>Hello World!</h1>"
        response = http_response.encode()
        connection.sendall(response)


def run(host: str, port: int):
    log('The server is running at: {}:{}'.format(host, port))
    with socket.socket() as s:
        s.bind((host, port))
        s.listen()
        while True:
            connection, address = s.accept()
            log('The visitor is from: {}'.format(address))
            process_connection(connection)


def main():
    config = dict(
        host='127.0.0.1',
        port=3000,
    )

    run(**config)


if __name__ == '__main__':
    main()
