import pymysql
import secret
import config
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
# from utiles import log


def random_string(random_range: int = 16) -> str:
    seed = ascii_letters + digits
    r = ''.join(choice(seed) for i in range(random_range))
    return r


def expired(expired_time: int) -> bool:
    now = int(time())
    result = expired_time < now
    return result


def signature_created(message: str) -> str:
    content = message + secret.token_key
    result = sha256(content.encode('ascii')).hexdigest()
    return result


def token_created(user_id, _expired: int = 3600):
    user_str = str(user_id)
    expired_time = int(time()) + _expired
    message = ';'.join([user_str, str(expired_time)])
    signature = signature_created(message)
    message_base64 = b64encode(message.encode())
    signature_base64 = b64encode(signature.encode())
    token = '.'.join([message_base64.decode(), signature_base64.decode()])
    return token


def token_checked(_id: int, token: str) -> bool:
    message_base64, signature_base64 = token.split('.', 1)
    message = b64decode(message_base64.encode())
    message = message.decode()
    user_id, expired_time = message.split(';', 1)
    signature = signature_created(message)
    signature_check = b64decode(signature_base64.encode())
    signature_check = signature_check.decode()

    try:
        return _id == int(user_id) and not expired(int(expired_time)) and signature == signature_check
    except ValueError:
        return False


class Model:
    connection = None

    @classmethod
    def init_db(cls):
        cls.connection = pymysql.connect(
            host=config.db_host,
            user=config.db_user,
            password=secret.mysql_password,
            db=config.db_name,
            charset='utf8mb4',
            cursorclass=pymysql.cursors.DictCursor
        )

    def __init__(self, form: dict):
        self.id = form.get('id', None)

    @classmethod
    def table_name(cls):
        return '`{}`'.format(cls.__name__).lower()

    @classmethod
    def insert(cls, form: dict):
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
        # log(sql_insert)
        values = tuple(form.values())

        with cls.connection.cursor() as cursor:
            cursor.execute(sql_insert, values)
            _id = cursor.lastrowid
        cls.connection.commit()
        return _id

    @classmethod
    def update(cls, _id: int, **kwargs):
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
        # log(sql_update)
        values = list(kwargs.values())
        values.append(_id)
        values = tuple(values)

        with cls.connection.cursor() as cursor:
            cursor.execute(sql_update, values)
        cls.connection.commit()

    @classmethod
    def delete(cls, _id: int):
        sql_delete = '''
        DELETE FROM
            {}
        WHERE
            `id`=%s
        '''.format(cls.table_name())
        # log(sql_delete)
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
        # log(sql_select)
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
        # log(sql_select)
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
