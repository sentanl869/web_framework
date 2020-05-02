from routes import (
    TemplateRender,
    html_response,
    redirect,
    login_required,
    current_user,
)
from models.todo import Todo


@login_required
def index(request) -> bytes:
    todos = Todo.find_all()
    body = TemplateRender.render('todo_index.html', todos=todos)
    return html_response(body)


@login_required
def add(request):
    form = request.form()
    user = current_user(request)
    todo = Todo.add(form, user.id)
    return redirect('/todo')


def route_dict() -> dict:
    d = {
        '/todo': index,
        '/todo/add': add
    }
    return d
