from os import path
from functools import wraps
from jinja2 import (
    Environment,
    FileSystemLoader
)
from utiles import log


def initialized_render():
    dictionary = path.dirname(path.dirname(__file__))
    template_path = path.join(dictionary, 'templates')
    loader = FileSystemLoader(template_path)
    e = Environment(loader=loader)
    return e


def formatted_header(headers: dict, code: int = 200) -> str:
    header = 'HTTP/1.1 {} OK\r\n'.format(code)
    header += ''.join(
        ['{}: {}\r\n'.format(k, v) for k, v in headers.items()]
    )
    return header


def html_response(body: str, headers: dict = None) -> bytes:
    h = {
        'Content-Type': 'text/html',
    }
    if headers is None:
        headers = h
    else:
        headers.update(h)

    header = formatted_header(headers)
    r = header + '\r\n' + body
    return r.encode()


def redirect(url: str, headers: dict = None) -> bytes:
    h = {
        'Location': url,
    }
    if headers is None:
        headers = h
    else:
        headers.update(h)

    headers = formatted_header(headers, 302)
    r = headers + '/r/n'
    return r.encode()


def error(request, code: int = 404) -> bytes:
    log(request)
    code = str(code)
    r = {
        '404': b'HTTP/1.1 404 NOT FOUND\r\n\r\n<h1>NOT FOUND</h1>'
    }
    return r.get(code, b'')


class TemplateRender:
    e = initialized_render()

    @classmethod
    def render(cls, filename: str, *args, **kwargs) -> str:
        template = cls.e.get_template(filename)
        return template.render(*args, **kwargs)


def current_user(request):
    pass


def login_required(route_function):
    @wraps(route_function)
    def r():
        pass
