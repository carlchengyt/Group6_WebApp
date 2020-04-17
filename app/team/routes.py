from flask import render_template, Blueprint, request, make_response, url_for, redirect, flash

from wtforms import ValidationError
from flask_login import current_user
from app.team.forms import TeamForm

from app import db
from app.models import Project, Team, Userstory, User, TeamUserLink

bp_team = Blueprint('team', __name__)


@bp_team.route('/')
def index():
    return render_template('index.html')


@bp_team.route('/team_base', methods=['GET', 'POST'])
def team_base():  # with search function
    if current_user.is_authenticated:

        if request.method == 'POST':
            term = request.form['search_term']
            if term == '':
                flash("Enter a Team Name or Member Name")
                return redirect(url_for('team.team_base'))
            results = Team.query.filter(Team.name.contains(term)).all()
            if not results:
                flash('No Team Found')
            return render_template('team_base.html', teams=results)
        else:
            teams = Team.query.all()
            return render_template('team_base.html', teams=teams)
    else:
        response = make_response(redirect(url_for('auth.login')))
        flash('Please Login First To Use The Team Function')
        return response

@bp_team.route('/team_info<team_id>', methods=['GET','POST'])
def team_info(team_id):
    if current_user.is_authenticated:

        teams = Team.query.all()
        team_leader = Team.query.join(User, User.user_id == Team.leader_user_id).with_entities(
            User.name.label('user_name')).filter(
            Team.team_id.contains(team_id)).all()
        team_details = TeamUserLink.query.join(Team, User).with_entities(Team.name.label('team_name'), Team.team_id,
                                                                         User.name.label('user_name'), User.user_id,
                                                                         User.email).order_by(User.user_id).filter(
            Team.team_id.contains(team_id)).all()
        userstory = Userstory.query.join(Team, Project, Priority).with_entities(Team.team_id,
                                                                                Userstory.userstory_id, Userstory.content,
                                                                                Userstory.creation_date, Userstory.deadline,
                                                                                Project.project_id,
                                                                                Project.name.label('project_name'),
                                                                                Project.description,
                                                                                Priority.priority_level).filter(
            Team.team_id.contains(team_id)).all()
    else:
        response = make_response(redirect(url_for('auth.login')))
        flash('Please Login First To Use The Team Function')
        return response
    return render_template('team_information.html', teams=teams, team_leader=team_leader,
                           team_details=team_details, userstory=userstory)


@bp_team.route('/team_info/team<team_id>/delete', methods=['GET', 'POST'])
def delete_team(team_id):
    if current_user.is_authenticated:
        deleted_team = Team.query.filter(Team.team_id.contains(team_id)).first()
        deleted_team_user_link = TeamUserLink.query.filter(TeamUserLink.team_id.contains(team_id)).all()
        for link in deleted_team_user_link:
            db.session.delete(link)
        db.session.delete(deleted_team)
        db.session.commit()
        response = make_response(redirect(url_for('team.team_base')))
    else:
        response = make_response(redirect(url_for('auth.login')))
        flash('Please Login First To Use The Team Function')
        return response
    return response


@bp_team.route('/createNewTeam', methods=['POST', 'GET'])
def team_creation():
    if current_user.is_authenticated:
        teams = Team.query.all()
        available_users = db.session.query(User).all()
        user_list = [(str(i.user_id), i.name) for i in available_users]
        new_team_form = TeamForm(request.form)
        new_team_form.leader.choices = user_list
        new_team_form.member1.choices = user_list
        new_team_form.member2.choices = user_list
        new_team_form.member3.choices = user_list
        new_team_form.member4.choices = user_list
        new_team_form.member5.choices = user_list

        # def get_userid(userid):
        # id = User.query.with_entities(User.user_id).filter(User.name == userid).all()
        # user_id = id[0][0]
        # return user_id

        def commit_user(team_id, user_id):
            user = TeamUserLink(team_id=team_id, user_id=user_id)
            db.session.add(user)
            db.session.commit()

        if request.method == 'POST':
            ind = 1
            try:
                new_team_form.validate_name(new_team_form.name)
            except:
                db.session.rollback()
                ind = 0
                flash('ERROR! Team name {} already exists. Please try another name'.format(
                    new_team_form.name.data), 'error')
            if ind == 1:
                team = Team(name=new_team_form.name.data, leader_user_id=new_team_form.leader.data)
                db.session.add(team)
                db.session.commit()
                id = Team.query.with_entities(Team.team_id).filter(Team.name == new_team_form.name.data).all()
                team_id = id[0][0]
                # user_id1 = get_userid(form.member1.data)
                # user_id2 = get_userid(form.member2.data)
                # user_id3 = get_userid(form.member3.data)
                # user_id4 = get_userid(form.member4.data)
                # user_id5 = get_userid(form.member5.data)
                commit_user(team_id, new_team_form.member1.data)
                commit_user(team_id, new_team_form.member2.data)
                commit_user(team_id, new_team_form.member3.data)
                commit_user(team_id, new_team_form.member4.data)
                commit_user(team_id, new_team_form.member5.data)
                flash('Team creation successful!')
                response = make_response(redirect(url_for('team.team_base')))
                return response
    else:
        response = make_response(redirect(url_for('auth.login')))
        flash('Please Login First To Use The Team Function')
        return response

    return render_template('team_creation.html', teams=teams, new_team_form=new_team_form)


@bp_team.route('/edit_team<team_id>', methods=['GET', 'POST'])
def team_edition(team_id):
    if current_user.is_authenticated:
        teams = Team.query.all()
        team_name = Team.query.with_entities(Team.name).filter(Team.team_id.contains(team_id)).first()

        available_users = User.query.all()
        user_list = [(i.user_id, i.name) for i in available_users]

        edit_team_form = TeamForm(request.form)
        edit_team_form.leader.choices = user_list
        edit_team_form.member1.choices = user_list
        edit_team_form.member2.choices = user_list
        edit_team_form.member3.choices = user_list
        edit_team_form.member4.choices = user_list
        edit_team_form.member5.choices = user_list

        member_list = []
        member_list.append(edit_team_form.member1.data)
        member_list.append(edit_team_form.member2.data)
        member_list.append(edit_team_form.member3.data)
        member_list.append(edit_team_form.member4.data)
        member_list.append(edit_team_form.member5.data)

        def update_team_member(team_id, new_user_id):
            members = TeamUserLink.query.filter(TeamUserLink.team_id.contains(team_id)).all()
            for i in range(5):
                members[i].user_id = new_user_id[i]
                db.session.commit()

        if request.method == 'POST':
            update_team_member(team_id, member_list)

            team = Team.query.filter(Team.team_id.contains(team_id)).first()
            name_backup = team.name  # copy the current team name
            team.name = ''  # remove current team name to make validation work
            db.session.commit()
            try:
                edit_team_form.validate_name(edit_team_form.name)
                team.leader_user_id = edit_team_form.leader.data
                team.name = '{}'.format(edit_team_form.name.data)
                db.session.commit()
                return redirect(url_for('team.team_info', team_id=team_id))
            except ValidationError:
                flash("The team name is unchanged due to repetition")
                team.name = name_backup
                team.leader_user_id = edit_team_form.leader.data
                db.session.commit()
                return redirect(url_for('team.team_edition', team_id=team_id))
    else:
        response = make_response(redirect(url_for('auth.login')))
        flash('Please Login First To Use The Team Function')
        return response

    return render_template('team_edition.html', teams=teams, team_name=team_name, edit_team_form=edit_team_form)
