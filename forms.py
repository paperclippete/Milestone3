from flask_wtf import FlaskForm
from wtforms import StringField, PasswordField, BooleanField
from wtforms.validators import InpputRequired, Email, Length

class loginForm(FlaskForm):
    username = StringField('username')
    password = PasswordField('password')
    
