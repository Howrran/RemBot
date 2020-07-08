import os

from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from .local_settings import DATABASE

DEFAULT_INTERVAL = 5

SQLALCHEMY_DATABASE_URI = f"postgresql://{DATABASE['POSTGRES_USER']}:" \
                          f"{DATABASE['POSTGRES_PASSWORD']}@" \
                          f"{DATABASE['HOST']}:{DATABASE['PORT']}/{DATABASE['DB_NAME']}"


class DB:
    ENGINE = create_engine(SQLALCHEMY_DATABASE_URI, echo=False)  # TODO change to false
    SESSION = sessionmaker(bind=ENGINE, autocommit=True)
    BASE_MODEL = declarative_base()
    session = SESSION()
