#!/usr/bin/python3
"""
State Module for HBNB project
"""

from models.base_model import BaseModel, Base
from sqlalchemy.orm import relationship
from sqlalchemy import Column, String
from models.city import City
from os import getenv
import models


class State(BaseModel, Base):
    """
    State class for storing state information
    """

    __tablename__ = "states"
    storage_type = getenv("HBNB_TYPE_STORAGE")
    name = Column(String(128), nullable=False)
    cities = relationship("City", cascade="all, delete", backref="state")

    if storage_type != "db":
        @property
        def cities(self):
            """
            Getter attribute for cities in a state
            """
            all_cities = models.storage.all(City)
            result = [
                         city
                         for city in all_cities.values()
                         if city.state_id == self.id
                     ]
            return result
