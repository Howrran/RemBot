import sqlite3
from config import DATABASE
from src.utils.decorators import database_decorator

@database_decorator
def init_database(cursor):

    cursor.execute('''
        CREATE TABLE users
        (id integer PRIMARY KEY AUTOINCREMENT,
        username text,
        telegram_id integer UNIQUE
        )
                   ''')

    cursor.execute('''
        CREATE TABLE user_words
        (id integer PRIMARY KEY AUTOINCREMENT,
        user_id integer,
        word_id integer,
        status integer
        )
                   ''')

    cursor.execute('''
    CREATE TABLE words
        (id integer PRIMARY KEY AUTOINCREMENT,
        word text UNIQUE,
        transcription text,
        translation text,
        example_phrase text
        )
                   ''')

    return True

init_database()