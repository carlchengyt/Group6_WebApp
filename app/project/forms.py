from flask_wtf import FlaskForm
from wtforms import SelectField, StringField, PasswordField, ValidationError, BooleanField, SubmitField, FieldList, \
    FormField
from wtforms.fields.html5 import DateField
from wtforms.validators import DataRequired, Email, EqualTo, Length
from flask import flash, redirect, url_for
from app import db
from app.models import User, Team, TeamUserLink, Project


class ProjectForm(FlaskForm):
    name = StringField('Project Name:', validators=[DataRequired()])
    description = StringField('Project Description:')
    communication = StringField('Project Communication:')
    due_date = DateField('Due Date:', validators=[DataRequired()], format='%Y-%m-%d')
    submit = SubmitField('Submit')

    def validate_project(self, name):
        projects = Project
        results = db.session.query(Project).filter(
            (projects.name == name.data)).first()
        if results is not None:
            raise ValidationError('A project is already registered with this name.')
        else:
            return True

    def validate_due_date(self, today, due_date):
        if due_date.data is not None:
            if (today < self.due_date.data):
                return True
            else:
                raise ValidationError('Due date is set before today.')
        else:
            raise ValidationError('Due date is not set properly.')


class SearchForm(FlaskForm):
    term = StringField('Search', validators=[DataRequired(), Length(min=2, max=60)])