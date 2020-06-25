"""Create database"""

from src.utils.decorators import database_update_decorator


@database_update_decorator
def init_database(cursor):
    """
    Create database`s tables

    :param cursor: used in decorator
    :return: True or None
    """
    cursor.execute('''
        CREATE TABLE users
        (id integer PRIMARY KEY AUTOINCREMENT,
        username text,
        telegram_id integer UNIQUE,
        interval integer DEFAULT 5
        ),
                   ''')

    cursor.execute('''
        CREATE TABLE user_words
        (id integer PRIMARY KEY AUTOINCREMENT,
        user_id integer,
        word_id integer,
        status integer
        UNIQUE (user_id, word_id)
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


init_database() #pylint: disable=no-value-for-parameter
