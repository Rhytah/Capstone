import os
import unittest
import json
from flask_sqlalchemy import SQLAlchemy

from run import app
from models import Movie, Actor


class CapstoneTestCase(unittest.TestCase):
    """This class represents the casting agency test case"""

    def setUp(self):
        """Define test variables and initialize app."""
        self.app = app
        self.client = self.app.test_client
        self.executive_producer_token = 'eyJhbGciOiJSUzI1NiIsInR5cCI6IkpXVCIsImtpZCI6Ik9EVTVOekk1T1VZMk9URTJSVUU0TURFNE5qUTRRMEkwT0VGRU1qazRSVGd5TmpWRFFUQkNPQSJ9.eyJpc3MiOiJodHRwczovL3JoeXRhaC5hdXRoMC5jb20vIiwic3ViIjoiZ29vZ2xlLW9hdXRoMnwxMDI2NjI3NDk2MTgxMjY4MTM4MzIiLCJhdWQiOlsiY2Fwc3RvbmUiLCJodHRwczovL3JoeXRhaC5hdXRoMC5jb20vdXNlcmluZm8iXSwiaWF0IjoxNTc5Njg2MDE5LCJleHAiOjE1Nzk2OTMyMTksImF6cCI6IjZ6cHVrQ2dlMnZJWDJSWnB3VGxCcEJxTDAwRmcycEhBIiwic2NvcGUiOiJvcGVuaWQgcHJvZmlsZSBlbWFpbCIsInBlcm1pc3Npb25zIjpbImFkZDphY3RvcnMiLCJhZGQ6bW92aWUiLCJkZWxldGU6YWN0b3JzIiwiZGVsZXRlOm1vdmllcyIsImVkaXQ6YWN0b3IiLCJlZGl0Om1vdmllIiwidmlldzphY3RvcnMiLCJ2aWV3Om1vdmllcyJdfQ.kKJFonoZMbP0-NjkrvAcDULljZ_MZDWW9OWfon5PrmeMfIe4pt8PSxWVi8z1X4BHrISrbYSzZf7gMZrKeci2AUr024tNaUrz9USgKAHXc6LK5dEtq1Y5DCar_NfBlu9hsCNo1U2wkdcHVpFdfB78tSDEnGzDjrKqcfWRPYqhkDeO6Y4zPNd_jgCsQZWOMvrRvEmCes8I0FxEUBsqaT302uS7292hAA8ZvY8ykoSqJ-jfTqTyv0OfHJBZSrz1g4bwydWYDNbxAr9laxbboVNTfMnwXQhfELfflcdQtJ42Yo0bCrBUf-J-t9knz6UhHwXoOwOpKP8FZmN154Z0lGwfeQ'

    def tearDown(self):
        """Executed after reach test"""
        pass

    def test_get_actors_before_signin(self):
        response = self.client().get('/actors')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)

    def test_index(self):
        response = self.client().get('/')
        self.assertEqual(response.status_code, 200)

    def test_get_movies_with_no_token(self):
        response = self.client().get('/movies')
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 401)

    def test_create_actors_without_token_fails(self):
        payload = {
            'name': 'mimi',
            'gender': 'female',
            'age': 18,
            'image_link': 'image'
        }
        response = self.client().post(
            '/actors/create',
            json=payload)
        self.assertEqual(response.status_code, 401)

    # Executive producer tests
    def test_get_actors_as_executive_producer(self):

        response = self.client().get(
            '/actors',
            headers={
                "Authorization":
                    "Bearer {}".format(self.executive_producer_token)
            }
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    def test_get_movies(self):

        response = self.client().get(
            '/movies',
            headers={
                "Authorization":
                    "Bearer {}".format(self.executive_producer_token)
            }
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    def test_get_actors_as_executive_producer(self):

        response = self.client().get(
            '/actors',
            headers={
                "Authorization":
                    "Bearer {}".format(self.executive_producer_token)
            }
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    def test_get_specific_movies(self):

        response = self.client().get(
            '/movies/1',
            headers={
                "Authorization":
                    "Bearer {}".format(self.executive_producer_token)
            }
        )
        data = json.loads(response.data)
        self.assertEqual(response.status_code, 200)

    def test_delete_movies_fails_without_token(self):
        response = self.client().delete(
            '/movies/1'
        )
        self.assertEqual(response.status_code, 401)


# Make the tests conveniently executable
if __name__ == "__main__":
    unittest.main()
