#!/usr/bin/python3
"""
City Test Module
"""

import unittest
from models.city import City


class TestCity(unittest.TestCase):
    """
    Test class for City
    """

    def test_module_docs(self):
        """
        Test the module documentation
        """
        module_doc = (
            __import__("models.city").city.__doc__
        )
        self.assertGreater(len(module_doc), 0)

    def test_class_docs(self):
        """
        Test the class documentation
        """
        class_doc = (
            __import__("models.city").city.City.__doc__
        )
        self.assertGreater(len(class_doc), 0)

    def test_name_type(self):
        """
        Test the type of the name attribute
        """
        city = City()
        self.assertIs(type(city.name), str)

    def test_state_id_type(self):
        """
        Test the type of the state_id attribute
        """
        city = City()
        self.assertIs(type(city.state_id), str)

    def test_name_initialization(self):
        """
        Test that the name attribute is initialized as an empty string
        """
        city = City()
        self.assertEqual(city.name, "")

    def test_state_id_initialization(self):
        """
        Test that the state_id attribute is initialized as an empty string
        """
        city = City()
        self.assertEqual(city.state_id, "")

    def test_to_dict_method(self):
        """
        Test the to_dict method of City
        """
        city = City()
        city_dict = city.to_dict()
        self.assertIn("__class__", city_dict)
        self.assertEqual(city_dict["__class__"], "City")
        self.assertIn("id", city_dict)
        self.assertEqual(city_dict["id"], city.id)
        self.assertIn("created_at", city_dict)
        self.assertEqual(city_dict["created_at"], city.created_at.isoformat())
        self.assertIn("updated_at", city_dict)
        self.assertEqual(city_dict["updated_at"], city.updated_at.isoformat())
        self.assertIn("name", city_dict)
        self.assertEqual(city_dict["name"], city.name)
        self.assertIn("state_id", city_dict)
        self.assertEqual(city_dict["state_id"], city.state_id)

    def test_str_representation(self):
        """
        Test the string representation of City
        """
        city = City()
        str_representation = str(city)
        self.assertTrue("[City]" in str_representation)
        self.assertTrue(city.id in str_representation)
        self.assertTrue(str(city.__dict__) in str_representation)


if __name__ == "__main__":
    unittest.main()
