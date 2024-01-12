#!/usr/bin/python3
"""
Module containing the FileStorage class.
"""

import json
from models.base_model import BaseModel
from models.user import User
from models.state import State
from models.city import City
from models.place import Place
from models.amenity import Amenity
from models.review import Review


class FileStorage:
    """Handles serialization and deserialization of objects"""
    __file_path = "file.json"
    __objects = {}

    def all(self):
        """Returns the dictionary __objects"""
        return FileStorage.__objects

    def new(self, obj):
        """Sets in __objects the obj with key <obj class name>.id"""
        _key = obj.__class__.__name__
        FileStorage.__objects["{}.{}".format(_key, obj.id)] = obj

    def save(self):
        """Serializes __objects to the JSON file"""
        new_dic = FileStorage.__objects
        dict_obj = {obj: new_dic[obj].to_dict() for obj in new_dic.keys()}
        with open(FileStorage.__file_path, "w") as f:
            json.dump(dict_obj, f)

    def reload(self):
        """Deserializes the JSON file to __objects"""
        try:
            with open(FileStorage.__file_path) as f:
                dict_obj = json.load(f)
                for value in dict_obj.values():
                    _name = value["__class__"]
                    del value["__class__"]
                    self.new(eval(_name)(**value))
        except FileNotFoundError:
            return
