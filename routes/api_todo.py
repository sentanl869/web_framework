from routes import (
    json_response,
    current_user,
    login_required,
)
from models.todo import Todo


@login_required
def api_all(request) -> bytes:
    u = current_user(request)
    todos = Todo.json_all(u.id)
    return json_response(todos)


def route_dict() -> dict:
    d = {
        '/api/todo/all': api_all,
    }
    return d
