"""
User model
"""
from sqlalchemy import (
    Column,
    Integer,
    String
)
from sqlalchemy.orm import relationship

from src.config import DB  # pylint: disable= no-name-in-module


class User(DB.BASE_MODEL):  # pylint: disable= too-few-public-methods
    """
    User model
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    telegram_id = Column(Integer, unique=True)
    interval = Column(Integer, default=5)
    language = Column(String, default='ukr')

    user_word = relationship("UserWord", backref='user')

    def __repr__(self):
        return f"<User(id='{self.id}',username='{self.username}', " \
               f"telegram_id='{self.telegram_id}', interval='{self.interval}')>"
