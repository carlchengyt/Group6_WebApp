from flask import session, redirect, url_for, render_template, request, make_response, flash
from . import bp_chatapp
from .forms import LoginForm
from flask_login import current_user
from app.models import  Project, Team, Userstory, User, TeamUserLink

@bp_chatapp.route('/room', methods=['GET', 'POST'])
def room():
    """Login form to enter a room."""
    if current_user.is_authenticated:
        team_form = LoginForm(request.form)

        name = current_user.name
        user_id = current_user.user_id
        team = TeamUserLink.query.join(Team).with_entities(Team.name)\
            .filter(TeamUserLink.user_id.contains(user_id)).all()
        team_list = [(i.name,i.name)for i in team]
        team_list = list(set(team_list))
        team_list.append(('Public','Public'))
        team_form.team.choices = team_list
        if request.method == 'POST':
            session['Your name'] = name
            session['Team'] = team_form.team.data
            return redirect(url_for('.chat'))
    else:
        response = make_response(redirect(url_for('auth.login')))
        flash('Please Login First To Use The Chat Function')
        return response
    return render_template('chat_index.html', team_form=team_form)


@bp_chatapp.route('/chat')
def chat():
    """Chat room. The user's name and room must be stored in
    the session."""
    name = session.get('Your name', '')
    team = session.get('Team', '')
    if name == '' or room == '':
        return redirect(url_for('.index'))
    return render_template('chat.html', name=name, team=team)
