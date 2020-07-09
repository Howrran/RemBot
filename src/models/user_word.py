"""
UserWord Model
"""
from sqlalchemy import Column, Integer, Boolean, UniqueConstraint, ForeignKey

from src.config import DB  # pylint: disable= no-name-in-module


class UserWord(DB.BASE_MODEL):
    """
    UserWord Model
    """
    __tablename__ = "user_words"
    __table_args__ = (UniqueConstraint('user_id', 'word_id', name='user_word'),)

    id = Column(Integer, primary_key=True)
    user_id = Column(Integer, ForeignKey('users.id', ondelete='CASCADE'))
    word_id = Column(Integer, ForeignKey('words.id', ondelete='CASCADE'))
    status = Column(Boolean)

    def __repr__(self):
        return f"<UserWord(id='{self.id}',user_id='{self.user_id}', " \
               f"word_id='{self.word_id}', status='{self.status}')>"
