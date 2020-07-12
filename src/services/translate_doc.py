"""
Translating and adding words to the database from google docs
"""
import time

from urllib.parse import urlparse
from src.services.user_word import UserWordService
from src.services.words import WordService
from src.utils.doc_manager import DocManager
from src.utils.translate import RussianTranslation


class NewWordsService:

    @staticmethod
    def add_user_words_from_doc_russian(user_telegram_id, url):
        """
        Add new words from user`s google doc to the words and user_words tables

        :param user_telegram_id: str or int idk yet |
        :param url: str | link to google document
        :return: dict | word_status | or None
        """
        start = time.time()

        document_id = NewWordsService.get_doc_id_from_url(url)

        if document_id is None:
            return None

        finish1 = time.time() - start
        print(f'get doc id = {finish1}')

        start2 = time.time()

        words = DocManager.get_words_in_dictionary(document_id)  # dict of words

        finish2 = time.time() - start2
        print(f'words in dictionary = {finish2}')

        word_status = {}  # if translator found that word or not

        start3 = time.time()

        for word, translation in words.items():

            if new_word := WordService.filter(word=word):  # if word already in db
                print(f'{word} exist')
                word_status[word] = 'already in database'
                # add word to user word list
                UserWordService.add_user_word(user_telegram_id=user_telegram_id, word=new_word[0])
                continue

            start4 = time.time()

            word_info = RussianTranslation.translate(word)

            finish4 = time.time() - start4
            print(f'translate = {finish4}')

            if not word_info:  # if could not translate
                word_status[word] = False
                continue

            if translation:
                word_info['rus_translation'] = translation
            word_status[word] = True

            new_word = WordService.create(**word_info)
            UserWordService.add_user_word(user_telegram_id=user_telegram_id, word=new_word)

        finish3 = time.time() - start3
        print(f'cycle = {finish3}')

        finish = time.time() - start
        print(f'total = {finish}')

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
