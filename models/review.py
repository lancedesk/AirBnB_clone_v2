#!/usr/bin/python3
"""
Review Module
"""
from models.base_model import BaseModel


class Review(BaseModel):
    """
    Review class
    Attributes:
        place_id (str): empty string (Place.id)
        user_id (str): empty string (User.id)
        text (str): empty string
    """
    place_id = ""
    user_id = ""
    text = ""
