#!/usr/bin/python3
"""
DB storage class
"""

from os import getenv
from sqlalchemy import create_engine, MetaData
from sqlalchemy.orm import sessionmaker, scoped_session
from models.state import State
from models.city import City
from models.base_model import Base
from models import stringtemplates as ENV
import models


class DBStorage:
    """
    This class handles the storage of objects using a relational database
    """
    __engine = None
    __session = None

    def __init__(self) -> None:
        """
        Initializes a new instance of the DBStorage class
        """
        user = getenv(ENV.HBNB_MYSQL_USER)
        pwd = getenv(ENV.HBNB_MYSQL_PWD)
        host = getenv(ENV.HBNB_MYSQL_HOST)
        db = getenv(ENV.HBNB_MYSQL_DB)
        env = getenv(ENV.HBNB_ENV, 'none')

        connection = f'mysql+mysqldb://{user:s}:{pwd:s}@{host:s}/{db:s}'
        self.__engine = create_engine(connection, pool_pre_ping=True)

        if env == ENV.TEST:
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None) -> dict:
        """
        Retrieves all objects of a specified class in the database
        Args:
            cls (str): Class name
        Returns:
            dict: Dictionary of objects
        """
        database = {}

        if cls != '':
            objs = self.__session.query(models.classes[cls]).all()
            for obj in objs:
                key = f'{obj.__class__.__name__}.{obj.id}'
                database[key] = obj
            return database
        else:
            for key, value in models.classes.items():
                if key != 'BaseModel':
                    objs = self.__session.query(value).all()
                    if len(objs):
                        for obj in objs:
                            k = f'{obj.__class__.__name__}.{obj.id}'
                            database[k] = obj
            return database

    def new(self, obj) -> None:
        """
        Adds a new object to the current database session
        Args:
            obj: Object to add to the session
        """
        self.__session.add(obj)

    def save(self) -> None:
        """
        Commits the current state of the database session
        """
        self.__session.commit()

    def delete(self, obj=None) -> None:
        """
        Deletes an object from the database session
        Args:
            obj: Object to delete from the session
        """
        if obj is None:
            return
        self.__session.delete(obj)

    def reload(self) -> None:
        """
        Creates all tables in the database and initializes a new session
        """
        self.__session = Base.metadata.create_all(self.__engine)
        factory = sessionmaker(bind=self.__engine, expire_on_commit=False)
        Session = scoped_session(factory)
        self.__session = Session()

    def close(self) -> None:
        """
        Closes the current session
        """
        self.__session.close()
