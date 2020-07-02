import os

from sqlalchemy import create_engine
from sqlalchemy.orm import sessionmaker
from sqlalchemy.ext.declarative import declarative_base

DATABASE = {
    'POSTGRES_USER': os.environ.get('POSTGRES_USER'),
    'POSTGRES_PASSWORD': os.environ.get('POSTGRES_PASSWORD'),
    'HOST': os.environ.get('HOST'),
    'PORT': os.environ.get('PORT'),
    'DB_NAME': os.environ.get('REM_BOT_DB')
}

SQLALCHEMY_DATABASE_URI = f"postgresql://{DATABASE['POSTGRES_USER']}:" \
                          f"{DATABASE['POSTGRES_PASSWORD']}@" \
                          f"{DATABASE['HOST']}:{DATABASE['PORT']}/{DATABASE['DB_NAME']}"

BASE_MODEL = declarative_base()


class DB:
    ENGINE = create_engine(SQLALCHEMY_DATABASE_URI, echo=True)  # TODO change to false
    SESSION = sessionmaker(bind=ENGINE)
    session = SESSION()

