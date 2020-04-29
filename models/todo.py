from models import Model


class Todo(Model):
    sql_create = '''
    CREAT TABLE {} (
        `id` INT NOT NULL AUTO_INCREMENT,
        `title` VARCHAR(140) NOT NULL,
        `user_id` INT NOT NULL,
        `created_time` INT NOT NULL,
        `updated_time` INT NOT NULL,
        PRIMARY KEY (`id`)
    )'''

    def __init__(self, form: dict):
        super().__init__(form)
        self.user_id = form['user_id']
        self.created_time = form['created_time']
        self.updated_time = form['updated_time']
