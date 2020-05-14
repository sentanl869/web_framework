let apiTodoAll = function (callback) {
    let path = '/api/todo/all';
    ajax('GET', path, '', callback);
};

let todoTemplate = function (todo, num) {
    return`
        <div class="todo-cell" data-id="${todo.id}">
            <span class="todo-title">${num} : ${todo.title}</span>
            <button class="todo-edit">编辑</button>
            <button class="todo-delete">删除</button>
        </div>
    `;
};

let insertTodo = function (todo, num = null) {
    let todoCell = todoTemplate(todo, num);
    let todoList = document.querySelector('#id-todo-list');
    todoList.insertAdjacentHTML('beforeend', todoCell)
};

let loadTodos = function () {
    apiTodoAll(function (todos) {
        for (let i = 0; i < todos.length; i++) {
            let todo = todos[i]
            insertTodo(todo, i + 1)
        }
    });
};

let bindEventTodo = function () {

};

let __main = function () {
    bindEventTodo();
    loadTodos();
};

__main();