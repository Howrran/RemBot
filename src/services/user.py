"""
User CRUD operations in DB
"""
from src.models import User
from src.config import DB, DEFAULT_INTERVAL
from src.utils.decorators import transaction_decorator
from src.utils.errors import NotExist


class UserService():
    """
    Class with CRUD methods
    """

    @staticmethod
    @transaction_decorator
    def create(username, telegram_id, interval=DEFAULT_INTERVAL):
        """
        Create new user or return user object if already exists

        :param username: str
        :param telegram_id: int
        :param interval: int
        :return: user object
        """
        user = UserService.filter(telegram_id=telegram_id)

        if user:
            return user[0]

        user = User(username=username, telegram_id=telegram_id, interval=interval)
        DB.session.add(user)
        return user

    @staticmethod
    def get_by_id(user_id):
        """
        Get user by id

        :param id: int
        :return: user or none
        """
        user = DB.session.query(User).get(user_id)
        return user

    @staticmethod
    @transaction_decorator
    def update(user_id, username=None, telegram_id=None, interval=None):
        """
        Update user info in database

        :param user_id: int
        :param username: str
        :param telegram_id: int
        :param interval: int
        :return: user object
        """
        user = UserService.get_by_id(user_id)

        if user is None:
            raise NotExist()

        if username is not None:
            user.username = username
        if telegram_id is not None:
            user.telegram_id = telegram_id
        if interval is not None:
            user.interval = interval

        DB.session.merge(user)

        return user

    @staticmethod
    @transaction_decorator
    def delete(user_id):
        """
        Delete user from database

        :param user_id: int
        :return: True or None
        """
        user = UserService.get_by_id(user_id)

        if user is None:
            raise NotExist()

        DB.session.delete(user)
        return True

    @staticmethod
    def filter(username=None, telegram_id=None, interval=None):
        """
        Get list of user objects by parameters

        :param username: str
        :param telegram_id: int
        :param interval: int
        :return: list
        """
        data = {}

        if username is not None:
            data['username'] = username
        if telegram_id is not None:
            data['telegram_id'] = telegram_id
        if interval is not None:
            data['interval'] = interval

        users = DB.session.query(User).filter_by(**data).all()
        return users
