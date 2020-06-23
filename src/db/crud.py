import sqlite3
from src.utils.decorators import database_decorator
from config import DATABASE

@database_decorator
def select_all_users(cursor):
    sql = '''SELECT * FROM users'''

    cursor.execute(sql)
    users = cursor.fetchall()

    return users

@database_decorator
def add_user(cursor, username, telegram_id):
        sql = '''INSERT INTO users
                      (username, telegram_id)
                      VALUES (?,?)'''

        cursor.execute(sql, (username, telegram_id))

        return True

add_user('niqgga', 78)
users = select_all_users()
print(users)