from datetime import datetime
from flask_wtf import Form
from wtforms import StringField, SelectField, SelectMultipleField, DateTimeField, BooleanField, IntegerField
from wtforms.validators import DataRequired, AnyOf, URL


class MovieForm(Form):
    title = StringField(
        'title', validators=[DataRequired()]
    )
    website = StringField(
        'website', validators=[DataRequired()]
    )
    release_date = DateTimeField(
        'release_date', validators=[DataRequired()]
    )
    image_link = StringField(
        'image_link'
    )
    facebook_link = StringField(
        'facebook_link', validators=[URL()]
    )

class ActorForm(Form):
    name = StringField(
        'name', validators=[DataRequired()]
    )
    
    age = IntegerField(
        'age', validators=[DataRequired()]
    )
    gender = StringField(
        'gender', validators=[DataRequired()]
    )
    image_link = StringField(
        'image_link'
    )
