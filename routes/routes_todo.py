from routes import (
    TemplateRender,
    html_response,
)


def index(request) -> bytes:
    body = TemplateRender.render('todo_index.html')
    return html_response(body)


def route_dict() -> dict:
    d = {
        '/todo': index
    }
    return d
