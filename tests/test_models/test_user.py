#!/usr/bin/python3
"""
User Test Module
"""

import unittest
from models.user import User


class TestUser(unittest.TestCase):
    """
    Test class for User
    """

    def test_module_docs(self):
        """
        Test the module documentation
        """
        module_doc = (
            __import__("models.user").user.__doc__
        )
        self.assertGreater(len(module_doc), 0)

    def test_class_docs(self):
        """
        Test the class documentation
        """
        class_doc = (
            __import__("models.user").user.User.__doc__
        )
        self.assertGreater(len(class_doc), 0)

    def test_attributes_type(self):
        """
        Test the type of attributes in User
        """
        user = User()
        self.assertIs(type(user.email), str)
        self.assertIs(type(user.password), str)
        self.assertIs(type(user.first_name), str)
        self.assertIs(type(user.last_name), str)

    def test_attribute_initialization(self):
        """
        Test that attributes are initialized correctly in User
        """
        user = User()
        self.assertEqual(user.email, "")
        self.assertEqual(user.password, "")
        self.assertEqual(user.first_name, "")
        self.assertEqual(user.last_name, "")

    def test_to_dict_method(self):
        """
        Test the to_dict method of User
        """
        user = User()
        user_dict = user.to_dict()
        self.assertIn("__class__", user_dict)
        self.assertEqual(user_dict["__class__"], "User")
        self.assertIn("id", user_dict)
        self.assertEqual(user_dict["id"], user.id)
        self.assertIn("created_at", user_dict)
        self.assertEqual(
            user_dict["created_at"], user.created_at.isoformat()
        )
        self.assertIn("updated_at", user_dict)
        self.assertEqual(
            user_dict["updated_at"], user.updated_at.isoformat()
        )
        self.assertIn("email", user_dict)
        self.assertEqual(user_dict["email"], user.email)
        self.assertIn("password", user_dict)
        self.assertEqual(user_dict["password"], user.password)
        self.assertIn("first_name", user_dict)
        self.assertEqual(user_dict["first_name"], user.first_name)
        self.assertIn("last_name", user_dict)
        self.assertEqual(user_dict["last_name"], user.last_name)

    def test_str_representation(self):
        """
        Test the string representation of User
        """
        user = User()
        str_representation = str(user)
        self.assertTrue("[User]" in str_representation)
        self.assertTrue(user.id in str_representation)
        self.assertTrue(str(user.__dict__) in str_representation)


if __name__ == "__main__":
    unittest.main()
