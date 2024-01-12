#!/usr/bin/python3
"""
Review Test Module
"""

import unittest
from models.review import Review


class TestReview(unittest.TestCase):
    """
    Test class for Review
    """

    def test_module_docs(self):
        """
        Test the module documentation
        """
        module_doc = (
            __import__("models.review").review.__doc__
        )
        self.assertGreater(len(module_doc), 0)

    def test_class_docs(self):
        """
        Test the class documentation
        """
        class_doc = (
            __import__("models.review").review.Review.__doc__
        )
        self.assertGreater(len(class_doc), 0)

    def test_attributes_type(self):
        """
        Test the types of attributes in Review
        """
        review = Review()
        self.assertIs(type(review.text), str)
        self.assertIs(type(review.place_id), str)
        self.assertIs(type(review.user_id), str)

    def test_attribute_initialization(self):
        """
        Test that attributes are initialized correctly in Review
        """
        review = Review()
        self.assertEqual(review.text, "")
        self.assertEqual(review.place_id, "")
        self.assertEqual(review.user_id, "")

    def test_to_dict_method(self):
        """
        Test the to_dict method of Review
        """
        review = Review()
        review_dict = review.to_dict()
        self.assertIn("__class__", review_dict)
        self.assertEqual(review_dict["__class__"], "Review")
        self.assertIn("id", review_dict)
        self.assertEqual(review_dict["id"], review.id)
        self.assertIn("created_at", review_dict)
        self.assertEqual(
            review_dict["created_at"], review.created_at.isoformat()
        )
        self.assertIn("updated_at", review_dict)
        self.assertEqual(
            review_dict["updated_at"], review.updated_at.isoformat()
        )
        self.assertIn("place_id", review_dict)
        self.assertEqual(review_dict["place_id"], review.place_id)
        self.assertIn("user_id", review_dict)
        self.assertEqual(review_dict["user_id"], review.user_id)
        self.assertIn("text", review_dict)
        self.assertEqual(review_dict["text"], review.text)

    def test_str_representation(self):
        """
        Test the string representation of Review
        """
        review = Review()
        str_representation = str(review)
        self.assertTrue("[Review]" in str_representation)
        self.assertTrue(review.id in str_representation)
        self.assertTrue(str(review.__dict__) in str_representation)


if __name__ == "__main__":
    unittest.main()
