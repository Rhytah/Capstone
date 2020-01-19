#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
import sys
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify,abort
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import  Movie,db, Actor
from flask_cors import CORS
from auth import AuthError,requires_auth

import logging
from logging import Formatter, FileHandler
from flask_wtf import Form
from forms import *
#----------------------------------------------------------------------------#
# App Config.
#----------------------------------------------------------------------------#

app = Flask(__name__)
moment = Moment(app)
app.config.from_object('config')
migrate = Migrate(app, db)
db.init_app(app)
CORS(app, resources={r"/*": {"origins": "*"}})

@app.after_request
def after_request(response):
    """ configuring CORS"""
    response.headers.add('Access-Control-Allow-Headers',
                            'Content-Type,Authorization,true')
    response.headers.add('Access-Control-Allow-Methods',
                            'GET,PUT,POST,DELETE,OPTIONS')
    return response


# TODO: connect to a local postgresql database


#----------------------------------------------------------------------------#
# Filters.
#----------------------------------------------------------------------------#

def format_datetime(value, format='medium'):
  date = dateutil.parser.parse(value)
  if format == 'full':
      format="EEEE MMMM, d, y 'at' h:mma"
  elif format == 'medium':
      format="EE MM, dd, y h:mma"
  return babel.dates.format_datetime(date, format)

app.jinja_env.filters['datetime'] = format_datetime


#----------------------------------------------------------------------------#
# Controllers.
#----------------------------------------------------------------------------#

@app.route('/')
def index():
  return jsonify({"message":"Welcome to Capstone. A casting agency"})

#------------------------------------------------------------------#
#  Movies
# ----------------------------------------------------------------#

@app.route('/movies')
@requires_auth('view:movies')
def get_movies(payload):
  data = Movie.get_all()

  return jsonify({
    "movies": data,
    "Success": True
  })

@app.route('/movies/search', methods=['POST'])
def search_movies():
    search_term = request.form.get('search_term')
    search_results = Movie.name_search(search_term)
    response = {
        'count': len(search_results),
        'data': search_results
    }

    return jsonify({
      "Successs":True,
      "results":response
    })
@app.route('/movies/<int:movie_id>')
def single_movie(movie_id):
  # shows the movie page with the given movie_id
  data = Movie.query.filter_by(id=movie_id).first()

  return jsonify({
    "movies": data.serialize(),
    "Success": True
  })


@app.route('/movies/create', methods=['POST'])
@requires_auth('add:movie')
def create_movie_submission(payload):
    """
    Create a movie
    """
    data = request.get_json()
    title=data.get("title"),
    release_date=data.get("release_date")
    website= data.get("website")
    image_link= data.get("image_link")
    facebook_link=data.get("facebook_link")
    description=data.get("description")

    new_movie = Movie(
      title=title, release_date=release_date,website=website,image_link=image_link, facebook_link=facebook_link, description=description
    )

    db.session.add(new_movie)
    db.session.commit()
    return jsonify({
        'success': True,
        'movie': new_movie.serialize()
    }), 201


@app.route('/movies/<int:movie_id>', methods=['PATCH'])
@requires_auth('edit:movie')
def partially_update_movie(payload,movie_id):
    """
    Update description of a movie
    """
    body = request.get_json()
    movie = Movie.query.filter_by(id=movie_id).first()

    if not movie:
        abort(404)
    print(movie)
    movie.description = body.get("description", movie.description)

    db.session.commit()
    return jsonify({
        'success': True,
        'movie': movie.serialize()})


@app.route('/movies/<int:movie_id>', methods=['DELETE'])
@requires_auth('delete:movies')
def delete_movie(payload, movie_id):
  """
  Delete a movie basing on it's id
  """
  movie = Movie.query.filter_by(id=movie_id).first()
  
  print(movie)
  if not movie:
    abort(404, "Movie not found")
  movie_title = movie.title

  db.session.delete(movie)
  db.session.commit()

  return jsonify({
      'success': True,
      'message': f'Movie - {movie_title} - has been successfully deleted.'
  }), 200


#  ----------------------------------------------------------------
#  actors
#  ----------------------------------------------------------------
@app.route('/actors')
@requires_auth('view:actors')
def actors(payload):
  """
  Create an actor
  """
  data= Actor.get_all()
  return jsonify({
    "movies": data,
    "Success": True
  })

@app.route('/actors/search', methods=['POST'])
def search_actors():
  # TODO: implement search on actors with partial string search. Ensure it is case-insensitive.
  # seach for "A" should return "Guns N Petals", "Matt Quevado", and "The Wild Sax Band".
  # search for "band" should return "The Wild Sax Band".
  search_term = request.form.get('search_term')
  actors = Actor.search_actor_name(search_term)

  response = {
      "count": len(actors),
      "data": actors
  }
  return render_template('pages/search_actors.html', results=response,
                          search_term=request.form.get('search_term', ''))

@app.route('/actors/<int:actor_id>')
@requires_auth('view:actors')
def single_actor(payload, actor_id):
  """
  Shows the actor with the given movie_id
  """

  data = Actor.get_by_id_full(actor_id)
  return jsonify({
    "movies": data,
    "Success": True
  })
  
#  Update
#  ----------------------------------------------------------------
@app.route('/actors/<int:actor_id>/edit', methods=['PATCH'])
@requires_auth('edit:actor')
def edit_actor(payload,actor_id):
  """
  Update description of a movie
  """
  body = request.get_json()
  actor = Actor.query.filter_by(id=actor_id).first()
 
  if not actor:
      abort(404)
  print(actor)
  actor.name = body.get("name", actor.name)

  db.session.commit()
  return jsonify({
      'success': True,
      'actor': actor.serialize()
      })
 

@app.route('/movies/<int:movie_id>/edit', methods=['POST'])
def edit_movie_submission(movie_id):
  # TODO: take values from the form submitted, and update existing
  # movie record with ID <movie_id> using the new attributes
  return redirect(url_for('single_movie', movie_id=movie_id))

#  Create actor
#  ----------------------------------------------------------------

@app.route('/actors/create', methods=['GET'])
def create_actor_form():
  form = ActorForm()
  return render_template('forms/new_actor.html', form=form)

@app.route('/actors/create', methods=['POST'])
@requires_auth('add:actors')

def create_actor_submission():
  # called upon submitting the new actor listing form
  # TODO: insert form data as a new movie record in the db, instead
  name = request.form['name']
  age = request.form['age']
  gender = request.form['gender']
  image_link = request.form['image_link']
  new_actor = Actor(name = name,age=age,gender=gender, image_link=image_link)
  db.session.add(new_actor)
  db.session.commit()
  # TODO: modify data to be the data object returned from db insertion

  # on successful db insert, flash success
  flash('Actor ' + request.form['name'] + ' was successfully listed!')
  # TODO: on unsuccessful db insert, flash an error instead.
  # e.g., flash('An error occurred. actor ' + data.name + ' could not be listed.')
  return render_template('pages/home.html')


'''
Example error handling for unprocessable entity
'''
@app.errorhandler(422)
def unprocessable(error):
    return jsonify({
        "success": False,
        "error": 422,
        "message": "unprocessable"
    }), 422


@app.errorhandler(400)
def bad_request(error):
    return jsonify({
        "success": False,
        "error": 400,
        "message": error.description
    }), 400


@app.errorhandler(500)
def internal_server_error(error):
    return jsonify({
        "success": False,
        "error": 500,
        "message": 'Internal Server Error. Contact admin!'
    }), 500


@app.errorhandler(405)
def method_not_allowed(error):
    return jsonify({
        "success": False,
        "error": 405,
        "message": 'Method Not Allowed. Double check that you are using the appropriate method for resource.'
    }), 405


'''
@TODO implement error handler for 404
    error handler should conform to general task above 
'''
@app.errorhandler(404)
def not_found(error):
    return jsonify({
        "success": False,
        "error": 404,
        "message": "Resource not found"
    }), 404

@app.errorhandler(AuthError)
def invalid_claims(error):
    return jsonify({
        "success": False,
        "error": 401,
        "message": error.__dict__
    }), 401
