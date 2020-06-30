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
                text += i.strip(".,ˈˌ")
                # text += i
        return text.replace('.', '')

    @staticmethod
    def translate(word):
        pass


class RussianTranslation(Translation):
    URL = 'https://dictionary.cambridge.org/dictionary/english-russian/'

    @staticmethod
    def get_translation(soup):
        translation = soup.find(class_='trans').contents[0] # get translation from the html and get it from the list
        translation = translation.strip('\n ') # get rid of new line and spaces
        return translation

    @staticmethod
    def get_phrase(soup):
        phrase = soup.select('div.def.ddef_d')[0]
        phrase = RussianTranslation.get_pron(phrase.contents)

        return phrase

    @staticmethod
    def translate(word):
        text = requests.get(RussianTranslation.URL + word).content

        soup = BeautifulSoup(text, 'html.parser')

        if soup.find(property='og:url').get('content').split('/')[-1] == '':
            return None

        translation = RussianTranslation.get_translation(soup)
        phrase = RussianTranslation.get_phrase(soup)

        pron = soup.find(class_='pron').find(class_='ipa').contents
        pron = RussianTranslation.get_pron(pron)
        print(word, pron, translation, phrase)
        # return pron


print(RussianTranslation.translate('grocery'))

content = DocManager.get_doc_content()
words = []

for i in content.split('\n'):
    words.append(i.split('-')[0].strip())
#
for word in words:
    # print(word, RussianTranslation.translate(word))
    RussianTranslation.translate(word)
