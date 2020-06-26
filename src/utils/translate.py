"""
Module for translating words
"""

import requests

from bs4 import BeautifulSoup
from src.doc_manager import DocManager

# url = 'https://www.oxfordlearnersdictionaries.com/definition/english/word_1?q=word'
# text = requests.get(url).text

# soup = BeautifulSoup(text, 'html.parser')

# a = soup.find('span', class_='phon')

content = DocManager.get_doc_content()
words = []

for i in content.split('\n'):
    words.append(i.split('-')[0].strip())

for word in words:
    url = f'https://dictionary.cambridge.org/dictionary/english-russian/{word}'
    print(url)
