#!/usr/bin/env python
import os
from app import create_app
from flask.ext.script import Manager, Shell
from app import db
from app.models import User, ContentManager, Player

app = create_app(os.getenv('FLASK_CONFIG') or 'default')
manager = Manager(app)

def make_shell_context():
    return dict(app=app, db=db, Player=Player, ContentManager=ContentManager, User=User)
manager.add_command('shell', Shell(make_context=make_shell_context))

@manager.command
def adduser(email, username, admin=False):
    """Register a new user."""
    from getpass import getpass
    password = getpass()
    password2 = getpass(prompt='Confirm: ')
    if password != password2:
        import sys
        sys.exit('Error: passwords do not match.')
    db.create_all()
    user = User(email=email, username=username, password=password,
                is_admin=admin)
    db.session.add(user)
    db.session.commit()
    print('User {0} was registered successfully.'.format(username))



if __name__ == '__main__':
    manager.run()

