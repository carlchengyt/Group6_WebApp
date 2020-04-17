from flask import Blueprint

bp_chatapp = Blueprint('chatapp', __name__)

from . import routes, events
