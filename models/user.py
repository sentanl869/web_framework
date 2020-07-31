from models import Model
from models.user_role import UserRole
from hashlib import sha256
from os import getenv


class User(Model):
    sql_create = '''
    CREATE TABLE `user` (
        `id` INT NOT NULL AUTO_INCREMENT,
        `username` VARCHAR(45) NOT NULL,
        `password` CHAR(64) NOT NULL,
        `role` ENUM('guest', 'normal', 'admin') NOT NULL,
        PRIMARY KEY (`id`)
    )'''

    def __init__(self, form) -> None:
        super().__init__(form)
        self.username = form['username']
        self.password = form['password']
        self.role = form.get('role', UserRole.normal)

    @staticmethod
    def guest():
        form = dict(
            role=UserRole.guest,
            username='Guest',
            password='Guest'
        )
        u = User(form)
        return u

    @staticmethod
    def salted_password(password: str) -> str:
        salt = getenv('salt')
        password = sha256(password.encode('ascii')).hexdigest()
        salted = password + salt
        hashed = sha256(salted.encode('ascii')).hexdigest()
        return hashed

    @staticmethod
    def register_check(username: str, password: str) -> tuple:
        user = User.find_by(username=username)
        if user is not None:
            error_code = '1'
            return False, error_code
        status = username.find(' ')
        if status != -1:
            error_code = '2'
            return False, error_code
        username_length = len(username)
        if username_length < 2:
            error_code = '3'
            return False, error_code
        password_length = len(password)
        if password_length < 2:
            error_code = '3'
            return False, error_code
        return True, ''

    @classmethod
    def register(cls, form: dict) -> tuple:
        username: str = form['username']
        password: str = form['password']
        check_passed, error_code = cls.register_check(username=username, password=password)
        if check_passed:
            form['password'] = cls.salted_password(password)
            u = User.new(form)
            return u, ''
        else:
            error_message = {
                '1': '该用户名已存在',
                '2': '用户名不允许包含空格',
                '3': '用户名和密码长度必须大于2',
            }
            result = error_message.get(error_code, '未知错误')
            return User.guest(), result

    @classmethod
    def login(cls, form: dict) -> tuple:
        username: str = form['username']
        password: str = form['password']
        salted = cls.salted_password(password)
        u = User.find_by(username=username, password=salted)
        if u is not None:
            return u, ''
        else:
            result = '用户名或密码错误'
            return User.guest(), result

    def is_guest(self) -> bool:
        return self.role == UserRole.guest
