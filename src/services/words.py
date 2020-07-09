"""
Words CRUD operations in DB
"""
from src.models import Word
from src.config import DB
from src.utils.decorators import transaction_decorator
from src.utils.errors import NotExist


class WordService():
    """
    Class with CRUD methods
    """

    @staticmethod
    @transaction_decorator
    def create( # pylint: disable=too-many-arguments
            word,
            transcription,
            example_phrase,
            link,
            ukr_translation=None,
            rus_translation=None):
        """
        Create new word or return object if already exists

        :param word: str
        :param transcription: str
        :param example_phrase: str
        :param ukr_translation: str
        :param rus_translation: str
        :return: word object
        """
        word_object = WordService.filter(word=word)

        if word_object:
            return word_object[0]

        word_object = Word(
            word=word,
            transcription=transcription,
            ukr_translation=ukr_translation,
            rus_translation=rus_translation,
            example_phrase=example_phrase,
            link=link
        )
        DB.session.add(word_object)
        return word_object

    @staticmethod
    def get_by_id(word_id):
        """
        Get word by id

        :param id: int
        :return: word or none
        """
        word = DB.session.query(Word).get(word_id)
        return word

    @staticmethod
    @transaction_decorator
    def update( # pylint: disable=too-many-arguments
            word_id,
            word=None,
            transcription=None,
            example_phrase=None,
            link=None,
            ukr_translation=None,
            rus_translation=None
    ):
        """
        Update word info in database

        :param word_id: int
        :param word: str
        :param transcription: str
        :param example_phrase: str
        :param link: str
        :param ukr_translation: str
        :param rus_translation: str
        :return: word object
        """
        word_object = WordService.get_by_id(word_id)

        if word_object is None:
            raise NotExist()

        if word is not None:
            word_object.word = word
        if transcription is not None:
            word_object.transcription = transcription
        if example_phrase is not None:
            word_object.example_phrase = example_phrase
        if link is not None:
            word_object.link = link
        if ukr_translation is not None:
            word_object.ukr_translation = ukr_translation
        if rus_translation is not None:
            word_object.rus_translation = rus_translation

        DB.session.merge(word_object)

        return word_object

    @staticmethod
    @transaction_decorator
    def delete(word_id):
        """
        Delete word from database

        :param word_id: int
        :return: True or None
        """
        word_object = WordService.get_by_id(word_id)

        if word_object is None:
            raise NotExist()

        DB.session.delete(word_object)
        return True

    @staticmethod
    def filter( # pylint: disable=too-many-arguments
            word=None,
            transcription=None,
            example_phrase=None,
            link=None,
            ukr_translation=None,
            rus_translation=None
    ):
        """
        Get list of word objects by parameters

        :param word: str
        :param transcription: str
        :param example_phrase: str
        :param link: str
        :param ukr_translation: str
        :param rus_translation: str
        :return: list
        """
        data = {}

        if word is not None:
            data['word'] = word
        if transcription is not None:
            data['transcription'] = transcription
        if example_phrase is not None:
            data['example_phrase'] = example_phrase
        if link is not None:
            data['link'] = link
        if ukr_translation is not None:
            data['ukr_translation'] = ukr_translation
        if rus_translation is not None:
            data['rus_translation'] = rus_translation

        words = DB.session.query(Word).filter_by(**data).all()
        return words
