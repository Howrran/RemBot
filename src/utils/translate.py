"""
Module for translating words
"""
import requests

from bs4 import BeautifulSoup, Tag


class Translation():
    """
    Basic class for translation
    """
    URL = None

    @staticmethod
    def get_text_from_tags(string):
        """
        extract text from html

        :param text: list of bs4.element.NavigableString and Tag or string with tags
        :return: str
        """
        text = ''
        for i in string:
            if isinstance(i, Tag):
                text += RussianTranslation.get_text_from_tags(i.contents)
            else:
                text += i.strip(".,ˈˌ")
        return text.replace('.', '')

    @staticmethod
    def get_transcription(soup):
        """
        Get transcription of the word from html

        :param soup: BeautifulSoup
        :return: str
        """
        transcription = soup.find(class_='pron').find(class_='ipa').contents
        transcription = RussianTranslation.get_text_from_tags(transcription)

        return transcription

    @staticmethod
    def get_explanation(soup):
        """
        Get explanation of the word from html

        :param soup: BeautifulSoup
        :return: str
        """
        explanation = soup.select('div.def.ddef_d')[0]
        explanation = RussianTranslation.get_text_from_tags(explanation.contents)

        return explanation


class RussianTranslation(Translation):
    """
    Translation into Russian by Cambridge dictionary
    """
    URL = 'https://dictionary.cambridge.org/dictionary/english-russian/'

    @staticmethod
    def get_translation(soup):
        """
        Get Russian translation of the word from html

        :param soup: BeautifulSoup
        :return: str
        """
        # get translation from the html and get rid of new line and spaces
        translation = soup.find(class_='trans').contents[0].strip('\n ')
        return translation

    @staticmethod
    def is_exist(soup):
        """
        Check if page for that word exist

        :param soup:
        :return:
        """
        exist = True
        if soup.find(property='og:url').get('content').split('/')[-1] == '':  # no such word on site
            exist = False

        return exist

    @staticmethod
    def get_word_info(word):
        """
        Return words: translation, transcription, explanation and link to the cambridge site

        :param word: str | word to translate
        :return: dict or None
        """
        link = RussianTranslation.URL + word
        content = requests.get(link, headers={"User-Agent": "Mozilla/5.0"}).content

        soup = BeautifulSoup(content, 'html.parser')

        if not RussianTranslation.is_exist(soup):
            return None

        translation = RussianTranslation.get_translation(soup)
        explanation = RussianTranslation.get_explanation(soup)
        transcription = RussianTranslation.get_transcription(soup)

        data = {
            'word': word,
            'transcription': transcription,
            'rus_translation': translation,
            'explanation': explanation,
            'link': link
        }

        return data


class UkrainianTranslation(Translation):
    """
    Translation into Ukrainian by Abby lingvo
    """
    URL_LINGVO = 'https://www.lingvolive.com/ru-ru/translate/en-uk/'

    @staticmethod
    def get_translation_lingvo(word):
        """
        Get Ukrainian Translation from html on LingvoLive

        :param word:
        :return:
        """
        link = UkrainianTranslation.URL_LINGVO + word

        content = requests.get(link, headers={"User-Agent": "Mozilla/5.0"}).content
        soup = BeautifulSoup(content, 'html.parser')
        if not UkrainianTranslation.is_exist(soup):
            return None

        translation = soup.select('div[class="_1S_20"] > span')

        ukr_translation = translation[-2] if translation[-1].text == 'Примеры' else translation[-1]
        ukr_translation = str(ukr_translation.text)

        return ukr_translation

    @staticmethod
    def is_exist(soup):
        """
        Check if page for that word exist

        :param soup:
        :return:
        """
        exist = True
        not_found = soup.find('div', attrs={'class': 'cw0oE'}).span.contents[
            0]  # check if word exist
        if not_found == 'Не найдено':
            exist = False

        return exist

# UkrainianTranslation.get_translation_google('section')
