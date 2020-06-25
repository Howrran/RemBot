"""
Module for operating with user in database
"""
from config import DEFAULT_INTERVAL
from src.utils.errors import UserNotExist
from src.utils.decorators import database_update_decorator


class UserCRUD():
    """
    Class with db operations for user
    """
    # positions in user tuple
    ID = 0
    USERNAME = 1
    TELEGRAM_ID = 2
    INTERVAL = 3

    @staticmethod
    @database_update_decorator
    def select_all_users(cursor):
        """
        Get all users from the database

        :param cursor: used in decorator
        :return: list: users
        """
        sql = 'SELECT * FROM users'

        cursor.execute(sql)
        users = cursor.fetchall()

        return users

    @staticmethod
    @database_update_decorator
    def add_user(cursor, username, telegram_id, interval=DEFAULT_INTERVAL):
        """
        add new user to the database

        :param cursor: used in decorator
        :param username: str
        :param telegram_id: int
        :param interval: int
        :return: True Or None if operation fail
        """
        sql = '''INSERT INTO users
                 (username, telegram_id, interval)
                 VALUES (?,?,?)'''

        cursor.execute(sql, (username, telegram_id, interval))

        return True

    @staticmethod
    @database_update_decorator
    def get_user_by_id(cursor, user_id):
        """
        Get user from the database by id

        :param cursor: used in decorator
        :param user_id: int or str
        :return: tuple or None
        """
        user_id = str(user_id)
        sql = 'SELECT * from users where id=?'
        user = cursor.execute(sql, (user_id)).fetchone()

        return user

    @staticmethod
    @database_update_decorator
    def user_filter(cursor, username=None, telegram_id=None):
        """
        Get users from the database by parameters

        :param cursor: used in decorator
        :param username: str
        :param telegram_id: int
        :return: list or None
        """
        data = {}

        if username:
            data['username'] = username
        if telegram_id:
            data['telegram_id'] = telegram_id

        sql = 'SELECT * from users where username=? or telegram_id=?'

        output = cursor.execute(sql,
                                (data.get('username'), data.get('telegram_id'))
                                ).fetchall()

        return output

    @staticmethod
    @database_update_decorator
    def update_user(cursor, user_id, username=None, interval=None):
        """
        Update user`s information in database

        :param cursor: used in decorator
        :param user_id: int
        :param username: str
        :param interval: int
        :return: tuple
        """

        user = UserCRUD.get_user_by_id(user_id=user_id)  # pylint: disable=no-value-for-parameter

        if user is None:
            raise UserNotExist()

        username = username if username else user[UserCRUD.USERNAME]
        interval = interval if interval else user[UserCRUD.INTERVAL]

        sql = '''UPDATE users
                 set username = ?, interval = ?
                 where id = ?
                '''
        cursor.execute(sql,
                       (username, interval, user_id)
                       )
        user = UserCRUD.get_user_by_id(user_id=user_id)  # pylint: disable=no-value-for-parameter

        return user
