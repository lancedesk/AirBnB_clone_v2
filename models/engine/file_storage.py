#!/usr/bin/python3
"""
This module defines a class to manage file storage for the hbnb clone
"""
import json


class FileStorage:
    """
    This class manages file storage for the hbnb clone
    """
    __file_path = 'file.json'
    __objects = {}

    def all(self, cls=None):
        """
        Returns the dictionary of objects
        Args:
            cls (class): class name
        Returns:
            dictionary of objects or specific class objects
        """
        if cls is None:
            return self.__objects
        cls_name = cls.__name__
        dct = {}
        for key in self.__objects.keys():
            if key.split('.')[0] == cls_name:
                dct[key] = self.__objects[key]
        return dct

    def new(self, obj):
        """
        Sets in __objects the obj with key <obj class name>.id
        Args:
            obj (Object): object to set in __objects dictionary
        """
        self.__objects.update(
            {obj.to_dict()['__class__'] + '.' + obj.id: obj}
            )

    def save(self):
        """
        Serializes __objects to the JSON file (path: __file_path)
        """
        with open(self.__file_path, 'w') as f:
            temp = {}
            temp.update(self.__objects)
            for key, val in temp.items():
                temp[key] = val.to_dict()
            json.dump(temp, f)

    def reload(self):
        """
        Deserializes the JSON file to __objects (only if the JSON file exists)
        """
        from models.base_model import BaseModel
        from models.user import User
        from models.place import Place
        from models.state import State
        from models.city import City
        from models.amenity import Amenity
        from models.review import Review

        classes = {
                    'BaseModel': BaseModel, 'User': User, 'Place': Place,
                    'State': State, 'City': City, 'Amenity': Amenity,
                    'Review': Review
                  }
        try:
            temp = {}
            with open(self.__file_path, 'r') as f:
                temp = json.load(f)
                for key, val in temp.items():
                    self.all()[key] = classes[val['__class__']](**val)
        except FileNotFoundError:
            pass

    def delete(self, obj=None):
        """
        Deletes obj from __objects if it’s inside
        Args:
            obj (Object): object to delete from __objects
        """
        if obj is None:
            return
        obj_key = obj.to_dict()['__class__'] + '.' + obj.id
        if obj_key in self.__objects.keys():
            del self.__objects[obj_key]

    def close(self):
        """
        Calls reload() method for deserializing the JSON file to objects
        """
        self.reload()
