import pymysql
from os import getenv
from time import time
from secrets import choice
from hashlib import sha256
from base64 import (
    b64encode,
    b64decode,
)
from string import (
    ascii_letters,
    digits,
)


def random_string(random_range: int = 16) -> str:
    seed = ascii_letters + digits
    r = ''.join(choice(seed) for i in range(random_range))
    return r


def expired(expired_time: int) -> bool:
    now = int(time())
    result = expired_time < now
    return result


def signature_created(message: str) -> str:
    token_key = getenv('token_key')
    content = message + token_key
    result = sha256(content.encode('ascii')).hexdigest()
    return result


def base64_created(content: str) -> str:
    result = b64encode(content.encode())
    return result.decode()


def base64_decoded(content: str) -> str:
    result = b64decode(content.encode())
    return result.decode()


def token_created(user_id: int, _expired: int = 3600) -> str:
    user_str = str(user_id)
    expired_time: int = int(time()) + _expired
    message = ';'.join([user_str, str(expired_time)])
    signature = signature_created(message)
    token = '.'.join([base64_created(message), base64_created(signature)])
    return token


def token_checked(_id: int, token: str) -> bool:
    try:
        message_base64, signature_base64 = token.split('.', 1)
        message = base64_decoded(message_base64)
        user_id, expired_time = message.split(';', 1)
        signature = signature_created(message)
        signature_check = base64_decoded(signature_base64)
        return _id == int(user_id) and not expired(int(expired_time)) and signature == signature_check
    except ValueError:
        return False


class Model:
    connection = None

    @classmethod
    def init_db(cls) -> None:
        db_host = getenv('db_host')
        db_user = getenv('db_user')
        db_name = getenv('db_name')
        mysql_password = getenv('mysql_password')
        cls.connection = pymysql.connect(
            host=db_host,
            user=db_user,
            password=mysql_password,
            db=db_name,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

    def __init__(self, form: dict) -> None:
        self.id = form.get('id', None)

    @classmethod
    def table_name(cls) -> str:
        return '`{}`'.format(cls.__name__).lower()

    @classmethod
    def insert(cls, form: dict) -> int:
        form.pop('id')
        sql_keys = ', '.join(
            ['`{}`'.format(k) for k in form.keys()]
        )
        sql_value = ', '.join(
            ['%s'] * len(form)
        )
        sql_insert = '''
        INSERT INTO
            {} ({})
        VALUE
            ({})
        '''.format(
            cls.table_name(),
            sql_keys,
            sql_value,
        )
        values = tuple(form.values())

        with cls.connection.cursor() as cursor:
            cursor.execute(sql_insert, values)
            _id = cursor.lastrowid
        cls.connection.commit()
        return _id

    @classmethod
    def update(cls, _id: int, **kwargs) -> None:
        sql_set = ', '.join(
            ['`{}`=%s'.format(k) for k in kwargs.keys()]
        )
        sql_update = '''
        UPDATE
            {}
        SET
            {}
        WHERE
            `id`=%s
        '''.format(
            cls.table_name(),
            sql_set,
        )
        values = list(kwargs.values())
        values.append(_id)
        values = tuple(values)

        with cls.connection.cursor() as cursor:
            cursor.execute(sql_update, values)
        cls.connection.commit()

    @classmethod
    def delete(cls, _id: int) -> None:
        sql_delete = '''
        DELETE FROM
            {}
        WHERE
            `id`=%s
        '''.format(cls.table_name())
        with cls.connection.cursor() as cursor:
            cursor.execute(sql_delete, (_id,))
        cls.connection.commit()

    @classmethod
    def new(cls, form: dict):
        m = cls(form)
        _id = cls.insert(m.__dict__)
        m.id = _id
        return m

    @classmethod
    def find_by(cls, **kwargs):
        sql_select = '''
        SELECT * FROM
            {}
        '''.format(cls.table_name())
        sql_and = ' AND '.join(
            ['`{}`=%s'.format(k) for k in kwargs.keys()]
        )
        sql_where = '''
        WHERE
            {}
        '''.format(sql_and)
        sql_limit = 'LIMIT 1;'
        sql_select = '{}{}{}'.format(sql_select, sql_where, sql_limit)
        values = tuple(kwargs.values())

        with cls.connection.cursor() as cursor:
            cursor.execute(sql_select, values)
            result = cursor.fetchone()
            if result is not None:
                return cls(result)

    @classmethod
    def find_all(cls, **kwargs) -> list:
        sql_select = '''
        SELECT * FROM
            {}
        '''.format(cls.table_name())

        if len(kwargs) > 0:
            sql_and = ' AND '.join(
                ['`{}`=%s'.format(k) for k in kwargs.keys()]
            )
            sql_where = '''
            WHERE
                {}
            '''.format(sql_and)
            sql_select = '{}{}'.format(sql_select, sql_where)
        values = tuple(kwargs.values())

        with cls.connection.cursor() as cursor:
            cursor.execute(sql_select, values)
            result = cursor.fetchall()
            if result is not None:
                for line in result:
                    m = cls(line)
                    yield m

    def json(self) -> dict:
        return self.__dict__

    @classmethod
    def json_all(cls, user_id: int = None) -> list:
        ms = cls.find_all(user_id=user_id)
        js = [m.json() for m in ms]
        return js
