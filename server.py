import socket
from models import Model
from utiles import log
from request import Request
from routes import error
from routes.routes_todo import route_dict as todo_routes
from routes.routes_user import route_dict as user_routes


def response_for_path(request):

    r = dict()
    r.update(todo_routes())
    r.update(user_routes())

    response = r.get(request.path, error)
    return response(request)


def process_connection(connection: socket.socket):
    with connection:
        buffer_size = 1024
        request = b''
        r = connection.recv(buffer_size)
        if len(r) > 0:
            request += r
            if len(r) < buffer_size:
                log(request)
                # log(request.decode())
                request = request.decode()
                r = Request(request)

            response = response_for_path(r)
            connection.sendall(response)


def run(host: str, port: int):
    log('The server is running at: {}:{}'.format(host, port))
    with socket.socket() as s:
        s.bind((host, port))
        s.listen()
        Model.init_db()
        while True:
            connection, address = s.accept()
            log('The connector is from: {}'.format(address))
            process_connection(connection)


def main():
    config = dict(
        host='127.0.0.1',
        port=3000,
    )

    run(**config)


if __name__ == '__main__':
    main()
