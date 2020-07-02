"""
User model
"""
from sqlalchemy import (
    Column,
    Integer,
    String
)

from config import DB


class User(DB.BASE_MODEL):
    """
    User model
    """
    __tablename__ = "users"

    id = Column(Integer, primary_key=True)
    username = Column(String)
    telegram_id = Column(Integer, unique=True)
    interval = Column(Integer, default=5)

    def __repr__(self):
        return f"<User(id='{self.id}',username='{self.username}', " \
               f"telegram_id='{self.telegram_id}', interval='{self.interval}')>"
