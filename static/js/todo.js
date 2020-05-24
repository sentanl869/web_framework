let todoTemplate = function (todo) {
    return`
        <li class="todo-cell" data-id="${todo.id}">
            <span class="todo-title">${todo.title}</span>
            <button class="todo-edit">编辑</button>
            <button class="todo-delete">完成</button>
        </li>
    `;
};

let todoEditTemplate = function (title) {
    return `
        <div class="todo-update-form">
            <input class="todo-update-input" value="${title}"/>
            <button class="todo-update">更新</button>
        </div>
    `;
};

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

let apiTodoUpdate = function (form, callback) {
    let path = '/api/todo/update';
    ajax('POST', path, form, callback);
};

let insertTodo = function (todo) {
    let todoCell = todoTemplate(todo);
    let todoList = document.querySelector('#id-todo-list');
    todoList.insertAdjacentHTML('beforeend', todoCell);
};

let insertEditForm = function (title, todoCell) {
    let editForm = todoEditTemplate(title);
    todoCell.insertAdjacentHTML('beforeend', editForm);
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
            input.value = '';
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

let bindEventTodoEdit = function () {
    let bind = document.querySelector('#id-todo-list');
    bind.addEventListener('click', function (event) {
        let self = event.target;
        if (self.classList.contains('todo-edit')) {
            let todoCell = self.closest('.todo-cell');
            let todoSpan = todoCell.querySelector('.todo-title');
            let title = todoSpan.innerText;
            insertEditForm(title, todoCell);
            self.disabled = true;
        }
    });
};

let bindEventTodoUpdate = function () {
    let bind = document.querySelector('#id-todo-list');
    bind.addEventListener('click', function (event) {
        let self = event.target;
        if (self.classList.contains('todo-update')) {
            let todoCell = self.closest('.todo-cell');
            let todoId = todoCell.dataset['id'];
            let updateContent = todoCell.querySelector('.todo-update-input');
            let title = updateContent.value;
            let form = {
                id: todoId,
                title: title,
            };
            apiTodoUpdate(form, function (todo) {
                let todoSpan = todoCell.querySelector('.todo-title');
                todoSpan.innerText = todo.title;
                let editForm = todoCell.querySelector('.todo-update-form');
                editForm.remove();
                let editButton = todoCell.querySelector('.todo-edit');
                editButton.disabled = false;
            });
        }
    });
};

let bindEventTodo = function () {
    bindEventTodoAdd();
    bindEventTodoDelete();
    bindEventTodoEdit();
    bindEventTodoUpdate();
};

let __main = function () {
    bindEventTodo();
    loadTodos();
};

__main();