from flask_wtf import FlaskForm
from wtforms import StringField, ValidationError, SubmitField, TextAreaField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Length

from app import db
from app.models import Project


class ProjectForm(FlaskForm):
    name = StringField('Project Name:', validators=[DataRequired()])
    description = TextAreaField('Project Description:')
    communication = StringField('Project Communication:')
    due_date = DateField('Due Date:', validators=[DataRequired()], format='%Y-%m-%d')
    submit = SubmitField('Submit')

    def validate_project(self, name):
        projects = Project
        results = db.session.query(Project).filter(
            (projects.name == name.data)).first()
        if results is None:
            if name.data == "":
                raise ValidationError('No Project Name has been entered.')
            else:
                return True
        else:
            raise ValidationError('A project is already registered with this name.')

    def validate_due_date(self, today, due_date):
        if due_date is not None:
            if today < self.due_date.data:
                return True
            else:
                raise ValidationError('Due date is set before today.')
        else:
            raise ValidationError('Due date is not set properly.')


class SearchForm(FlaskForm):
    term = StringField('Search', validators=[DataRequired(), Length(min=2, max=60)])
