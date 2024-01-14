#!/usr/bin/python3
""" State Module for HBNB project """
from models.base_model import BaseModel, Base
from models import storage_type
from models.city import City
from sqlalchemy import Column, String
from sqlalchemy.orm import relationship


class State(BaseModel, Base):
    """State class for storing state information in the HBNB project.

    Attributes:
        __tablename__ (str): The name of the database table for states.
        name (str): The name of the state.
        cities (relationship): A relationship with the City class, establishing
                             a one-to-many relationship btw states & cities.

    Methods:
        None.

    """
    __tablename__ = 'states'

    if storage_type == 'db':
        name = Column(String(128), nullable=False)
        cities = relationship('City', backref='state',
                              cascade='all, delete, delete-orphan')

    else:
        name = ''

        @property
        def cities(self):
            """Getter method for cities related to the state.

            Returns:
                list: A list of City objects related to the state.

            """
            from models import storage
            related_cities = []
            cities = storage.all(City)

            for city in cities.values():
                if city.state_id == self.id:
                    related_cities.append(city)

            return related_cities
