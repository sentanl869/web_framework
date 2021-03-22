const todoTemplate = (todo) => {
    let content = HTMLEscaped(todo.title)
    return`
        <li class="todo-cell" data-id="${todo.id}">
            <span class="todo-title">${content}</span>
            <button class="todo-edit">编辑</button>
            <button class="todo-delete">完成</button>
        </li>
    `
}

const todoEditTemplate = (title) => {
    return `
        <div class="todo-update-form">
            <input class="todo-update-input" value="${title}"/>
            <button class="todo-update">更新</button>
        </div>
    `
}

const token = document.querySelector('meta[name=token]').content

const apiTodoAll = (callback) => {
    const path = '/api/todo/all'
    ajax('GET', path, '', token, callback)
}

const apiTodoAdd = (form, callback) => {
    const path = '/api/todo/add'
    ajax('POST', path, form, token, callback)
}

const apiTodoDelete = (todoId, callback) => {
    let path = `/api/todo/delete?id=${todoId}`
    ajax('GET', path, '', token, callback)
}

const apiTodoUpdate = (form, callback) => {
    const path = '/api/todo/update'
    ajax('POST', path, form, token, callback)
}

const insertTodo = (todo) => {
    let todoCell = todoTemplate(todo)
    let todoList = document.querySelector('#id-todo-list')
    todoList.insertAdjacentHTML('beforeend', todoCell)
}

const insertEditForm = (title, todoCell) => {
    let editForm = todoEditTemplate(title)
    todoCell.insertAdjacentHTML('beforeend', editForm)
}

const loadTodos = () => {
    apiTodoAll((todos) => {
        for (let i = 0; i < todos.length; i++) {
            let todo = todos[i]
            insertTodo(todo)
        }
    })
}

const bindEventTodoAdd = () => {
    let bind = document.querySelector('#id-button-add')
    bind.addEventListener('click', () => {
        let input = document.querySelector('#id-input-todo')
        let title = input.value
        let form = {
            title: title
        }
        apiTodoAdd(form, (todo) => {
            insertTodo(todo)
            input.value = ''
        })
    })
}

const bindEventTodoDelete = () => {
    let bind = document.querySelector('#id-todo-list')
    bind.addEventListener('click', (event) => {
        let self = event.target
        if (self.classList.contains('todo-delete')) {
            let todoId = self.parentElement.dataset['id']
            apiTodoDelete(todoId, () => {
                self.parentElement.remove()
            })
        }
    })
}

const bindEventTodoEdit = () => {
    let bind = document.querySelector('#id-todo-list')
    bind.addEventListener('click', (event) => {
        let self = event.target
        if (self.classList.contains('todo-edit')) {
            let todoCell = self.closest('.todo-cell')
            let todoSpan = todoCell.querySelector('.todo-title')
            let title = todoSpan.innerText
            insertEditForm(title, todoCell)
            self.disabled = true
        }
    })
}

const bindEventTodoUpdate = () => {
    let bind = document.querySelector('#id-todo-list')
    bind.addEventListener('click', (event) => {
        let self = event.target
        if (self.classList.contains('todo-update')) {
            let todoCell = self.closest('.todo-cell')
            let todoId = todoCell.dataset['id']
            let updateContent = todoCell.querySelector('.todo-update-input')
            let title = updateContent.value
            let form = {
                id: todoId,
                title: title,
            }
            apiTodoUpdate(form, (todo) => {
                let todoSpan = todoCell.querySelector('.todo-title')
                todoSpan.innerText = todo.title
                let editForm = todoCell.querySelector('.todo-update-form')
                editForm.remove()
                let editButton = todoCell.querySelector('.todo-edit')
                editButton.disabled = false
            })
        }
    })
}

const bindEventTodo = () => {
    bindEventTodoAdd()
    bindEventTodoDelete()
    bindEventTodoEdit()
    bindEventTodoUpdate()
}

const __main = () => {
    bindEventTodo()
    loadTodos()
}

__main()