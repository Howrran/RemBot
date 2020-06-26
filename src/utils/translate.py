"""
Module for translating words
"""

import requests

from bs4 import BeautifulSoup, Tag
from src.doc_manager import DocManager


class Translation():
    URL = None

    @staticmethod
    def get_pron(pron):
        """
        extract pronunciation from html

        :param pron: list of bs4.element.NavigableString and Tag
        :return: str
        """
        text = ''
        for i in pron:
            if isinstance(i, Tag):
                text += RussianTranslation.get_pron(i.contents)
            else:
                text += i.strip(".,ˈˌ ")
        return text.replace('.', '')

    @staticmethod
    def translate(word):
        pass


class RussianTranslation(Translation):
    URL = 'https://dictionary.cambridge.org/dictionary/english-russian/'

    @staticmethod
    def translate(word):
        text = requests.get(RussianTranslation.URL + word).content

        # print(requests.get(RussianTranslation.URL).status_code)

        soup = BeautifulSoup(text, 'html.parser')

        print(soup.find(property='og:url').get('content'))
        pron = soup.find(class_='pron').find(class_='ipa').contents
        pron = RussianTranslation.get_pron(pron)
        return pron


RussianTranslation.translate('grocery')

content = DocManager.get_doc_content()
words = []

for i in content.split('\n'):
    words.append(i.split('-')[0].strip())
#
# for word in words:
#     print(word, RussianTranslation.translate(word))
#
