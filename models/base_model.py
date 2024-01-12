#!/usr/bin/python3
"""
Module containing the BaseModel class.
Defines the BaseModel class, which serves as the base class for other classes.
"""

import models
from uuid import uuid4
from datetime import datetime


class BaseModel:
    """
    Base class for other classes.
    """

    def __init__(self, *args, **kwargs):
        """
        Initializes instance attributes.

        Args:
            *args: Variable length argument list (not used in this case).
            **kwargs: Keyword args to initialize attributes from a dictionary.
        """
        time_format = "%Y-%m-%dT%H:%M:%S.%f"
        self.id = str(uuid4())
        self.created_at = datetime.today()
        self.updated_at = datetime.today()
        if len(kwargs) != 0:
            for k, v in kwargs.items():
                if k == "created_at" or k == "updated_at":
                    self.__dict__[k] = datetime.strptime(v, time_format)
                else:
                    self.__dict__[k] = v
        else:
            models.storage.new(self)

    def save(self):
        """
        Updates the 'updated_at' attribute with the current datetime
        and saves the object to the storage.
        """
        self.updated_at = datetime.today()
        models.storage.save()

    def to_dict(self):
        """
        Returns a dictionary representation of the object.

        Returns:
            dict: A dictionary containing keys/values of the instance.
        """
        rdict = self.__dict__.copy()
        rdict["created_at"] = self.created_at.isoformat()
        rdict["updated_at"] = self.updated_at.isoformat()
        rdict["__class__"] = self.__class__.__name__
        return rdict

    def __str__(self):
        """
        Returns a string representation of the object.

         Returns:
            str: A formatted string.
        """
        clname = self.__class__.__name__
        return "[{}] ({}) {}".format(clname, self.id, self.__dict__)
