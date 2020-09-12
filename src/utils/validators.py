"""Module for validators"""
from urllib.parse import urlparse


class Validator():
    """
    Validators
    """

    @staticmethod
    def interval_validator(interval):
        """
        Validate new interval

        :param interval: int | interval in seconds
        :return:
        """
        if not interval.isnumeric():
            return False

        interval = int(interval)

        if not 1 < interval < 86_400:
            return False

        return True

    @staticmethod
    def google_doc_validator(url):
        """
        Google docs url validator

        urlparse = ParseResult(
        scheme='https',
        netloc='docs.google.com',
        path='/document/d/1j-v9OfrngzZ9-or7guRVIV5bjLQ7A0ninbIwOkZKg4k/edit',
        params='',
        query='',
        fragment='gid=0')

        :param url:
        :return: True if url is from google docs
        """
        parsed_url = urlparse(url)
        splitted_url_path = parsed_url.path.split('/')
        if len(splitted_url_path) > 3:
            d_value = splitted_url_path[2]
            return bool(parsed_url.netloc == 'docs.google.com' and d_value == 'd')
        return False

    @staticmethod
    def language_validator(language):
        """
        Validate language input

        :param language:
        :return:
        """
        language_list = ['ukr', 'rus']
        if language.lower() not in language_list:
            return False

        return True
