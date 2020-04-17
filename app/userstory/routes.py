from flask import render_template, Blueprint, request, make_response, url_for, redirect, flash

from wtforms import ValidationError
from flask_login import current_user

from app.userstory.forms import UserstoryForm, UserstoryUpdateForm

from app import db
from app.models import Comment, Team, Userstory, Project
from datetime import date

bp_userstory = Blueprint('userstory', __name__)


@bp_userstory.route('/userstory_base', methods=['GET'])
def userstory_base():
    if current_user.is_authenticated:

        userstory = Userstory.query.all()
        projects = Project.query.all()
    else:
        response = make_response(redirect(url_for('auth.login')))
        flash('Please Login First To Use The Userstory Function')
        return response
    return render_template('userstory_base.html', userstory=userstory, projects=projects)


@bp_userstory.route('/userstory/project<project_id>', methods=['GET','POST'])
def userstory_info(project_id):
    one_project = Project.query.filter(Project.project_id.contains(project_id)).all()
    projects = Project.query.all()
    if request.method == 'POST':
        term = request.form['search_term']
        results = Userstory.query.join(Project).filter(Project.project_id.contains(project_id)).filter(Userstory.content.contains(term)|Userstory.priority.contains(term)).all()
        if not results:
            flash('No Userstory Found')
        return render_template('userstory_information.html', userstories=results, one_project=one_project)
    else:
        userstories = Userstory.query.join(Team, Project).with_entities(Team.team_id,
                                                                        Team.name.label('team_name'),
                                                                        Userstory.userstory_id, Userstory.content,
                                                                        Userstory.priority,
                                                                        Userstory.creation_date,
                                                                        Userstory.deadline,
                                                                        Project.project_id,
                                                                        Project.name.label('project_name'),
                                                                        Project.description).filter(
                                                                        Project.project_id.contains(project_id)).all()
    return render_template('userstory_information.html', userstories=userstories, one_project=one_project, projects=projects)


@bp_userstory.route('/createNewUserstory', methods=['POST', 'GET'])
def userstory_creation():
    projects = Project.query.all()
    available_team = db.session.query(Team).all()
    available_project = db.session.query(Project).all()

    team_list = [(str(i.team_id), i.name) for i in available_team]
    project_list = [(str(i.project_id), i.name) for i in available_project]

    form = UserstoryForm(request.form)
    form.team.choices = team_list
    form.project.choices = project_list
    create_date = date.today()

    if request.method == 'POST':
        if form.validate_content():
            userstory = Userstory(content=form.content.data,
                                  project_id=form.project.data,
                                  priority=form.priority.data,
                                  creation_date=create_date,
                                  deadline=form.deadline.data,
                                  team_id=form.team.data)
            if form.deadline.data != None and form.validate_deadline(create_date):
                db.session.add(userstory)
                db.session.commit()
                response = make_response(redirect(url_for('userstory.userstory_base')))
                return response
            else:
                flash('Invalid deadline, Please pick dates in the future')
                return redirect(url_for('userstory.userstory_creation'))

        else:
            flash('Too short userstory content, Minimum 20 characters')
            return redirect(url_for('userstory.userstory_creation'))

    return render_template('userstory_creation.html', form=form, projects=projects)


@bp_userstory.route('/project<project_id>/userstory<userstory_id>delete', methods=['GET', 'POST'])
def delete_userstory(userstory_id, project_id):
    projects = Project.query.all()
    userstories = Userstory.query.join(Team, Project).filter(Userstory.userstory_id.contains(userstory_id)).all()
    if request.method == 'GET':
        deleted_userstory = Userstory.query.filter(Userstory.userstory_id.contains(userstory_id)).first()
        db.session.delete(deleted_userstory)
        db.session.commit()
        response = make_response(redirect(url_for('userstory.userstory_info', project_id=project_id)))
        return response
    return render_template('userstory_information.html', userstories=userstories, projects=projects)


@bp_userstory.route('/edit_userstory<userstory_id>/', methods=['GET', 'POST'])
def userstory_edition(userstory_id):
    projects = Project.query.all()
    available_team = db.session.query(Team).all()
    team_list = [(str(i.team_id), i.name) for i in available_team]

    form = UserstoryUpdateForm(request.form)
    form.team.choices = team_list
    today = date.today()

    current_userstory = Userstory.query.filter(Userstory.userstory_id.contains(userstory_id)).first()
    if request.method == 'POST':
        if form.validate_content():
            editing_userstory = Userstory.query.filter(Userstory.userstory_id.contains(userstory_id)).first()
            editing_userstory.content = form.content.data
            editing_userstory.priority = form.priority.data
            editing_userstory.deadline = form.deadline.data
            editing_userstory.team_id = form.team.data
            if form.deadline.data != None and form.validate_deadline(today):
                db.session.commit()
                response = make_response(redirect(url_for('userstory.userstory_base')))
                return response
            else:
                flash('Invalid deadline, Please pick dates in the future')
                return redirect(url_for('userstory.userstory_edition', userstory_id=userstory_id))
        else:
            flash('Too short userstory content, Minimum 20 characters')
            return redirect(url_for('userstory.userstory_edition', userstory_id=userstory_id))

    return render_template('userstory_edition.html', form=form, current_userstory=current_userstory, projects=projects)
