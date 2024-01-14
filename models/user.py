#!/usr/bin/python3
""" User Module for HBNB project """

from models.base_model import BaseModel, Base
from models import storage_type
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class User(BaseModel, Base):
    """User class for storing user information in the HBNB project.

    Attributes:
        __tablename__ (str): The name of the database table for users.
        email (str): The email address of the user.
        password (str): The password of the user.
        first_name (str): The first name of the user.
        last_name (str): The last name of the user.
        places (relationship): Relationship with the 'Place' class.
        reviews (relationship): Relationship with the 'Review' class.

    Methods:
        None.

    """
    __tablename__ = 'users'

    if storage_type == 'db':
        email = Column(String(128), nullable=False)
        password = Column(String(128), nullable=False)
        first_name = Column(String(128), nullable=True)
        last_name = Column(String(128), nullable=True)
        places = relationship('Place', backref='user',
                              cascade='all, delete, delete-orphan')
        reviews = relationship('Review', backref='user',
                               cascade='all, delete, delete-orphan')

    else:
        email = ""
        password = ""
        first_name = ""
        last_name = ""
