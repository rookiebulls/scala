from datetime import datetime
import hashlib
from werkzeug.security import generate_password_hash, check_password_hash
from flask import request
from flask.ext.login import UserMixin
from . import db, login_manager
import base64


class User(UserMixin, db.Model):
    __tablename__ = 'users'
    id = db.Column(db.Integer, primary_key=True)
    email = db.Column(db.String(64),
                      nullable=False, unique=True, index=True)
    username = db.Column(db.String(64),
                         nullable=False, unique=True, index=True)
    is_admin = db.Column(db.Boolean)
    password_hash = db.Column(db.String(128))

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = generate_password_hash(password)

    def verify_password(self, password):
        return check_password_hash(self.password_hash, password)



@login_manager.user_loader
def load_user(user_id):
    return User.query.get(int(user_id))


class Player(db.Model):
    __tablename__ = 'players'
    id = db.Column(db.Integer, primary_key=True)
    name = db.Column(db.String(128), nullable=False)
    last_player_heartbeat = db.Column(db.DateTime())
    last_player_issue = db.Column(db.Text())
    last_player_state = db.Column(db.String(64))
    last_screen_issue = db.Column(db.Text())
    screen_type = db.Column(db.String(64))
    power_status = db.Column(db.String(64))
    resolution = db.Column(db.String(64))
    brightness = db.Column(db.String(64))
    contrast = db.Column(db.String(64))
    powered_on_hours = db.Column(db.Integer)
    backlight_on_hours = db.Column(db.Integer)
    cm_id = db.Column(db.Integer, db.ForeignKey('contentmanagers.id'))

class ContentManager(db.Model):
    __tablename__ = 'contentmanagers'
    id = db.Column(db.Integer, primary_key=True)
    ip_address = db.Column(db.String(128),
                      nullable=False, unique=True, index=True)
    username = db.Column(db.String())
    password_hash = db.Column(db.String())
    players = db.relationship('Player', lazy='dynamic', backref='contentmanager')

    @property
    def password(self):
        raise AttributeError('password is not a readable attribute')

    @password.setter
    def password(self, password):
        self.password_hash = base64.encodestring(password)
