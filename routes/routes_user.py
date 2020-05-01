from routes import (
    TemplateRender,
    html_response,
    redirect,
)
from urllib import parse
from models.user import User
from models.session import Session
# from utiles import log


def login_view(request) -> bytes:
    query: dict = request.query
    result = query.get('result', '')
    result = parse.unquote_plus(result)
    body = TemplateRender.render('login.html', result=result)
    return html_response(body)


def register_view(request) -> bytes:
    query: dict = request.query
    result = query.get('result', '')
    result = parse.unquote_plus(result)
    body = TemplateRender.render('register.html', result=result)
    return html_response(body)


def register(request) -> bytes:
    form = request.form()
    user, result = User.register(form)
    return redirect('/todo/register?result={}'.format(result))


def login(request) -> bytes:
    form = request.form()
    user, result = User.login(form)

    if user.is_guest():
        return redirect('/todo/login?result={}'.format(result))
    else:
        session_id = Session.save(user.id)
        header = {
            'Set-Cookie': 'session_id={}; path=/'.format(session_id)
        }

        return redirect('/todo/login?result={}'.format(result), header)


def route_dict() -> dict:
    d = {
        '/todo/login': login_view,
        '/todo/register': register_view,
        '/todo/user/register': register,
        '/todo/user/login': login,
    }
    return d
