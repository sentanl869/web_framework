from models import Model
from models.user_role import UserRole
from secret import salt
from hashlib import sha256
from utiles import log


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
        salted = password + salt
        hashed = sha256(salted.encode('ascii')).hexdigest()
        return hashed

    @classmethod
    def register(cls, form: dict):
        username: str = form['username']
        password: str = form['password']
        index = username.find(' ')
        if index == -1:
            status = len(username) > 2 and len(password) > 2
            if status:
                form['password'] = cls.salted_password(password)
                u = User.new(form)
                result = '注册成功'
                return u, result
            else:
                result = '用户名与密码长度必须大于2'
                return User.guest(), result
        else:
            result = '用户名不允许包含空格'
            return User.guest(), result

    @classmethod
    def login(cls, form: dict):
        username: str = form['username']
        password: str = form['password']
        salted = cls.salted_password(password)
        u = User.find_by(username=username, password=salted)
        if u is not None:
            result = '登录成功'
            return u, result
        else:
            result = '用户名或密码错误'
            return User.guest(), result

    def is_guest(self) -> bool:
        return self.role == UserRole.guest
