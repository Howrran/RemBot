from src.models import User
from src.config import DB
from src.utils.decorators import transaction_decorator
from src.utils.errors import NotExist


class UserService():

    @staticmethod
    @transaction_decorator
    def create(username, telegram_id, interval):

        user = User(username=username, telegram_id=telegram_id, interval=interval)
        DB.session.add(user)
        return user


    @staticmethod
    def get_by_id(user_id):
        """
        Get user by id
        :param id:
        :return: user or none
        """
        user = DB.session.query(User).get(user_id)
        return user

    @staticmethod
    @transaction_decorator
    def update(user_id, username=None, telegram_id=None, interval=None):
        """
        Update user info in database

        :param user_id:
        :param username:
        :param telegram_id:
        :param interval:
        :return:
        """

        user = UserService.get_by_id(user_id)

        if username:
            user.username = username
        if telegram_id:
            user.telegram_id = telegram_id
        if interval:
            user.interval = interval

        DB.session.merge()

        return user

    @staticmethod
    @transaction_decorator
    def delete(user_id):
        """
        Delete user from database
        :param user_id:
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
        Check if user exist in database.

        :param username:
        :param telegram_id:
        :param interval:
        :return:
        """

        data = {}

        if username:
            data['username'] = username
        if telegram_id:
            data['telegram_id'] = telegram_id
        if interval:
            data['interval'] = interval

        users = DB.session.query(User).filter_by(**data).all()

        return users

# use = User(username="Johnatan", telegram_id=344, interval=10)
print(UserService.get_by_id(4))