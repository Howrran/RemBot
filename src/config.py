"""
Project configuration
"""
from sqlalchemy import create_engine
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy.orm import sessionmaker
from src.local_settings  import DATABASE #pylint: disable=no-name-in-module, import-error

DEFAULT_INTERVAL = 5

SQLALCHEMY_DATABASE_URI = f"postgresql://{DATABASE['POSTGRES_USER']}:" \
                          f"{DATABASE['POSTGRES_PASSWORD']}@" \
                          f"{DATABASE['HOST']}:{DATABASE['PORT']}/{DATABASE['DB_NAME']}"


class DB: #pylint: disable=too-few-public-methods
    """
    DataBase connection
    """
    ENGINE = create_engine(SQLALCHEMY_DATABASE_URI, echo=False)
    SESSION = sessionmaker(bind=ENGINE, autocommit=True)
    BASE_MODEL = declarative_base()
    session = SESSION()
