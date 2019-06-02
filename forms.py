from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, SubmitField
from wtforms.validators import DataRequired, Email, Length

class user_login_form(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    


class user_register_form(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    firstname = StringField('first_name', validators=[DataRequired()])
    lastname =  StringField('last_name', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])
    
    
class user_update_form(FlaskForm):
    username = StringField('username', validators=[DataRequired()])
    firstname = StringField('first_name', validators=[DataRequired()])
    lastname =  StringField('last_name', validators=[DataRequired()])
    password = PasswordField('password', validators=[DataRequired()])