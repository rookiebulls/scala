from flask import Blueprint

players = Blueprint('players', __name__)

from . import routes

