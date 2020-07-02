# from src.db.db_config import BASE, SESSION
# from sqlalchemy import Column, Integer, String
#
#
# class UserWord(BASE):
#     __tablename__ = "user_words"
#     __table_args__ = (SESSION.UniqueConstraint('user_id', 'word_id',
#                                                name='user_word'),
#                       )
#     id = Column(Integer, primary_key=True)
#     user_id = Column(Integer)
#     word_id = Column(Integer)
#     status = Column(Integer)
#
#
# CREATE TABLE user_words
#         (id integer PRIMARY KEY AUTOINCREMENT,
#         user_id integer,
#         word_id integer,
#         status integer,
#         UNIQUE (user_id, word_id)
#         CONSTRAINT fk_user
#             FOREIGN KEY (user_id)
#             REFERENCES users(id)
