from datetime import datetime


from flask_sqlalchemy import SQLAlchemy

db = SQLAlchemy()


#----------------------------------------------------------------------------#
# Models.
#----------------------------------------------------------------------------#

class Movie(db.Model):
    __tablename__ = 'Movie'

    id = db.Column(db.Integer, primary_key=True)
    title = db.Column(db.String)
    image_link = db.Column(db.String(500))
    facebook_link = db.Column(db.String(120))
    website = db.Column(db.String())
    description = db.Column(db.String())
    release_date = db.Column(db.DateTime)
    deleted = db.Column(db.Boolean, default=False)

    def __repr__(self):
        return f'<Movie self.title {self.title}>'

    def get_enum(self):
        return [
            (movie.id, movie.title)
            for movie in self.query.with_entities(self.id, self.title).all()
        ]

    def get_by_id(self, id):
        return self.query.filter_by(id=id).first_or_404()

    @classmethod
    def get_by_id_full(cls, id):
        details = {}
        movie = cls.get_by_id(id)
        details.update(movie)

        return details

    @classmethod
    def name_search(cls, movie_title):
        movies = cls.query.filter(
            cls.title.ilike(f'%{movie_title}%')
        ).all()
        return [
            {
                "id": movie.id,
                "title": movie.title,
            }
            for movie in movies
        ]

    def exists(self, name):
        return self.query.filter(db.func.lower(self.title) == db.func.lower(title)).count()

    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id).serialize


    @classmethod
    def get_all(cls):
        movies = cls.query.all()
        results = [
            {
                'title': movie.title,
                'website': movie.website,
                'image_link': movie.image_link,
                'description': movie.description,
                'id': movie.id
            }
            for movie in movies
        ]

        return results


    @property
    def serialize(self):
        return {
            'id': self.id,
            'title': self.title,
            'release_date': self.release_date,
            'website': self.website,
            'facebook_link': self.facebook_link,
            'image_link': self.image_link,
            'description':self.description
        }



class Actor(db.Model):
    __tablename__ = 'Actor'

    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String)
    age = db.Column(db.String(120))
    gender = db.Column(db.String(120))
    image_link = db.Column(db.String(500))
   



    def __repr__(self):
        return f'<Actor self.id {self.name}>'


    @classmethod
    def get_by_id(cls, id):
        return cls.query.get_or_404(id)

    @classmethod
    def get_by_id_full(cls, id):
        details = {}
        actor = cls.get_by_id(id)
        details.update(actor.serialize)

        return details
    @classmethod
    def search_actor_name(cls, actor_name):
        movies = cls.query.filter(
            cls.name.ilike(f'%{actor_name}%')
        ).all()
        return [
            {
                "id": actor.id,
                "name": actor.name,
            }
            for actor in actors
        ]
    @classmethod
    def get_all(cls):
        actors = cls.query.all()
        results = [
            {
                'name': actor.name,
                'gender': actor.gender,
                'age': actor.age,
                'image_link': actor.image_link,
                'id': actor.id
            }
            for actor in actors
        ]

        return results

    @property
    def serialize(self):
        return {
            'id': self.id,
            'name': self.name,
            'age': self.age,
            'gender': self.gender,
            'image_link': self.image_link
        }

    def __repr__(self):
        return f'<Actor name: {self.name}>'
    