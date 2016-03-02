from flask import render_template, flash, redirect, url_for, abort, request, current_app
from flask.ext.login import login_required, current_user
from .. import db
from ..models import User, Player, ContentManager
from . import players
from .forms import ProfileForm, EditForm, ContentmanagerForm, CMEditForm
import requests


@players.route('/')
def index():
    try:
        page = request.args.get('page', 1, type=int)
        pagination = Player.query.order_by(Player.last_player_heartbeat.desc()).paginate(
            page, per_page=current_app.config['PLAYER_PER_PAGE'],
            error_out=False)
        players = pagination.items
        cms = ContentManager.query.all()
        return render_template('players/index.html', players=players, cms=cms, pagination=pagination)
    except Exception, e:
        return str(e)



@players.route('/user/<username>')
@login_required
def user(username):
    user = User.query.filter_by(username=username).first_or_404()
    users = User.query.all()
    return render_template('players/user.html', user=user, users=users)


@players.route('/players/contentmanager/<int:id>')
def sorted_players(id):
    try:
        cms = ContentManager.query.all()
        cm = ContentManager.query.get_or_404(id)
        page = request.args.get('page', 1, type=int)
        pagination = cm.players.order_by(Player.last_player_heartbeat.desc()).paginate(
            page, per_page=current_app.config['PLAYER_PER_PAGE'],
            error_out=False)
        players = pagination.items
        return render_template('players/sorted_players.html', players=players, cms=cms, pagination=pagination, id=id)
    except Exception, e:
        return str(e)


@players.route('/screen/<int:id>')
def screen(id):
    player = Player.query.get_or_404(id)
    cms = ContentManager.query.all()
    return render_template('players/screen.html', player=player, cms=cms)


@players.route('/user/new', methods=['GET', 'POST'])
@login_required
def new_user():
    form = ProfileForm()
    if form.validate_on_submit():
        email = form.email.data
        username = form.username.data
        password = form.password.data
        user = User(email=email, username=username, password=password)
        db.session.add(user)
        db.session.commit()
        flash('Successfully add a new user.')
        return redirect(url_for('players.user', username=current_user.username))
    return render_template('players/add_user.html', form=form)


@players.route('/user/edit/<username>', methods=['GET', 'POST'])
@login_required
def edit_user(username):
    form = EditForm()
    user = User.query.filter_by(username=username).first_or_404()
    if form.validate_on_submit():
        user.email = form.email.data
        user.username = form.username.data
        user.password = form.password.data
        db.session.add(user)
        db.session.commit()
        flash('Successfully edit user.')
        return redirect(url_for('players.user', username=current_user.username))
    form.email.data = user.email
    form.username.data = user.username
    return render_template('players/edit_user.html', form=form)


@players.route('/user/delete/<username>', methods=['GET','POST'])
@login_required
def delete_user(username):
    user = User.query.filter_by(username=username).first_or_404()
    db.session.delete(user)
    db.session.commit()
    flash('Successfully delete a user.')
    return redirect(url_for('players.user', username=current_user.username))


@players.route('/contentmanager')
@login_required
def contentmanager():
    cms = ContentManager.query.all()
    return render_template('players/cm.html', cms=cms)


@players.route('/contentmanager/new', methods=['GET', 'POST'])
@login_required
def new_cm():
    form = ContentmanagerForm()
    if form.validate_on_submit():
        ip_address = form.ip_address.data
        username = form.username.data
        password = form.password.data
        CM_LOGIN = {"username": username, "password": password}
        try:
            r = requests.post("%s/api/rest/auth/login" % ip_address, json=CM_LOGIN)
            authinfo = r.json()
            if authinfo.get('token') is not None:
                cm = ContentManager(ip_address=ip_address, username=username, password=password)
                db.session.add(cm)
                db.session.commit()
                flash('Successfully add a new content manager.')
                return redirect(url_for('players.contentmanager'))
            else:
                flash('Invalid username or password.')
        except Exception, e:
            flash(e)

    return render_template('players/add_cm.html', form=form)

    

@players.route('/contentmanager/edit/<int:id>', methods=['GET', 'POST'])
@login_required
def edit_cm(id):
    form = CMEditForm()
    cm = ContentManager.query.get_or_404(id)
    if form.validate_on_submit():
        cm.ip_address = form.ip_address.data
        cm.username = form.username.data
        cm.password = form.password.data
        db.session.add(cm)
        db.session.commit()
        flash('Successfully edit content manager.')
        return redirect(url_for('players.contentmanager'))
    form.ip_address.data = cm.ip_address
    form.username.data = cm.username
    return render_template('players/edit_user.html', form=form)


@players.route('/contentmanager/delete/<int:id>', methods=['GET','POST'])
@login_required
def delete_cm(id):
    cm = ContentManager.query.get_or_404(id)
    db.session.delete(cm)
    db.session.commit()
    flash('Successfully delete a content manager.')
    return redirect(url_for('players.contentmanager'))