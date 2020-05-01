from models import Model
from models.user import User
from string import (
    ascii_letters,
    digits,
)
from secrets import choice
from time import time
from utiles import log


def random_string() -> str:
    seed = ascii_letters + digits
    r = ''.join(choice(seed) for i in range(16))
    return r


class Session(Model):
    sql_create = '''
    CREATE TABLE `session` (
        `id` INT NOT NULL AUTO_INCREMENT,
        `session_id` CHAR(16) NOT NULL,
        `user_id` INT NOT NULL,
        `expired_time` INT NOT NULL,
        PRIMARY KEY (`id`)
    )'''

    @classmethod
    def save(cls, user_id, expired: int = 3600):
        sql_insert = '''
        INSERT INTO
            `session` (`session_id`, `user_id`, `expired_time`)
        VALUES
            (%s, %s, %s);
        '''

        with cls.connection.cursor() as cursor:
            expired_time = time() + expired
            session_id = random_string()
            cursor.execute(sql_insert, (session_id, user_id, expired_time))
        cls.connection.commit()

        return session_id

    @classmethod
    def find_user(cls, session_id):
        sql_find = '''
        SELECT
            `user_id`
        FROM
            `session`
        WHERE
            `session_id`=%s;
        '''

        with cls.connection.cursor() as cursor:
            cursor.execute(sql_find, session_id)
            r = cursor.fetchall()
            log('***session', r)
            user_id = int(r[0]['user_id'])
            u = User.find_by(id=user_id)

        return u
