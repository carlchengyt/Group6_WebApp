from flask_wtf import FlaskForm
from wtforms.fields import StringField,SelectField, SubmitField
from wtforms.validators import Required


class LoginForm(FlaskForm):
    """Accepts a nickname and a room."""
    team = SelectField('team')
    submit = SubmitField('Enter Chatroom')
