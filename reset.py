import pymysql
import secret
import config
# from utiles import log
from models import Model
from models.todo import Todo
from models.user import User
from models.session import Session


def recreate_table(cursor: pymysql.cursors.DictCursor):
    cursor.execute(Todo.sql_create)
    cursor.execute(User.sql_create)
    cursor.execute(Session.sql_create)


def recreate_database():
    connection = pymysql.connect(
        host=config.db_host,
        user=config.db_user,
        password=secret.mysql_password,
        charset='utf8mb4',
        cursorclass=pymysql.cursors.DictCursor
    )

    with connection.cursor() as cursor:
        cursor.execute(
            'DROP DATABASE IF EXISTS `{}`'.format(
                config.db_name
            )
        )
        cursor.execute(
            'CREATE DATABASE `{}` DEFAULT CHARACTER SET utf8mb4'.format(
                config.db_name
            )
        )
        cursor.execute('USE `{}`'.format(config.db_name))

        recreate_table(cursor)

    connection.commit()
    connection.close()


def generate_user():
    Model.init_db()
    d = dict(
        username='test',
        password='1231234',
    )
    User.register(d)


if __name__ == '__main__':
    recreate_database()
    generate_user()
