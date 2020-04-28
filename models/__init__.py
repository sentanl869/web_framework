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
        sql_keys = ', '.join(['`{}`'.format(k) for k in form.keys()])
        sql_value = ', '.join(['%s'] * len(form))
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
    def new(cls, form: dict):
        m = cls(form)
        _id = cls.insert(m.__dict__)
        m.id = _id
        return m
