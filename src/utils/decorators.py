import functools
import sqlite3

from config import DATABASE
from sqlite3 import (
    OperationalError,
    IntegrityError
)

def database_decorator(func):
    """
    Connection decorator
    :param func: function to decorate
    :return: function wrapper
    """
    @functools.wraps(func)
    def wrapper(*args, **kwargs):
        """
        Function decorator
        :param *args: args
        :param **kwargs: kwargs
        """
        try:
            conn = sqlite3.connect(DATABASE)
            cursor = conn.cursor()
            result = func(cursor, *args, **kwargs)
            conn.commit()
            conn.close()

            return result

        except (OperationalError, IntegrityError) as err:
            print(err)
            return None

    return wrapper
