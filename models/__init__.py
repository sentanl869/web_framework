import pymysql
import secret
import config
# from utiles import log


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
            if result is None:
                return None
            else:
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

        ms = list()
        with cls.connection.cursor() as cursor:
            cursor.execute(sql_select, values)
            result = cursor.fetchall()
            for line in result:
                m = cls(line)
                ms.append(m)
            return ms
