from os import path
from functools import wraps
from json import dumps
from jinja2 import (
    Environment,
    FileSystemLoader,
)
from utiles import log
from models import token_checked
from models.user import User
from models.todo import Todo
from models.session import Session


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


def json_response(data, headers: dict = None) -> bytes:
    h = {
        'Content-Type': 'application/json',
    }
    if headers is None:
        headers = h
    else:
        headers.update(h)

    header = formatted_header(headers)
    body = dumps(data, ensure_ascii=False, indent=2)
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
    log('Error: \n', request)
    code = str(code)
    r = {
        '403': b'HTTP/1.1 403 Forbidden\r\n\r\n<h1>403 FORBIDDEN</h1>',
        '404': b'HTTP/1.1 404 Not Found\r\n\r\n<h1>404 NOT FOUND</h1>',
    }
    return r.get(code, b'')


def initialized_render():
    dictionary = path.dirname(path.dirname(__file__))
    template_path = path.join(dictionary, 'templates')
    loader = FileSystemLoader(template_path)
    env = Environment(loader=loader)
    return env


class TemplateRender:
    env = initialized_render()

    @classmethod
    def render(cls, filename: str, *args, **kwargs) -> str:
        template = cls.env.get_template(filename)
        return template.render(*args, **kwargs)


def current_user(request):
    if 'session_id' in request.cookies:
        session_id = request.cookies['session_id']
        user = Session.find_user(session_id)
        if user is not None:
            return user
        else:
            return User.guest()
    else:
        return User.guest()


def token_required(route_function):
    @wraps(route_function)
    def r(request):
        if request.method == 'GET':
            token = request.query['token']
        else:
            token = request.form()['token']

        u = current_user(request)
        if token_checked(u.id, token):
            return route_function(request)
        else:
            return error(request, 403)

    return r


def api_token_required(route_function):
    @wraps(route_function)
    def r(request):
        u = current_user(request)
        token = request.headers['X-CSRF-TOKEN']
        if token_checked(u.id, token):
            return route_function(request)
        else:
            return error(request, 403)

    return r


def login_required(route_function):
    @wraps(route_function)
    def r(request):
        user = current_user(request)
        if user.is_guest():
            return redirect('/todo/login')
        else:
            return route_function(request)

    return r


def todo_same_user_required(route_function):
    @wraps(route_function)
    def r(request):
        user = current_user(request)
        if request.method == 'GET':
            todo_id = request.query['id']
        else:
            todo_id = request.form()['id']

        todo = Todo.find_by(id=int(todo_id))
        if todo.user_id == user.id:
            return route_function(request)
        else:
            return redirect('/todo/login')

    return r


def api_todo_same_user_required(route_function):
    @wraps(route_function)
    def r(request):
        user = current_user(request)
        if request.method == 'GET':
            todo_id = request.query['id']
        else:
            todo_id = request.json()['id']

        todo = Todo.find_by(id=int(todo_id))
        if todo.user_id == user.id:
            return route_function(request)
        else:
            return redirect('/todo/login')

    return r
