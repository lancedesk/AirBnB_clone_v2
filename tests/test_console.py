#!/usr/bin/python3
"""
Unit tests for HBNBCommand class in console.py.
"""

import json
import MySQLdb
import os
import sqlalchemy
import unittest
from io import StringIO
from unittest.mock import patch

from console import HBNBCommand
from models import storage
from models.base_model import BaseModel
from models.user import User
from tests import clear_stream


class TestHBNBCommand(unittest.TestCase):
    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') == 'db', 'FileStorage test')
    def test_fs_create(self):
        """
        Test the 'create' command for FileStorage.

        This method tests the creation of City and User instances using the
        'create' command in the console. It verifies that the instances are
        successfully created and their attributes can be displayed using the
        'show' command.

        """

        with patch('sys.stdout', new=StringIO()) as cout:
            command = HBNBCommand()
            command.onecmd('create City name="Nairobi"')
            model_id = cout.getvalue().strip()
            clear_stream(cout)
            self.assertIn('City.{}'.format(model_id), storage.all().keys())
            command.onecmd('show City {}'.format(model_id))
            self.assertIn("'name': 'Nairobi'", cout.getvalue().strip())
            clear_stream(cout)
            command.onecmd('create User name="Robert" age=34 height=6.1')
            model_id = cout.getvalue().strip()
            self.assertIn('User.{}'.format(model_id), storage.all().keys())
            clear_stream(cout)
            command.onecmd('show User {}'.format(model_id))
            self.assertIn("'name': 'Robert'", cout.getvalue().strip())
            self.assertIn("'age': 34", cout.getvalue().strip())
            self.assertIn("'height': 6.1", cout.getvalue().strip())

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') != 'db', 'DBStorage test')
    def test_db_create(self):
        """
        Test the 'create' command for DBStorage.

        Tests creation of a User instance with non-null attributes
        using 'create' command in console. It verifies that instance is
        successfully created and its attributes are correctly stored in the
        database.

        """

        with patch('sys.stdout', new=StringIO()) as cout:
            command = HBNBCommand()
            # creating a model with non-null attribute(s)
            with self.assertRaises(sqlalchemy.exc.OperationalError):
                command.onecmd('create User')
            # creating a User instance
            clear_stream(cout)
            command.onecmd('create User '
                           'email="lncedesk@gmail.com" '
                           'password="456"')
            model_id = cout.getvalue().strip()
            connection = MySQLdb.connect(
                host=os.getenv('HBNB_MYSQL_HOST'),
                port=3306,
                user=os.getenv('HBNB_MYSQL_USER'),
                passwd=os.getenv('HBNB_MYSQL_PWD'),
                db=os.getenv('HBNB_MYSQL_DB')
            )
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM users WHERE id="{}"'
                           .format(model_id))
            result = cursor.fetchone()
            self.assertTrue(result is not None)
            self.assertIn('lncedesk@gmail.com', result)
            self.assertIn('456', result)
            cursor.close()
            connection.close()

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') != 'db', 'DBStorage test')
    def test_db_show(self):
        """
        Test the 'show' command for DBStorage.

        This method tests 'show' command for a User instance in DBStorage. It
        creates a User instance, saves it to database, and then checks if
        'show' command displays the correct attributes of the instance.

        """

        with patch('sys.stdout', new=StringIO()) as cout:
            command = HBNBCommand()
            # showing a User instance
            obj = User(email="lncedesk@gmail.com", password="456")
            connection = MySQLdb.connect(
                host=os.getenv('HBNB_MYSQL_HOST'),
                port=3306,
                user=os.getenv('HBNB_MYSQL_USER'),
                passwd=os.getenv('HBNB_MYSQL_PWD'),
                db=os.getenv('HBNB_MYSQL_DB')
            )
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM users WHERE id="{}"'.format(obj.id))
            result = cursor.fetchone()
            self.assertTrue(result is None)
            command.onecmd('show User {}'.format(obj.id))
            self.assertEqual(
                cout.getvalue().strip(),
                '** no instance found **'
            )
            obj.save()
            connection = MySQLdb.connect(
                host=os.getenv('HBNB_MYSQL_HOST'),
                port=3306,
                user=os.getenv('HBNB_MYSQL_USER'),
                passwd=os.getenv('HBNB_MYSQL_PWD'),
                db=os.getenv('HBNB_MYSQL_DB')
            )
            cursor = connection.cursor()
            cursor.execute('SELECT * FROM users WHERE id="{}"'.format(obj.id))
            clear_stream(cout)
            command.onecmd('show User {}'.format(obj.id))
            result = cursor.fetchone()
            self.assertTrue(result is not None)
            self.assertIn('lncedesk@gmail.com', result)
            self.assertIn('456', result)
            self.assertIn('lncedesk@gmail.com', cout.getvalue())
            self.assertIn('456', cout.getvalue())
            cursor.close()
            connection.close()

    @unittest.skipIf(
        os.getenv('HBNB_TYPE_STORAGE') != 'db', 'DBStorage test')
    def test_db_count(self):
        """
        Test the 'count' command for DBStorage.

        This method tests the 'count' command for a specified model class in
        DBStorage. Counts number of instances of State class before and
        after creating a new State instance, ensuring that count is correctly
        incremented.

        """

        with patch('sys.stdout', new=StringIO()) as cout:
            command = HBNBCommand()
            connection = MySQLdb.connect(
                host=os.getenv('HBNB_MYSQL_HOST'),
                port=3306,
                user=os.getenv('HBNB_MYSQL_USER'),
                passwd=os.getenv('HBNB_MYSQL_PWD'),
                db=os.getenv('HBNB_MYSQL_DB')
            )
            cursor = connection.cursor()
            cursor.execute('SELECT COUNT(*) FROM states;')
            res = cursor.fetchone()
            prev_count = int(res[0])
            command.onecmd('create State name="Nairobi"')
            clear_stream(cout)
            command.onecmd('count State')
            cnt = cout.getvalue().strip()
            self.assertEqual(int(cnt), prev_count + 1)
            clear_stream(cout)
            command.onecmd('count State')
            cursor.close()
            connection.close()
