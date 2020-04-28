from datetime import date
from flask import render_template, Blueprint, request, flash, redirect, url_for, make_response
from flask_login import current_user
from wtforms import ValidationError
from app.project.forms import ProjectForm
from app import db
from app.models import Project, Team, Userstory

bp_project = Blueprint('project', __name__)


@bp_project.route('/Backlog', methods=['GET', 'POST'])
def backlog():
    if current_user.is_authenticated:
        backlogs = Project.query.all()
        backlog_link = Project.query.join(Userstory).with_entities(Project.name.label('project_name'),
                                                                   Project.project_id,
                                                                   Userstory.userstory_id,
                                                                   Userstory.content).order_by(
            Userstory.userstory_id).all()
        return render_template('backlog.html', projects=backlogs, links=backlog_link)
    else:
        response = make_response(redirect(url_for('auth.login')))
        flash('Please Login First To Use The Project Function')
        return response


@bp_project.route('/ProjectCreation', methods=['POST', 'GET'])
def create_project():
    projects = Project.query.all()
    form = ProjectForm(request.form)
    if request.method == 'POST':
        print(form.due_date)
        create_date = date.today()
        if form.communication.data == "":
            form.communication.data = "No Communication"
        if form.description.data == "":
            form.description.data = "No Description"
        try:
            form.validate_project(form.name)
            form.validate_due_date(create_date, form.due_date.data)
            projects = Project(name=form.name.data,
                               description=form.description.data,
                               communication=form.communication.data,
                               assigned_date=create_date,
                               due_date=form.due_date.data)
            db.session.add(projects)
            db.session.commit()
            flash('Project Created Successfully!!!')
            return redirect(url_for('project.backlog'))
        except ValidationError:
            flash('Project Creation Failed')
            return redirect(url_for('project.backlog'))
    return render_template('project_creation.html', form=form, projects=projects)


@bp_project.route('/Project/<term>', methods=['POST', 'GET'])
def project(term):
    projects = Project.query.filter(Project.project_id.contains(term)).all()
    project_link = Project.query.join(Userstory, Team).with_entities(Project.name.label('project_name'),
                                                                     Project.project_id,
                                                                     Userstory.userstory_id,
                                                                     Userstory.content,
                                                                     Userstory.creation_date,
                                                                     Userstory.deadline,
                                                                     Userstory.priority,
                                                                     Team.name.label(
                                                                         'team_name')).order_by(
        Userstory.userstory_id).filter(Userstory.project_id.contains(term)).all()
    userstory_number = Userstory.query.filter(Userstory.project_id.contains(term)).count()
    print("userstory number "+str(userstory_number))
    current_project = Project.query.filter(Project.project_id == term).first()
    print("current project id "+str(current_project.project_id))
    if not project_link:
        flash("This Project has not been fully setup!")

    return render_template('project.html', projects=projects, links=project_link, current_project=current_project,
                           userstory_number=userstory_number)


@bp_project.route('/EditProject/<id>', methods=['POST', 'GET'])
def edit_project(id):
    form = ProjectForm(request.form)
    current_project = Project.query.with_entities(Project.name, Project.project_id, Project.description,
                                                  Project.communication, Project.assigned_date,
                                                  Project.due_date).order_by(
        Project.project_id).filter(Project.project_id.contains(id)).first()

    def clear_project_name():
        clear = Project.query.filter(Project.project_id.contains(id)).first()
        clear.name = '#'
        db.session.commit()

    def update_project(project_name):
        update = Project.query.filter(Project.project_id.contains(id)).first()
        if form.communication.data == "":
            form.communication.data = "No Communication"
        if form.description.data == "":
            form.description.data = "No Description"
        update.name = '{}'.format(project_name)
        update.description = form.description.data
        update.communication = form.communication.data
        update.due_date = form.due_date.data
        db.session.commit()

    if request.method == 'GET':
        # displays default input
        form.name.data = current_project.name
        form.description.data = current_project.description
        form.communication.data = current_project.communication
        # form.due_date.data = current_project.due_date
        return render_template('project_edition.html', form=form)

    elif request.method == 'POST':
        project = Project.query.filter(Project.project_id.contains(id)).first()
        name_backup = project.name
        create_date = date.today()
        try:
            clear_project_name()
            form.validate_project(form.name)
            form.validate_due_date(create_date, form.due_date)
            update_project(form.name.data)
            response = make_response(redirect(url_for('project.project', term=id)))
            return response
        except ValidationError:
            flash("Not validated deadline date")
            project.name = name_backup
            db.session.commit()
            return redirect(url_for('project.edit_project', id=id))
    elif not current_project:
        flash("No Projects Founded!")
        return redirect(url_for('project.backlog'))
    return render_template('project.html', projects=current_project)


@bp_project.route('/Project/<project>/delete', methods=['GET', 'POST'])
def delete_project(project):
    current_project = Project.query.with_entities(Project.name, Project.project_id, Project.description,
                                                  Project.communication,
                                                  Project.assigned_date, Project.due_date).order_by(
        Project.project_id).filter(Project.project_id.contains(project)).first()
    if request.method == 'GET':
        deleted_project = Project.query.filter(Project.project_id.contains(project)).first()
        db.session.delete(deleted_project)
        db.session.commit()
        response = make_response(redirect(url_for('project.backlog')))
        return response
    return render_template('project.html', current_project=current_project)


@bp_project.route('/ProjectSearch', methods=['POST'])
def project_search():
    term = request.form['search_term']
    projects = Project.query.all()
    search_name = Project.query.with_entities(Project.name, Project.project_id, Project.description,
                                              Project.communication,
                                              Project.assigned_date, Project.due_date).order_by(
        Project.project_id).filter(Project.name.contains(term)).all()

    search_description = Project.query.with_entities(Project.name, Project.project_id, Project.description,
                                                     Project.communication,
                                                     Project.assigned_date, Project.due_date).order_by(
        Project.project_id).filter(Project.description.contains(term)).all()

    search_communication = Project.query.with_entities(Project.name, Project.project_id, Project.description,
                                                       Project.communication,
                                                       Project.assigned_date, Project.due_date).order_by(
        Project.project_id).filter(Project.communication.contains(term)).all()
    print(search_communication)

    if request.method == 'POST':
        if term == '':
            flash("Enter a Project Name, Description or Communication")
            return redirect(url_for('project.backlog'))
        results = Project.query.filter(Project.name.contains(term)).all()
        print("name" + str(search_name))
        if not search_name:
            results = Project.query.filter(Project.description.contains(term)).all()
            print("description" + str(search_description))
            if not search_description:
                results = Project.query.filter(Project.communication.contains(term)).all()
                print("communication" + str(search_communication))
                if not results:
                    flash('No Project Found')
                    return redirect(url_for('project.backlog'))
        return render_template("project_search.html", projects=results)
    else:
        return redirect(url_for('project.backlog'))
