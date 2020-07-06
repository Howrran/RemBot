"""
Module for operating with words in database
"""
from src.utils.decorators import database_update_decorator
from src.utils.errors import NotExist


class WordCRUD():
    """
    Class for operating with words in db
    """

    # positions in word tuple
    ID = 0
    WORD = 1
    TRANSCRIPTION = 2
    TRANSLATION = 3
    EXAMPLE_PHRASE = 4
    LINK = 5

    @staticmethod
    @database_update_decorator
    def select_all_words(cursor):
        """
        Get all words from the database

        :param cursor: used in decorator
        :return: list: words
        """
        sql = 'SELECT * FROM words'

        cursor.execute(sql)
        words = cursor.fetchall()

        return words

    @staticmethod
    @database_update_decorator
    def add_word(cursor, word, transcription, translation, example_phrase, link): # pylint: disable=too-many-arguments
        """
        Add new word to the database

        :param cursor: used in decorator
        :param word: str
        :param transcription: str
        :param translation: str
        :param example_phrase: str
        :param link: str
        :return:
        """
        sql = '''INSERT INTO words
                 (word, transcription, translation, example_phrase, link)
                 VALUES (?,?,?,?,?)'''

        cursor.execute(sql, (word, transcription, translation, example_phrase, link))

        return True

    @staticmethod
    @database_update_decorator
    def get_word_by_id(cursor, word_id):
        """
        Get word from the database by id

        :param cursor: used in decorator
        :param word_id: str or int
        :return: tuple or None
        """
        word_id = str(word_id)
        sql = 'SELECT * from words where id=?'
        word = cursor.execute(sql, (word_id)).fetchone()

        return word

    @staticmethod
    @database_update_decorator
    def word_filter( # pylint: disable=too-many-arguments
            cursor,
            word=None,
            transcription=None,
            translation=None,
            example_phrase=None,
            link=None):
        """
        Get words from the database by parameters

        :param cursor: used in decorator
        :param word: str
        :param transcription: str
        :param translation: str
        :param example_phrase: str
        :param link: str
        :return: list
        """

        sql = '''SELECT * from words
                 where word=? and
                 (transcription=? or translation=? or example_phrase=? or link=?)'''

        output = cursor.execute(sql,
                                (word, transcription, translation, example_phrase, link)
                                ).fetchall()

        return output

    @staticmethod
    @database_update_decorator
    def update_word(  #pylint: disable=too-many-arguments
            cursor,
            word_id,
            word=None,
            transcription=None,
            translation=None,
            example_phrase=None,
            link=None):
        """
        Update word`s information in database

        :param cursor: used in decorator
        :param word_id: int
        :param word: str
        :param transcription: str
        :param translation: str
        :param example_phrase: str
        :param link: str
        :return:
        """
        if word is None and transcription is None \
                and translation is None and example_phrase is None and link is None:
            return None

        old_word = WordCRUD.get_word_by_id( #pylint: disable=no-value-for-parameter
            word_id=word_id)

        if old_word is None:
            raise NotExist()

        word = word if word else old_word[WordCRUD.WORD]
        transcription = transcription if transcription else old_word[WordCRUD.TRANSCRIPTION]
        translation = translation if translation else old_word[WordCRUD.TRANSLATION]
        example_phrase = example_phrase if example_phrase else old_word[WordCRUD.EXAMPLE_PHRASE]
        link = link if link else old_word[WordCRUD.LINK]

        sql = '''UPDATE words
                 set word = ?, transcription = ?, translation = ?, example_phrase = ?, link = ?
                 where id = ?
                '''
        cursor.execute(sql,
                       (word, transcription, translation, example_phrase, link, word_id)
                       )
        new_word = WordCRUD.get_word_by_id( #pylint: disable=no-value-for-parameter
            word_id=word_id)

        return new_word
