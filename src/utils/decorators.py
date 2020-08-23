"""Project decorators"""
import functools

from sqlalchemy.exc import (
    IntegrityError,
    ProgrammingError,
    SQLAlchemyError,
    InvalidRequestError
)

from src.config import DB  # pylint: disable=no-name-in-module
from src.utils.errors import CustomException


def transaction_decorator(func):
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
        DB.session.begin(subtransactions=True)

        try:
            result = func(*args, **kwargs)
            DB.session.commit()
            return result

        except IntegrityError as ex:
            print(ex)
        except ProgrammingError as ex:
            print(ex)
        except CustomException as ex:
            print(ex)
        except InvalidRequestError as ex:
            print(ex)
        except SQLAlchemyError as ex:
            print(ex)

        DB.session.rollback()
        return None
    return wrapper
