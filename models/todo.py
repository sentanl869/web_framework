from models import Model
from time import time


class Todo(Model):
    sql_create = '''
    CREATE TABLE `todo` (
        `id` INT NOT NULL AUTO_INCREMENT,
        `title` VARCHAR(140) NOT NULL,
        `user_id` INT NOT NULL,
        `created_time` INT NOT NULL,
        `updated_time` INT NOT NULL,
        PRIMARY KEY (`id`)
    )'''

    def __init__(self, form: dict):
        super().__init__(form)
        self.title = form['title']
        self.user_id = form['user_id']
        self.created_time = form['created_time']
        self.updated_time = form['updated_time']

    @classmethod
    def add(cls, form: dict, user_id: int):
        form['user_id'] = user_id
        form['created_time'] = int(time())
        form['updated_time'] = int(time())
        todo = cls.new(form)
        return todo

    @classmethod
    def update(cls, _id: int, **kwargs):
        super().update(
            _id,
            title=kwargs['title'],
            updated_time=int(time())
        )

        todo = cls.find_by(id=_id)
        return todo
