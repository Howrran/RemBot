"""
User CRUD operations in DB
"""
from src.models import UserWord
from src.config import DB
from src.utils.decorators import transaction_decorator
from src.utils.errors import NotExist


class UserWordService():
    """
    Class with CRUD methods
    """

    @staticmethod
    @transaction_decorator
    def create(user_id, word_id, status=True):
        """
        Create new user_word or return object if already exists

        :param user_id: int
        :param word_id: int
        :param status: bool | if True user can get this word
        :return: user_word object
        """
        user_word = UserWordService.filter(user_id=user_id, word_id=word_id)

        if user_word:
            return user_word[0]

        user_word = UserWord(user_id=user_id, word_id=word_id, status=status)
        DB.session.add(user_word)
        return user_word

    @staticmethod
    def get_by_id(user_word_id):
        """
        Get user_word by id

        :param id: int
        :return: user_word or none
        """
        user_word = DB.session.query(UserWord).get(user_word_id)
        return user_word

    @staticmethod
    @transaction_decorator
    def update(user_word_id, user_id=None, word_id=None, status=None):
        """
        Update user_word info in database

        :param user_word_id: int
        :param user_id: int
        :param word_id: int
        :param status: bool
        :return: user_word object
        """
        user_word = UserWordService.get_by_id(user_word_id)

        if user_word is None:
            raise NotExist()

        if user_id is not None:
            user_word.user_id = user_id
        if word_id is not None:
            user_word.word_id = word_id
        if status is not None:
            user_word.status = status

        DB.session.merge(user_word)

        return user_word

    @staticmethod
    @transaction_decorator
    def delete(user_word_id):
        """
        Delete user_word from database

        :param user_word_id: int
        :return: True or None
        """
        user_word = UserWordService.get_by_id(user_word_id)

        if user_word is None:
            raise NotExist()

        DB.session.delete(user_word)
        return True

    @staticmethod
    def filter(user_id=None, word_id=None, status=None):
        """
        Get list of user_word objects

        :param user_id: int
        :param word_id: int
        :param status: bool
        :return: list
        """
        data = {}

        if user_id is not None:
            data['user_id'] = user_id
        if word_id is not None:
            data['word_id'] = word_id
        if status is not None:
            data['status'] = status

        user_words = DB.session.query(UserWord).filter_by(**data).all()
        return user_words
