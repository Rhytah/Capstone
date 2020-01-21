import os
from flask import Flask
from functools import wraps
from unittest.mock import patch
import unittest
import json
from src import app
from src.error_handlers import error_handlers
from flask_sqlalchemy import SQLAlchemy


def mock_func(x=''):
    def decorator(f):
        @wraps(f)
        def wrapper(*args, **kwargs):
            payload = x
            return f(payload, *args, **kwargs)
        return wrapper
    return decorator

""" overiding requires_auth decorator """
patch('src.views.actors.requires_auth', mock_func).start()
from src.views.actors import actors_app

myApp = Flask(__name__)
actors_app(myApp)
error_handlers(myApp)

class ActorsTestCase(unittest.TestCase):

    def setUp(self):
        self.client = myApp.test_client()

    def test_get_actors(self):
        """ Test get actors endpoint """
        response = self.client.get('/actors')
        body = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertTrue(isinstance(body['actors'], list))

    def test_delete_actors(self):
        """ Test delete actors endpoint """
        response = self.client.delete('/actors/1')
        body = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(body['message'], 'Actor Successfully deleted.')

    def test_post_actors(self):
        """ Test post actors endpoint """
        body = {
            "age": 2,
            "gender": "female",
            "name": "test"
        }
        response = self.client.post('/actors',
                                    content_type='application/json',
                                    data=json.dumps(body))
        body = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 201)
        self.assertEqual(body['actor']['name'], 'test')

    def test_patch_actors(self):
        """ Test update actors endpoint """
        body = {"name": "patch"}
        response = self.client.patch('/actors/2',
                                    content_type='application/json',
                                    data=json.dumps(body))
        body = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 200)
        self.assertEqual(body['actor']['name'], 'patch')

    ##################
    # error behavior #
    ##################

    def test_patch_actor(self):
        """ Test patch actors endpoint with unexisting id """
        response = self.client.patch('/actors/0')
        body = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 404)
        self.assertEqual(body['message'], "resource not found")

    def test_post_actor(self):
        """ Test post actors endpoint with a string as age """
        body = {
            "age": "test",
            "gender": "female",
            "name": "test"
        }
        response = self.client.post('/actors',
                                    content_type='application/json',
                                    data=json.dumps(body))
        body = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(body['message'], ['Age should be an integer.'])

    def test_actor_patch(self):
        """ Test update actors endpoint with integer as name """
        body = {"name": 1000}
        response = self.client.patch('/actors/2',
                                    content_type='application/json',
                                    data=json.dumps(body))
        body = json.loads(response.data.decode())
        self.assertEqual(response.status_code, 400)
        self.assertEqual(body['message'], ['name should be a string.'])


if __name__ == "__main__":
    unittest.main()
