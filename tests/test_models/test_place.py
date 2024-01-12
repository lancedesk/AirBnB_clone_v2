#!/usr/bin/python3
"""
Place Test Module
"""

import unittest
from models.place import Place


class TestPlace(unittest.TestCase):
    """
    Test class for Place
    """

    def test_module_docs(self):
        """
        Test the module documentation
        """
        module_doc = (
            __import__("models.place").place.__doc__
        )
        self.assertGreater(len(module_doc), 0)

    def test_class_docs(self):
        """
        Test the class documentation
        """
        class_doc = (
            __import__("models.place").place.Place.__doc__
        )
        self.assertGreater(len(class_doc), 0)

    def test_attributes_type(self):
        """
        Test the types of attributes in Place
        """
        place = Place()
        self.assertIs(type(place.name), str)
        self.assertIs(type(place.city_id), str)
        self.assertIs(type(place.user_id), str)
        self.assertIs(type(place.description), str)
        self.assertIs(type(place.number_rooms), int)
        self.assertIs(type(place.number_bathrooms), int)
        self.assertIs(type(place.max_guest), int)
        self.assertIs(type(place.price_by_night), int)
        self.assertIs(type(place.latitude), float)
        self.assertIs(type(place.longitude), float)
        self.assertIs(type(place.amenity_ids), list)

    def test_attribute_initialization(self):
        """
        Test that attributes are initialized correctly in Place
        """
        place = Place()
        self.assertEqual(place.name, "")
        self.assertEqual(place.city_id, "")
        self.assertEqual(place.user_id, "")
        self.assertEqual(place.description, "")
        self.assertEqual(place.number_rooms, 0)
        self.assertEqual(place.number_bathrooms, 0)
        self.assertEqual(place.max_guest, 0)
        self.assertEqual(place.price_by_night, 0)
        self.assertEqual(place.latitude, 0.0)
        self.assertEqual(place.longitude, 0.0)
        self.assertEqual(place.amenity_ids, [])

    def test_to_dict_method(self):
        """
        Test the to_dict method of Place
        """
        place = Place()
        place_dict = place.to_dict()
        self.assertIn("__class__", place_dict)
        self.assertEqual(place_dict["__class__"], "Place")
        self.assertIn("id", place_dict)
        self.assertEqual(place_dict["id"], place.id)
        self.assertIn("created_at", place_dict)
        self.assertEqual(
            place_dict["created_at"], place.created_at.isoformat()
        )
        self.assertIn("updated_at", place_dict)
        self.assertEqual(
            place_dict["updated_at"], place.updated_at.isoformat()
        )
        self.assertIn("name", place_dict)
        self.assertEqual(place_dict["name"], place.name)
        self.assertIn("city_id", place_dict)
        self.assertEqual(place_dict["city_id"], place.city_id)
        self.assertIn("user_id", place_dict)
        self.assertEqual(place_dict["user_id"], place.user_id)
        self.assertIn("description", place_dict)
        self.assertEqual(place_dict["description"], place.description)
        self.assertIn("number_rooms", place_dict)
        self.assertEqual(place_dict["number_rooms"], place.number_rooms)
        self.assertIn("number_bathrooms", place_dict)
        self.assertEqual(
            place_dict["number_bathrooms"], place.number_bathrooms
        )
        self.assertIn("max_guest", place_dict)
        self.assertEqual(place_dict["max_guest"], place.max_guest)
        self.assertIn("price_by_night", place_dict)
        self.assertEqual(
            place_dict["price_by_night"], place.price_by_night
        )
        self.assertIn("latitude", place_dict)
        self.assertEqual(place_dict["latitude"], place.latitude)
        self.assertIn("longitude", place_dict)
        self.assertEqual(place_dict["longitude"], place.longitude)
        self.assertIn("amenity_ids", place_dict)
        self.assertEqual(place_dict["amenity_ids"], place.amenity_ids)

    def test_str_representation(self):
        """
        Test the string representation of Place
        """
        place = Place()
        str_representation = str(place)
        self.assertTrue("[Place]" in str_representation)
        self.assertTrue(place.id in str_representation)
        self.assertTrue(str(place.__dict__) in str_representation)


if __name__ == "__main__":
    unittest.main()
