#!/usr/bin/python3
"""This module defines a base class for all models in our hbnb clone"""
import uuid
from datetime import datetime
from sqlalchemy.ext.declarative import declarative_base
from sqlalchemy import Column, String, DATETIME
from models import storage_type

Base = declarative_base()


class BaseModel:
    """Base model for other classes.

    Attributes:
        id (str): A unique identifier for the model.
        created_at (datetime): The datetime when the model was created.
        updated_at (datetime): The datetime when the model was last updated.

    Note:
        `id` attribute is a primary key and must be unique for each instance.
        `created_at` and `updated_at` attributes are automatically set to the
        current UTC time when an instance is created or updated.
    """

    id = Column(String(60),
                nullable=False,
                primary_key=True,
                unique=True)
    created_at = Column(DATETIME,
                        nullable=False,
                        default=datetime.utcnow())
    updated_at = Column(DATETIME,
                        nullable=False,
                        default=datetime.utcnow())

    def __init__(self, *args, **kwargs):
        """Instantiates a new model"""
        if not kwargs:
            self.id = str(uuid.uuid4())
            self.created_at = datetime.now()
            self.updated_at = datetime.now()
        else:
            for key in kwargs:
                if key in ['created_at', 'updated_at']:
                    setattr(self, key, datetime.fromisoformat(kwargs[key]))
                elif key != '__class__':
                    setattr(self, key, kwargs[key])
            if storage_type == 'db':
                if not hasattr(self, 'id'):
                    setattr(self, 'id', str(uuid.uuid4()))
                if not hasattr(self, 'created_at'):
                    setattr(self, 'created_at', datetime.now())
                if not hasattr(self, 'updated_at'):
                    setattr(self, 'updated_at', datetime.now())

    def __str__(self):
        """Returns a string representation of the instance"""
        return '[{}] ({}) {}'.format(
            self.__class__.__name__, self.id, self.__dict__)

    def save(self):
        """Updates updated_at with current time when instance is changed"""
        from models import storage
        self.updated_at = datetime.now()
        storage.new(self)
        storage.save()

    def to_dict(self):
        """Convert instance into dictionary format"""
        dictionary = self.__dict__.copy()
        dictionary['__class__'] = self.__class__.__name__
        for key in dictionary:
            if isinstance(dictionary[key], datetime):
                dictionary[key] = dictionary[key].isoformat()
        if '_sa_instance_state' in dictionary.keys():
            del(dictionary['_sa_instance_state'])
        return dictionary

    def delete(self):
        '''Dletes current instance from storage'''
        from models import storage
        storage.delete(self)
