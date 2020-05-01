# Written by Student 4 Zehua Zheng

from flask_wtf import FlaskForm

from wtforms import SelectField, StringField, ValidationError
from wtforms.validators import DataRequired

from app import db
from app.models import Team


class TeamForm(FlaskForm):
    name = StringField('Team name', validators=[DataRequired()])
    leader = SelectField('Team leader', validators=[DataRequired()])
    member1 = SelectField('Team member1')
    member2 = SelectField('Team member2')
    member3 = SelectField('Team member3')
    member4 = SelectField('Team member4')
    member5 = SelectField('Team member5')

    def validate_name(self,name):
        teams = Team
        results = db.session.query(Team).filter(
            (teams.name == name.data)).first()
        if results is not None:
            raise ValidationError('A team is already registered for that team name')
        else:
            return True


class CreateUserstoryForm(FlaskForm):
    userstory = StringField('Userstory', validators=[DataRequired()])
    project = StringField('Project', validators=[DataRequired()])
    priority = StringField('Priority: ', validators=[DataRequired()])
    create_date = StringField('Date of Creation:', validators=[DataRequired])
    deadline = StringField('Date of Creation:', validators=[DataRequired])
    team = StringField('Team', validators=[DataRequired])