import os
SECRET_KEY = os.urandom(32)
# Grabs the folder where the script runs.
basedir = os.path.abspath(os.path.dirname(__file__))

# Enable debug mode.
DEBUG = True

# Connect to the database


SQLALCHEMY_DATABASE_URI = 'postgres://zsabckmxbixnie:2fb15ea73fb72903a8477049ae37df07f0dc8bc413a895ab3ff85ca40d07fb2d@ec2-174-129-220-12.compute-1.amazonaws.com:5432/d130qfeos1ek7u'
# SQLALCHEMY_DATABASE_URI = 'postgres://rhytah@localhost:5432/capstone'

SQLALCHEMY_TRACK_MODIFICATIONS = False
