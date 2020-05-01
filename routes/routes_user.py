from routes import (
    TemplateRender,
    html_response,
    redirect,
)
from urllib import parse
from models.user import User
# from utiles import log


def login_view(request) -> bytes:
    body = TemplateRender.render('login.html')
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


def route_dict() -> dict:
    d = {
        '/todo/login': login_view,
        '/todo/register': register_view,
        '/todo/user/register': register,
    }
    return d
