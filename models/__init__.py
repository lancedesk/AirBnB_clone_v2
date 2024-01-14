#!/usr/bin/python3
"""
This module handles the storage setup for the HBNB project.
It determines the storage type (database or file) based on the
environment variable HBNB_TYPE_STORAGE and initializes the
appropriate storage instance accordingly.
"""

from os import getenv

storage_type = getenv('HBNB_TYPE_STORAGE')

if storage_type == 'db':
    from models.engine.db_storage import DBStorage
    storage = DBStorage()

else:
    from models.engine.file_storage import FileStorage
    storage = FileStorage()

storage.reload()
