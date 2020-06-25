"""
Module for operating with user`s words in database
"""
from src.utils.errors import NotExist
from src.utils.decorators import database_update_decorator


class UserWordsCRUD():
    """
        Class with db operations for user`s words
        """

    # positions in tuple
    ID = 0
    USER_ID = 1
    WORD_ID = 2
    STATUS = 3

    @staticmethod
    @database_update_decorator
    def select_all(cursor):
        """
        Get all users_words from the database

        :param cursor: used in decorator
        :return: list: users_words
        """
        sql = 'SELECT * FROM user_words'

        cursor.execute(sql)
        users_words = cursor.fetchall()

        return users_words

    @staticmethod
    @database_update_decorator
    def get_by_id(cursor, record_id):
        """
        Get record from the database by record_id

        :param cursor: used in decorator
        :param record_id: int or str
        :return: tuple or None
        """
        record_id = str(record_id)
        sql = 'SELECT * from user_words where id=?'
        record = cursor.execute(sql, (record_id)).fetchone()

        return record

    @staticmethod
    @database_update_decorator
    def add_record(cursor, user_id, word_id, status):
        """
        Add new record to db

        :param cursor: used in decorator
        :param user_id:
        :param word_id:
        :param status:
        :return: True
        """
        sql = '''INSERT INTO user_words
                     (user_id, word_id, status)
                     VALUES (?,?,?)'''

        cursor.execute(sql, (user_id, word_id, status))

        return True

    @staticmethod
    @database_update_decorator
    def select_user_words(cursor, user_id):
        """
        Get all words of user from the database

        :param cursor: used in decorator
        :param user_id: int in decorator
        :return: list: user_words
        """
        user_id = str(user_id)
        sql = 'SELECT * FROM user_words where user_id=?'

        cursor.execute(sql, user_id)
        user_words = cursor.fetchall()

        return user_words

    @staticmethod
    @database_update_decorator
    def select_word_users(cursor, word_id):
        """
        Get all users of the word from the database

        :param cursor: used in decorator
        :param word_id: int in decorator
        :return: list: users of that word
        """
        word_id = str(word_id)
        sql = 'SELECT * FROM user_words where word_id=?'

        cursor.execute(sql, word_id)
        user_words = cursor.fetchall()

        return user_words

    @staticmethod
    @database_update_decorator
    def update_record(cursor, record_id, user_id=None, word_id=None, status=None):
        """
        Update record in db

        :param cursor: used in decorator
        :param record_id: int record id
        :param user_id: int
        :param word_id: int
        :param status: int (0\1)
        :return:
        """
        if user_id is None and word_id is None and status is None:
            return None

        record = UserWordsCRUD.get_by_id( # pylint: disable=no-value-for-parameter
            record_id=record_id)

        if record is None:
            raise NotExist()

        user_id = user_id if user_id else record[UserWordsCRUD.USER_ID]
        word_id = word_id if word_id else record[UserWordsCRUD.WORD_ID]
        status = status if status else record[UserWordsCRUD.STATUS]

        sql = '''UPDATE user_words
                     set user_id= ?, word_id = ?, status = ?
                     where id = ?
                    '''
        cursor.execute(sql,
                       (user_id, word_id, status, record_id)
                       )
        record = UserWordsCRUD.get_by_id( #pylint: disable=no-value-for-parameter
            record_id=record_id)

        return record
