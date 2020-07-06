"""
Word Model
"""
from sqlalchemy import Column, Integer, String
from sqlalchemy.orm import relationship

from config import DB  # pylint: disable= no-name-in-module


class Word(DB.BASE_MODEL):
    """
    Word Model
    """
    __tablename__ = "words"

    id = Column(Integer, primary_key=True)
    word = Column(String)
    transcription = Column(String)
    ukr_translation = Column(String)
    rus_translation = Column(String)
    example_phrase = Column(String)
    link = Column(String)

    user_word = relationship("UserWord", backref='word')

    def __repr__(self):
        return f"<Word(id='{self.id}',word='{self.word}', " \
               f"transcription='{self.transcription}'," \
               f" ukr_translation='{self.ukr_translation}', " \
               f"rus_translation='{self.rus_translation}'," \
               f" example_phrase='{self.example_phrase}', " \
               f"link='{self.link}')>"
