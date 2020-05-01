from routes import (
    TemplateRender,
    html_response,
    login_required,
)


@login_required
def index(request) -> bytes:
    body = TemplateRender.render('todo_index.html')
    return html_response(body)


def route_dict() -> dict:
    d = {
        '/todo': index
    }
    return d
