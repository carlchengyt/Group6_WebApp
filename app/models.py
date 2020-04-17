from app import db
from werkzeug.security import generate_password_hash, check_password_hash
from flask_login import UserMixin


class User(UserMixin, db.Model):
    _table_ = db.Model.metadata.tables['user']
    __table_args__ = {'extend_existing': True}
    user_id = db.Column(db.Integer, primary_key=True)

    def get_id(self):
           return (self.user_id)

    def set_password(self, password):
        self.password = generate_password_hash(password)

    def check_password(self, password):
        return check_password_hash(self.password, password)


class Team(db.Model):
    _table_ = db.Model.metadata.tables['team']
    __table_args__ = {'extend_existing': True}
    team_id = db.Column(db.Integer, primary_key=True)



class Comment(db.Model):
    _table_ = db.Model.metadata.tables['comment']
    __table_args__ = {'extend_existing': True}
    comment_id = db.Column(db.Integer, primary_key=True)


class Project(db.Model):
    _table_ = db.Model.metadata.tables['project']
    __table_args__ = {'extend_existing': True}
    project_id = db.Column(db.Integer, primary_key=True)

class Userstory(db.Model):
    _table_ = db.Model.metadata.tables['userstory']
    __table_args__ = {'extend_existing': True}
    userstory_id = db.Column(db.Integer, primary_key=True)

class TeamUserLink(db.Model):
    _table_ = db.Model.metadata.tables['team_user_link']
    __table_args__ = {'extend_existing': True}
    link_id = db.Column(db.Integer, primary_key=True)