"""
Translating and adding words to the database from google docs
"""
from urllib.parse import urlparse
from src.services.user_word import UserWordService
from src.services.words import WordService
from src.utils.doc_manager import DocManager
from src.utils.translate import RussianTranslation


class NewWordsService:
    """
    Add user words
    """

    @staticmethod
    def add_user_words_from_doc_russian(user_telegram_id, url):
        """
        Add new words from user`s google doc to the words and user_words tables

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

        # TODO create function add many words
        for word, translation in words.items():

            if new_word := WordService.filter(word=word):  # if word already in db
                print(f'{word} exist')
                word_status[word] = 'already in database'
                # add word to user word list
                UserWordService.add_user_word(user_telegram_id=user_telegram_id, word=new_word[0])
                continue

            word_info = RussianTranslation.get_word_info(word)

            if not word_info:  # if could not translate
                word_status[word] = False
                continue

            if translation:
                word_info['rus_translation'] = translation
            word_status[word] = True

            new_word = WordService.create(**word_info)
            UserWordService.add_user_word(user_telegram_id=user_telegram_id, word=new_word)

        return word_status

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
