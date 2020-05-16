from routes import (
    json_response,
    current_user,
    login_required,
)
from models.todo import Todo
# from utiles import log


@login_required
def api_all(request) -> bytes:
    u = current_user(request)
    todos = Todo.json_all(u.id)
    return json_response(todos)


@login_required
def api_add(request) -> bytes:
    form = request.json()
    u = current_user(request)
    t = Todo.add(form, u.id)
    return json_response(t.json())


@login_required
def api_delete(request) -> bytes:
    todo_id = request.query['id']
    Todo.delete(todo_id)
    r = dict()
    return json_response(r)


def route_dict() -> dict:
    d = {
        '/api/todo/all': api_all,
        '/api/todo/add': api_add,
        '/api/todo/delete': api_delete,
    }
    return d
