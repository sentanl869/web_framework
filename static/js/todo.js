let apiTodoAll = function (callback) {
    let path = '/api/todo/all';
    ajax('GET', path, '', callback);
};

let apiTodoAdd = function (form, callback) {
    let path = '/api/todo/add';
    ajax('POST', path, form, callback);
};

let apiTodoDelete = function (todoId, callback) {
    let path = `/api/todo/delete?id=${todoId}`;
    ajax('GET', path, '', callback);
};

let todoTemplate = function (todo) {
    return`
        <div class="todo-cell" data-id="${todo.id}">
            <span class="todo-title">${todo.title}</span>
            <button class="todo-edit">编辑</button>
            <button class="todo-delete">完成</button>
        </div>
    `;
};

let insertTodo = function (todo) {
    let todoCell = todoTemplate(todo);
    let todoList = document.querySelector('#id-todo-list');
    todoList.insertAdjacentHTML('beforeend', todoCell);
};

let loadTodos = function () {
    apiTodoAll(function (todos) {
        for (let i = 0; i < todos.length; i++) {
            let todo = todos[i];
            insertTodo(todo);
        }
    });
};

let bindEventTodoAdd = function () {
    let bind = document.querySelector('#id-button-add');
    bind.addEventListener('click', function () {
        let input = document.querySelector('#id-input-todo');
        let title = input.value;
        let form = {
            title: title
        };
        apiTodoAdd(form, function (todo) {
            insertTodo(todo);
        });
    });
};

let bindEventTodoDelete = function () {
    let bind = document.querySelector('#id-todo-list');
    bind.addEventListener('click', function (event) {
        let self = event.target;
        if (self.classList.contains('todo-delete')) {
            let todoId = self.parentElement.dataset['id'];
            apiTodoDelete(todoId, function () {
                self.parentElement.remove();
            });
        }
    });
};

let bindEventTodo = function () {
    bindEventTodoAdd();
    bindEventTodoDelete();
};

let __main = function () {
    bindEventTodo();
    loadTodos();
};

__main();