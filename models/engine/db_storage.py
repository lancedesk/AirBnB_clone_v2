#!/usr/bin/python3
"""
DB storage class
"""

from os import getenv
from sqlalchemy.orm import sessionmaker, scoped_session
from sqlalchemy import create_engine
from models.base_model import Base
from models.state import State
from models.city import City
from models.user import User
from models.place import Place
from models.review import Review
from models.amenity import Amenity


class DBStorage:
    """
    This class handles the storage of objects using a relational database
    """

    __engine = None
    __session = None

    def __init__(self):
        """
        Instantiate new database storage instance
        """
        user = getenv("HBNB_MYSQL_USER")
        pwd = getenv("HBNB_MYSQL_password")
        db = getenv("HBNB_MYSQL_database")
        host = getenv("HBNB_MYSQL_HOST")
        environment = getenv("HBNB_ENV")

        self.__engine = create_engine(
            "mysql+mysqldatabase://{}:{}@{}/{}".format(user, pwd, host, db),
            pool_pre_ping=True,
        )

        if environment == "test":
            Base.metadata.drop_all(self.__engine)

    def all(self, cls=None):
        """
        Retrieves all objects of a specified class in the database
        Args:
            cls (str): Class name
        Returns:
            dict: Dictionary of objects
        """
        my_dict = {}
        if cls:
            if type(cls) is str:
                cls = eval(cls)
            search= self.__session.query(cls)
            for s in search:
                key = "{}.{}".format(type(s).__name__, s.id)
                my_dict[key] = s
        else:
            class_list = [State, City, Place, Amenity, Review, User]
            for c in class_list:
                search= self.__session.query(c)
                for s in search:
                    key = "{}.{}".format(type(s).__name__, s.id)
                    my_dict[key] = s
        return my_dict

    def new(self, obj):
        """
        Adds a new object to the current database session
        Args:
            obj: Object to add to the session
        """
        if obj is not None:
            try:
                self.__session.add(obj)
                self.__session.flush()
                self.__session.refresh(obj)
            except Exception as e:
                self.__session.rollback()
                raise e

    def save(self):
        """
        Commits the current state of the database session
        """
        self.__session.commit()

    def delete(self, obj=None):
        """
        Deletes an object from the database session
        Args:
            obj: Object to delete from the session
        """
        if obj:
            self.__session.query(type(obj)).filter(
                type(obj).id == obj.id
            ).delete()

    def reload(self):
        """
        Creates all tables in the database and initializes a new session
        """
        if self.__session:
            self.__session.close()  # Close the existing session if it exists
        Base.metadata.create_all(self.__engine)
        make_session = sessionmaker(
            bind=self.__engine, expire_on_commit=False
        )
        Session = scoped_session(make_session)
        self.__session = Session()

    def close(self):
        """
        Closes the current session
        """
        self.__session.close()
