"""
Google docs url validation function
"""
from urllib.parse import urlparse


def validate_url(url):
    """
    Google docs url validator
    :param url:
    :return: True if url is from google docs
    """
    parsed_url = urlparse(url)
    splitted_url_path = parsed_url.path.split('/')
    if len(splitted_url_path) > 3:
        d_value = splitted_url_path[2]
        return bool(parsed_url.netloc == 'docs.google.com' and d_value == 'd')
    return False
