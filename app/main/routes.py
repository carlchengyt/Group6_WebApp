# Written by Student 1 Yutong Cheng
from flask import render_template, Blueprint, request, make_response, url_for, redirect


from app import db
from app.models import Comment, Project, Team, Userstory, User, TeamUserLink

bp_main = Blueprint('main', __name__)


@bp_main.route('/')
def home():
    return render_template('home.html')
