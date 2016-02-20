from flask.ext.wtf import Form
from wtforms import StringField, TextAreaField, SubmitField, PasswordField
from wtforms.fields.html5 import DateField
from wtforms.validators import Optional, Length, Required, URL, Email, Regexp, EqualTo
from wtforms import ValidationError
from ..models import User, ContentManager


class ProfileForm(Form):
    email = StringField('Email', validators=[Required(), Length(1,64), Email()])
    username = StringField('Username', validators=[Required(), Length(1, 64), \
                        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Username must have only lettters, \
                        numbers or underscore')])
    password = PasswordField('Password', validators=[Required(), \
                           EqualTo('password1', message='Password must match.')])
    password1 = PasswordField('Confirm password', validators=[Required()])
    submit = SubmitField('New')

    def validate_username(self, field):
        if User.query.filter_by(username=field.data).first():
            raise ValidationError('Username has already existed.')


class EditForm(Form):
    email = StringField('Email', validators=[Required(), Length(1,64), Email()])
    username = StringField('Username', validators=[Required(), Length(1, 64), \
                        Regexp('^[A-Za-z][A-Za-z0-9_.]*$', 0, 'Username must have only lettters, \
                        numbers or underscore')])
    password = PasswordField('Password', validators=[EqualTo('password1', message='Password must match.')])
    password1 = PasswordField('Confirm password')
    submit = SubmitField('Edit')


class ContentmanagerForm(Form):
    ip_address = StringField('ServerAddress', validators=[Required()])
    username = StringField('LoginName', validators=[Required()])
    password = PasswordField('LoginPassword', validators=[Required(), EqualTo('password1', message='Password must match.')])
    password1 = PasswordField('Confirm password', validators=[Required()])
    submit = SubmitField('New')

    def validate_ip_address(self, field):
        if ContentManager.query.filter_by(ip_address=field.data).first:
            raise ValidationError('Content manager has already existed.')


class CMEditForm(Form):
    ip_address = StringField('Email', validators=[Required()])
    username = StringField('Username', validators=[Required()])
    password = PasswordField('Password', validators=[EqualTo('password1', message='Password must match.')])
    password1 = PasswordField('Confirm password')
    submit = SubmitField('Edit')

