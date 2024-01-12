#!/usr/bin/python3
"""
BaseModel tests
"""

import unittest
from models.base_model import BaseModel
from datetime import datetime
from uuid import UUID
from unittest.mock import patch


class TestBaseModel(unittest.TestCase):
    """
    Unit tests for the BaseModel class.
    """
    def test_str_representation(self):
        """
        Tests the string representation of the object.
        """
        obj = BaseModel()
        str_representation = str(obj)
        self.assertTrue("[BaseModel]" in str_representation)
        self.assertTrue(obj.id in str_representation)
        self.assertTrue(str(obj.__dict__) in str_representation)

    def test_save_updates_updated_at(self):
        """
        Tests if calling save updates the updated_at attribute.
        """
        obj = BaseModel()
        initial_updated_at = obj.updated_at
        obj.save()
        self.assertNotEqual(obj.updated_at, initial_updated_at)

    def test_to_dict_method(self):
        """
        Tests the to_dict method of the BaseModel class.
        """
        obj = BaseModel()
        obj_dict = obj.to_dict()
        self.assertIn("__class__", obj_dict)
        self.assertEqual(obj_dict["__class__"], "BaseModel")
        self.assertIn("id", obj_dict)
        self.assertEqual(obj_dict["id"], obj.id)
        self.assertIn("created_at", obj_dict)
        self.assertEqual(obj_dict["created_at"], obj.created_at.isoformat())
        self.assertIn("updated_at", obj_dict)
        self.assertEqual(obj_dict["updated_at"], obj.updated_at.isoformat())

    def test_initialization_with_dict(self):
        """
        Tests initializing a new object from a dictionary.
        """
        obj = BaseModel()
        obj_dict = obj.to_dict()
        new_obj = BaseModel(**obj_dict)
        self.assertEqual(obj.id, new_obj.id)
        self.assertEqual(obj.created_at, new_obj.created_at)
        self.assertEqual(obj.updated_at, new_obj.updated_at)

    def test_unique_ids(self):
        """
        Tests that the IDs generated for different objects are unique.
        """
        obj1 = BaseModel()
        obj2 = BaseModel()
        self.assertNotEqual(obj1.id, obj2.id)

    def test_created_at_and_updated_at_types(self):
        """
        Tests the types of created_at and updated_at attributes.
        """
        obj = BaseModel()
        self.assertIsInstance(obj.created_at, datetime)
        self.assertIsInstance(obj.updated_at, datetime)

    def test_created_at_before_updated_at(self):
        """
        Tests if created_at is before or equal to updated_at.
        """
        obj = BaseModel()
        self.assertLessEqual(obj.created_at, obj.updated_at)

    # Additional Tests
    def test_moduleDocs(self):
        """
        Tests documentation for the module.
        """
        moduleDoc = __import__("models.base_model").base_model.__doc__
        self.assertGreater(len(moduleDoc), 0)

    def test_classDocs(self):
        """
        Tests documentation for the class.
        """
        classDoc = __import__("models.base_model").base_model.BaseModel.__doc__
        self.assertGreater(len(classDoc), 0)

    def test_methodDocsSave(self):
        """
        Tests documentation for the save method.
        """
        methodDoc = (
            __import__("models.base_model")
            .base_model.BaseModel.save.__doc__
        )
        self.assertGreater(len(methodDoc), 0)

    def test_methodDocsto_dict(self):
        """
        Tests documentation for the to_dict method.
        """
        methodDoc = (
            __import__("models.base_model")
            .base_model.BaseModel.to_dict.__doc__
        )
        self.assertGreater(len(methodDoc), 0)

    def test_methodDocs__str___(self):
        """
        Tests documentation for the __str__ method.
        """
        methodDoc = (
            __import__("models.base_model")
            .base_model.BaseModel.__str__.__doc__
        )
        self.assertGreater(len(methodDoc), 0)

    def test_idType(self):
        """
        Tests the type of the id attribute.
        """
        obj = BaseModel()
        self.assertIs(type(obj.id), str)

    def test_idLength(self):
        """
        Tests the length of the id attribute.
        """
        obj = BaseModel()
        self.assertEqual(len(obj.id), 36)

    def test_idValidity(self):
        """
        Tests the validity of the id attribute as a UUID.
        """
        obj = BaseModel()
        value = UUID(obj.id)
        self.assertIs(type(value), UUID)

    def test_created_atType(self):
        """
        Tests the type of the created_at attribute.
        """
        obj = BaseModel()
        self.assertIs(type(obj.created_at), datetime)

    def test_updated_atType(self):
        """
        Tests the type of the updated_at attribute.
        """
        obj = BaseModel()
        self.assertIs(type(obj.updated_at), datetime)

    def test_outputOf__str__(self):
        """
        Tests the output of the __str__ method.
        """
        obj = BaseModel()
        str1 = f"[BaseModel] ({obj.id}) {obj.__dict__}"
        str2 = str(obj)
        self.assertEqual(str1, str2)

    def test_updated_atChanged(self):
        """
        Tests if calling save changes the updated_at attribute.
        """
        obj = BaseModel()
        initial_value = obj.updated_at
        obj.save()
        self.assertGreater(obj.updated_at, initial_value)

    def test_to_dictCheck(self):
        """
        Tests if the keys of to_dict are present in the object's __dict__.
        """
        obj = BaseModel()
        to_dict_dict = obj.to_dict()
        __dict__dict = obj.__dict__
        for keys in __dict__dict:
            self.assertIn(keys, to_dict_dict)

    def test_to_dict(self):
        """
        Tests the presence and type of keys in the to_dict output.
        """
        obj = BaseModel()
        to_dict_dict = obj.to_dict()
        self.assertIn("__class__", to_dict_dict)
        self.assertIs(type(to_dict_dict["__class__"]), str)

    def test_to_dict_Valid(self):
        """
        Tests the validity and formatting of to_dict output.
        """
        obj = BaseModel()
        to_dict_dict = obj.to_dict()
        created_at = datetime.fromisoformat(to_dict_dict["created_at"])
        updated_at = datetime.fromisoformat(to_dict_dict["updated_at"])
        self.assertIn("created_at", to_dict_dict)
        self.assertIn("updated_at", to_dict_dict)
        self.assertIs(type(to_dict_dict["created_at"]), str)
        self.assertIs(type(to_dict_dict["updated_at"]), str)
        self.assertEqual(to_dict_dict["created_at"], created_at.isoformat())
        self.assertEqual(to_dict_dict["updated_at"], updated_at.isoformat())

    def test_dictType(self):
        """
        Tests the type of the id attribute in the to_dict output.
        """
        obj = BaseModel()
        to_dict_dict = obj.to_dict()
        self.assertIs(type(to_dict_dict["id"]), str)


if __name__ == "__main__":
    unittest.main()
