import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from api import appfrom api.models import Movie, Actor



class CapstoneTestCase(unittest.TestCase):
    """This class represents the Capstone test case"""


    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        self.client = self.app.test_client
        self.database_name = "capstone_test"
        self.database_path = "postgres://rhytah:khaleesi@{}/{}".format('localhost:5432', self.database_name)
        # binds the app to the current context
        with self.app.app_context():
            self.db = SQLAlchemy()
            self.db.init_app(self.app)
            # create all tables
            self.db.create_all()
    
    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_actors_before_signin(self):
        response = self.client().get('/actors')
        data= json.loads(response.data)
        self.assertEqual(response.status_code, 401)


    def test_index(self):
        response= self.client().get('/')
        self.assertEqual(response.status_code,200)

    def test_get_movies_with_no_token(self):
        response= self.client().get('/movies')
        data= json.loads(response.data)
        self.assertEqual(response.status_code, 401)



# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
