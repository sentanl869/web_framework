from routes import (
    TemplateRender,
    html_response,
    redirect,
    login_required,
    current_user,
    todo_same_user_required,
    csrf_token_required,
)
from models import token_created
from models.todo import Todo


@login_required
def ajax_index(request) -> bytes:
    user = current_user(request)
    todos = Todo.find_all(user_id=user.id)
    body = TemplateRender.render('todo_ajax.html', todos=todos)
    return html_response(body)


@login_required
def index(request) -> bytes:
    user = current_user(request)
    token = token_created(user.id)
    todos = Todo.find_all(user_id=user.id)
    body = TemplateRender.render('todo_index.html', todos=todos, token=token)
    return html_response(body)


@login_required
@csrf_token_required
def add(request) -> bytes:
    form = request.form()
    user = current_user(request)
    todo = Todo.add(form, user.id)
    return redirect('/todo')


@login_required
@csrf_token_required
@todo_same_user_required
def edit(request) -> bytes:
    query = request.query
    todo_id = query['id']
    user = current_user(request)
    token = token_created(user.id)
    todo = Todo.find_by(id=todo_id)
    body = TemplateRender.render('todo_edit.html', todo=todo, token=token)
    return html_response(body)


@login_required
@csrf_token_required
@todo_same_user_required
def update(request) -> bytes:
    form = request.form()
    todo_id = int(form['id'])
    title = form['title']
    todo = Todo.update(todo_id, title=title)
    return redirect('/todo')


@login_required
@csrf_token_required
@todo_same_user_required
def delete(request) -> bytes:
    query = request.query
    todo_id = int(query['id'])
    Todo.delete(todo_id)
    return redirect('/todo')


def route_dict() -> dict:
    d = {
        '/': ajax_index,
        '/todo': index,
        '/todo/add': add,
        '/todo/edit': edit,
        '/todo/update': update,
        '/todo/delete': delete,
    }
    return d
