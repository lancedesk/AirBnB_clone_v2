#!/usr/bin/python3
""" Amenity Module for HBNB project """

from models.base_model import BaseModel, Base
from models import storage_type
from sqlalchemy import Column, String


class Amenity(BaseModel, Base):
    """Amenity class for storing amenity information in the HBNB project.

    Attributes:
        __tablename__ (str): The name of the database table for amenities.
        name (str): The name of the amenity.

    Methods:
        None.

    """
    __tablename__ = 'amenities'

    if storage_type == 'db':
        name = Column(String(128), nullable=False)

    else:
        name = ""
