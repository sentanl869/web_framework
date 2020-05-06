from os import path


def css_static(request) -> bytes:
    filename = request.query['file']
    dictionary = path.dirname(path.dirname(__file__))
    css_path = path.join(dictionary, 'static', 'css', filename)
    with open(css_path, 'rb') as f:
        header = b'HTTP/1.1 200 OK\r\nContent-Type: text/css\r\n\r\n'
        css = header + f.read()
        return css


def route_dict() -> dict:
    d = {
        '/static/css': css_static
    }
    return d
