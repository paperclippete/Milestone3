from flask_wtf import FlaskForm
from wtforms import Form, StringField, SelectField
from wtforms.validators import DataRequired

class recipe_search(Form):
    choices = [('title', 'title'),
               ('recipe_description', 'recipe_description'),
               ('ingredients', 'ingredients')]
    select = SelectField('Search for recipes:', choices=choices)
    search = StringField('')