import socket
from utiles import log
from request import Request
from routes.routes_todo import route_dict as todo_routes


def response_for_path(request):

    r = dict()
    r.update(todo_routes())

    response = r.get(request.path)
    return response(request)


def process_connection(connection: socket.socket):
    with connection:
        buffer_size = 1024
        request = b''
        while True:
            r = connection.recv(buffer_size)
            request += r
            if len(r) < buffer_size:
                # log(request)
                # log(request.decode())
                request = request.decode()
                r = Request(request)
                break

        response = response_for_path(r)
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
