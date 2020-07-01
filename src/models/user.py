from src.db.db_config import BASE, SESSION
from sqlalchemy import Column, Integer, String


class User(BASE):
    __tablename__ = "users"

    id2 = SESSION.Column()
    id = Column(Integer, primary_key=True)
    username = Column(String)
    telegram_id = Column(Integer, unique=True)
    interval = Column(Integer, default=5)
