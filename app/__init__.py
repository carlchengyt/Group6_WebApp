# Copied from Lecture 6 of COMP0034 and edited by Group 6

from flask import Flask, render_template
from flask_login import LoginManager
from flask_sqlalchemy import SQLAlchemy
from flask_socketio import SocketIO
from config import Config

db = SQLAlchemy()
login_manager = LoginManager()
socketio = SocketIO()


def page_not_found(e):
    return render_template('404.html'), 404


def internal_server_error(e):
    return render_template('500.html'), 500


def create_app(debug=False):
    app = Flask(__name__)
    app.debug = debug
    app.config.from_object(Config)
    db.init_app(app)
    login_manager.init_app(app)

    with app.app_context():
        db.Model.metadata.reflect(db.engine)

    # Register error handlers
    app.register_error_handler(404, page_not_found)
    app.register_error_handler(500, internal_server_error)

    # Register Blueprints

    # Register Blueprints
    from app.main.routes import bp_main
    app.register_blueprint(bp_main)

    from app.team.routes import bp_team
    app.register_blueprint(bp_team)

    from app.auth.routes import bp_auth
    app.register_blueprint(bp_auth)

    from app.chatapp import bp_chatapp
    app.register_blueprint(bp_chatapp)

    from app.project.routes import bp_project
    app.register_blueprint(bp_project)

    from app.userstory.routes import bp_userstory
    app.register_blueprint(bp_userstory)

    socketio.init_app(app)
    return app
