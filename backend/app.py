#----------------------------------------------------------------------------#
# Imports
#----------------------------------------------------------------------------#

import json
import dateutil.parser
import babel
import sys
from flask import Flask, render_template, request, Response, flash, redirect, url_for, jsonify
from flask_moment import Moment
from flask_sqlalchemy import SQLAlchemy
from flask_migrate import Migrate
from models import  Movie,db, Actor

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
  return render_template('pages/home.html')

#------------------------------------------------------------------#
#  Movies
# ----------------------------------------------------------------#

@app.route('/movies')
def movies():
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
  data = Movie.get_by_id_full(movie_id)

  return jsonify({
    "movies": data,
    "Success": True
  })

#  ----------------------------------------------------------------  
#  Create movie
#  ----------------------------------------------------------------

@app.route('/movies/create', methods=['GET'])
def create_movie_form():
  form = MovieForm()
  return render_template('forms/new_movie.html', form=form)

@app.route('/movies/create', methods=['POST'])
def create_movie_submission():

    try:
      title = request.form['title']
      release_date = request.form['release_date']
      website = request.form['website']
      image_link = request.form['image_link']
      facebook_link = request.form['facebook_link']
      description = request.form['description']
      movie = Movie(title = title,release_date=release_date,website=website, image_link=image_link, facebook_link=facebook_link,description=description)
      db.session.add(movie)
      db.session.commit()

      flash('Movie ' + request.form['title'] + ' was successfully listed!')
    except:
      db.session.rollback()
      flash('An error occurred. Movie could not be listed.')

    finally:
      db.session.close()
      return render_template('pages/home.html')

@app.route('/movies/<int:movie_id>', methods=['PATCH'])
def partially_update_movie(movie_id):
    body = request.get_json()
    movie = Movie.query.filter_by(id=movie_id).first()

    if not movie:
        abort(404)
    print(movie)
    movie.description = body.get("description", movie.description)

    db.session.commit()
    return jsonify({
        'success': True,
        'movie': movie.get_by_id_full(movie_id)})


@app.route('/movies/<int:movie_id>', methods=['DELETE'])
def delete_movie(movie_id):
  try:
    movie = db.session.query(Movie).filter_by(id = movie_id).first()
    movie_title = movie.title
    db.session.delete(movie)
    db.session.commit()
    flash('Movie ' + movie_title + ' successfully deleted.')
    print("worked")
  except Exception as err:
    flash('An error occurred. Movie with id ' + movie_id + ' could not be deleted.')

  # BONUS CHALLENGE: Implement a button to delete a Venue on a Venue Page, have it so that
  # clicking that button delete it from the db then redirect the user to the homepage
  return render_template('pages/home.html')





#  actors
#  ----------------------------------------------------------------
@app.route('/actors')
def actors():
  # TODO: replace with real data returned from querying the database
  data= Actor.get_all()
  return render_template('pages/actors.html', actors=data)

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
def single_actor(actor_id):
  # shows the movie page with the given movie_id
  # TODO: replace with real movie data from the movies table, using movie_id
  data = Actor.get_by_id_full(actor_id)
  return render_template('pages/single_actor.html', actor=data)
  
#  Update
#  ----------------------------------------------------------------
@app.route('/actors/<int:actor_id>/edit', methods=['GET'])
def edit_actor(actor_id):
  actor = Actor.get_by_id(actor_id).serialize
  form = ActorForm(**actor)
 

  return render_template('forms/edit_actor.html', form=form, actor=actor)
 
  # TODO: populate form with fields from actor with ID <actor_id>

@app.route('/actors/<int:actor_id>/edit', methods=['POST'])
def edit_actor_submission(actor_id):
  # TODO: take values from the form submitted, and update existing
  # actor record with ID <actor_id> using the new attribute
  form=actorForm()
  try:
      actor = actor.query.get(actor_id)
      actor.name = request.form['name']
      actor.age = request.form['age']
      actor.gender = request.form['gender']

      db.session.commit()
  except:
      print(sys.exc_info())
      db.session.rollback()

  finally:
      db.session.close()

  return redirect(url_for('single_actor', actor_id=actor_id))
  # return redirect(url_for('show_actor', actor_id=actor_id))

@app.route('/movies/<int:movie_id>/edit', methods=['GET'])
def edit_movie(movie_id):
  movie = Movie.get_by_id(movie_id)
  form = MovieForm(**movie)
  print(movie)
  return render_template('forms/edit_movie.html', form=form, movie=movie)

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


@app.errorhandler(404)
def not_found_error(error):
    return render_template('errors/404.html'), 404

@app.errorhandler(500)
def server_error(error):
    return render_template('errors/500.html'), 500


if not app.debug:
    file_handler = FileHandler('error.log')
    file_handler.setFormatter(
        Formatter('%(asctime)s %(levelname)s: %(message)s [in %(pathname)s:%(lineno)d]')
    )
    app.logger.setLevel(logging.INFO)
    file_handler.setLevel(logging.INFO)
    app.logger.addHandler(file_handler)
    app.logger.info('errors')

#----------------------------------------------------------------------------#
# Launch.
#----------------------------------------------------------------------------#

# Default port:
if __name__ == '__main__':
    app.run()

# Or specify port manually:
'''
if __name__ == '__main__':
    port = int(os.environ.get('PORT', 5000))
    app.run(host='0.0.0.0', port=port)
'''
