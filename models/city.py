#!/usr/bin/python3
"""
City Module
"""
from models.base_model import BaseModel


class City(BaseModel):
    """
    City class
    Attributes:
        state_id (str): empty string (State.id)
        name (str): empty string
    """
    state_id = ""
    name = ""
