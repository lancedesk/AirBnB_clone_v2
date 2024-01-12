#!/usr/bin/python3
"""
State Test Module
"""

import unittest
from models.state import State


class TestState(unittest.TestCase):
    """
    Test class for State
    """

    def test_module_docs(self):
        """
        Test the module documentation
        """
        module_doc = (
            __import__("models.state").state.__doc__
        )
        self.assertGreater(len(module_doc), 0)

    def test_class_docs(self):
        """
        Test the class documentation
        """
        class_doc = (
            __import__("models.state").state.State.__doc__
        )
        self.assertGreater(len(class_doc), 0)

    def test_name_type(self):
        """
        Test the type of the 'name' attribute in State
        """
        state = State()
        self.assertIs(type(state.name), str)

    def test_attribute_initialization(self):
        """
        Test that attributes are initialized correctly in State
        """
        state = State()
        self.assertEqual(state.name, "")

    def test_to_dict_method(self):
        """
        Test the to_dict method of State
        """
        state = State()
        state_dict = state.to_dict()
        self.assertIn("__class__", state_dict)
        self.assertEqual(state_dict["__class__"], "State")
        self.assertIn("id", state_dict)
        self.assertEqual(state_dict["id"], state.id)
        self.assertIn("created_at", state_dict)
        self.assertEqual(
            state_dict["created_at"], state.created_at.isoformat()
        )
        self.assertIn("updated_at", state_dict)
        self.assertEqual(
            state_dict["updated_at"], state.updated_at.isoformat()
        )
        self.assertIn("name", state_dict)
        self.assertEqual(state_dict["name"], state.name)

    def test_str_representation(self):
        """
        Test the string representation of State
        """
        state = State()
        str_representation = str(state)
        self.assertTrue("[State]" in str_representation)
        self.assertTrue(state.id in str_representation)
        self.assertTrue(str(state.__dict__) in str_representation)


if __name__ == "__main__":
    unittest.main()
