from models import (
    Model,
    random_string,
    expired,
)
from models.user import User
from time import time
# from utiles import log


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
    def save(cls, user_id, _expired: int = 3600):
        sql_insert = '''
        INSERT INTO
            `session` (`session_id`, `user_id`, `expired_time`)
        VALUES
            (%s, %s, %s);
        '''

        with cls.connection.cursor() as cursor:
            expired_time = int(time()) + _expired
            session_id = random_string()
            cursor.execute(sql_insert, (session_id, user_id, expired_time))
        cls.connection.commit()

        return session_id

    @classmethod
    def find_user(cls, session_id):
        sql_find = '''
        SELECT
            `user_id`, `expired_time`
        FROM
            `session`
        WHERE
            `session_id`=%s;
        '''

        with cls.connection.cursor() as cursor:
            cursor.execute(sql_find, session_id)
            r = cursor.fetchall()
            if len(r) > 0:
                user_id = int(r[0]['user_id'])
                expired_time = int(r[0]['expired_time'])
                if not expired(expired_time):
                    u = User.find_by(id=user_id)
                else:
                    u = User.guest()
            else:
                u = User.guest()

        return u
