from models import Model
from models.user_role import UserRole


class User(Model):
    sql_create = '''
    CREATE TABLE `user` (
        `id` INT NOT NULL AUTO_INCREMENT,
        `username` VARCHAR(45) NOT NULL,
        `password` CHAR(64) NOT NULL,
        `role` ENUM('guest', 'normal', 'admin') NOT NULL,
        PRIMARY KEY (`id`)
    )'''

    def __init__(self, form):
        super().__init__(form)
        self.username = form['username']
        self.password = form['password']
        self.role = form.get('role', UserRole.normal)

    @classmethod
    def guest(cls):

        form = dict(
            role=UserRole.guest,
            username='Guest',
            password='Guest'
        )
        u = User(form)
        return u

    def is_guest(self):
        return self.role == UserRole.guest
