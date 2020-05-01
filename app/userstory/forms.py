# Written by Student 3 Yifeng Zhao

from flask_wtf import FlaskForm

from wtforms import SelectField, StringField, ValidationError
from wtforms.validators import DataRequired
from wtforms.fields.html5 import DateField

from app import db
from app.models import Team


class UserstoryForm(FlaskForm):
    content = StringField('UserStory Content', validators=[DataRequired()])
    project = SelectField('Project')
    priority = SelectField('Priority', choices=[('EMERGENCY', 'Emergency'), ('NORMAL', 'Normal'), ('SPARE', 'Spare')])
    deadline = DateField('Date of Deadline:', validators=[DataRequired()], format='%Y-%m-%d')
    team = SelectField('Team')

    def validate_deadline(self, today):
        if (today < self.deadline.data):
            return True
        else:
            return False

    def validate_content(self):
        if (len(self.content.data) > 20) and (len(self.content.data) < 400):
            return True
        else:
            return False


class UserstoryUpdateForm(FlaskForm):
    content = StringField('UserStory Content', validators=[DataRequired()])
    priority = SelectField('Priority',
                           choices=[('EMERGENCY', 'Emergency'), ('NORMAL', 'Normal'), ('SPARE', 'Spare'),('COMPLETED','Completed')])
    deadline = DateField('Date of Deadline:', validators=[DataRequired()], format='%Y-%m-%d')
    team = SelectField('Team')

    def validate_deadline(self, today):
        if (today < self.deadline.data):
            return True
        else:
            return False

    def validate_content(self):
        if (len(self.content.data) > 20) and (len(self.content.data) < 400):
            return True
        else:
            return False
