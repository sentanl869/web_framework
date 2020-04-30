from routes import (
    TemplateRender,
    html_response,
)


def login_view(request):
    body = TemplateRender.render('login.html')
    return html_response(body)


def route_dict() -> dict:
    d = {
        '/todo/login': login_view
    }
    return d
