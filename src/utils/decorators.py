"""Project decorators"""
import functools
import sqlite3

from sqlite3 import (
    OperationalError,
    IntegrityError,
    ProgrammingError
)
from config import DATABASE
from src.utils.errors import CustomException


def database_update_decorator(func):
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

        except (OperationalError, IntegrityError, ProgrammingError, CustomException) as err:
            print(err)
            return None

    return wrapper
