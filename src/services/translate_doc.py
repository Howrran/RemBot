"""
Translating and adding words to the database from google docs
"""
from urllib.parse import urlparse
from src.services.user_word import UserWordService
from src.services.words import WordService
from src.utils.doc_manager import DocManager
from src.utils.translate import RussianTranslation, UkrainianTranslation


class NewWordsService:
    """
    Add user words
    """

    @staticmethod
    def add_user_words_from_doc(user_telegram_id, url):
        """
        Add new words from user`s google doc to the words and user_words tables

        #TODO add many words in one query
        :param user_telegram_id: str or int idk yet |
        :param url: str | link to google document
        :return: dict | word_status | or None
        """
        document_id = NewWordsService.get_doc_id_from_url(url)

        if document_id is None:
            return None

        words = DocManager.get_words_in_dictionary(document_id)  # dict of words
        if words is None:
            return None
        word_status = {}  # if translator found that word or not

        for word, translation in words.items():
            # pylint: disable=singleton-comparison
            if words[word] == False: # if that word wasn`t legit in doc file
                word_status[word] = False
                continue

            new_word = NewWordsService.add_single_word(
                user_telegram_id=user_telegram_id,
                word=word,
                translation=translation)

            word_status[word] = bool(new_word)

        return word_status


    @staticmethod
    def add_single_word(user_telegram_id, word, translation=None):
        """
        Add new word to the words and user_words tables

        :param word:
        :return:
        """
        if new_word := WordService.filter(word=word):  # if word already in db
            # add word to user word list
            UserWordService.add_user_word(user_telegram_id=user_telegram_id, word=new_word[0])
            return new_word[0]

        word_info = RussianTranslation.get_word_info(word)

        if not word_info:  # if could not translate
            return None

        ukr_translation = UkrainianTranslation.get_translation(word)
        if ukr_translation is not None:
            word_info['ukr_translation'] = ukr_translation
        # if translation:
        #     word_info['ukr_translation'] = translation
        #
        # else:
        #     ukr_translation = UkrainianTranslation.get_translation(word)
        #     if ukr_translation is not None:
        #         word_info['ukr_translation'] = ukr_translation

        new_word = WordService.create(**word_info)
        UserWordService.add_user_word(user_telegram_id=user_telegram_id, word=new_word)
        return new_word

    @staticmethod
    def get_doc_id_from_url(url: str):
        """
        Get google doc id from url

        urlparse = ParseResult(
        scheme='https',
        netloc='docs.google.com',
        path='/document/d/1p0Q49GW9HUXBkd5LmKB9k7TRngc4fUEaQgCjzuQmHaM/edit',
        params='',
        query='',
        fragment='gid=0')
        :param url: str | doc url
        :return: None or str | doc id
        """
        try:
            sheet_id_number = 3

            link = urlparse(url)
            # split path and get sheet_id from it
            sheet_id = link.path.split('/')[sheet_id_number]

            return sheet_id

        except IndexError:
            return None
