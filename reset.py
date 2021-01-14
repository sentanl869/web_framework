import os

import pymysql
from dotenv import load_dotenv

from models import Model
from models.todo import Todo
from models.user import User
from models.session import Session


def recreate_table(cursor: pymysql.cursors.DictCursor) -> None:
    cursor.execute(Todo.sql_create)
    cursor.execute(User.sql_create)
    cursor.execute(Session.sql_create)


def recreate_database() -> None:
    load_dotenv()
    db_name = os.environ.get('db_name')
    db_host = os.environ.get('db_host')
    db_user = os.environ.get('db_user')
    mysql_password = os.environ.get('mysql_password')

    connection = pymysql.connect(
            host=db_host,
            user=db_user,
            password=mysql_password,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )
    with connection.cursor() as cursor:
        cursor.execute(
            'DROP DATABASE IF EXISTS `{}`'.format(
                db_name
            )
        )
        cursor.execute(
            'CREATE DATABASE `{}` DEFAULT CHARACTER SET utf8mb4'.format(
                db_name
            )
        )
        cursor.execute('USE `{}`'.format(db_name))

        recreate_table(cursor)

    connection.commit()
    connection.close()


def generate_user() -> None:
    Model.init_db()
    d = dict(
        username='test',
        password='1231234',
    )
    User.register(d)
    User.connection.close()


if __name__ == '__main__':
    recreate_database()
    generate_user()
