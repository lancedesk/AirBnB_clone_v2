#!/usr/bin/python3
"""
Amenity Test Module
"""

import unittest
from models.amenity import Amenity


class TestAmenity(unittest.TestCase):
    """
    Test class for Amenity
    """

    def test_module_docs(self):
        """
        Test the module documentation
        """
        module_doc = (
            __import__("models.amenity").amenity.__doc__
        )
        self.assertGreater(len(module_doc), 0)

    def test_class_docs(self):
        """
        Test the class documentation
        """
        class_doc = (
            __import__("models.amenity").amenity.Amenity.__doc__
        )
        self.assertGreater(len(class_doc), 0)

    def test_name_type(self):
        """
        Test the type of the name attribute
        """
        amenity = Amenity()
        self.assertIs(type(amenity.name), str)

    def test_name_initialization(self):
        """
        Test that the name attribute is initialized as an empty string
        """
        amenity = Amenity()
        self.assertEqual(amenity.name, "")

    def test_to_dict_method(self):
        """
        Test the to_dict method of Amenity
        """
        amenity = Amenity()
        amenity_dict = amenity.to_dict()
        self.assertIn("__class__", amenity_dict)
        self.assertEqual(amenity_dict["__class__"], "Amenity")
        self.assertIn("id", amenity_dict)
        self.assertEqual(amenity_dict["id"], amenity.id)
        self.assertIn("created_at", amenity_dict)
        self.assertEqual(
            amenity_dict["created_at"], amenity.created_at.isoformat()
        )
        self.assertIn("updated_at", amenity_dict)
        self.assertEqual(
            amenity_dict["updated_at"], amenity.updated_at.isoformat()
        )
        self.assertIn("name", amenity_dict)
        self.assertEqual(amenity_dict["name"], amenity.name)

    def test_str_representation(self):
        """
        Test the string representation of Amenity
        """
        amenity = Amenity()
        str_representation = str(amenity)
        self.assertTrue("[Amenity]" in str_representation)
        self.assertTrue(amenity.id in str_representation)
        self.assertTrue(str(amenity.__dict__) in str_representation)


if __name__ == "__main__":
    unittest.main()
