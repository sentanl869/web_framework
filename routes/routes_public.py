from os import path


def static(request) -> bytes:
    filename = request.query['file']
    _path = request.path.split('/')
    dictionary = path.dirname(path.dirname(__file__))
    file_path = path.join(dictionary, _path[1], _path[2], filename)
    with open(file_path, 'rb') as f:
        header = b'HTTP/1.1 200 OK\r\n\r\n'
        file = header + f.read()
        return file


def route_dict() -> dict:
    d = {
        '/static/css': static,
        '/static/js': static,
    }
    return d
