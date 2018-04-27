#!coding: utf-8

import functools

from flask import request, redirect, url_for, render_template
from flask_login import login_user, login_required, current_user

from .forms import LoginForm
from . import main
from ..models import User
from .. import login_manager


render = functools.partial(
    render_template,
)


def roles_required(*roles):
    def wrapper(fn):
        @functools.wraps(fn)
        def decorated_view(*args, **kw):
            if 'admin' in roles:
                if not current_user.has_role('admin'):
                    return redirect(url_for('main.login'))
            return fn(*args, **kw)
        return decorated_view
    return wrapper


def verify_user(username, password):
    user = User.query.filter_by(username=username).filter_by(password=password).first()
    if user:
        return user


@login_manager.user_loader
def load_user(user_id):
    return User.query.get(user_id)


@main.route('/login', methods=['GET', 'POST'])
def login():
    form = LoginForm(request.form)
    if form.validate_on_submit():
        username = form.username.data
        password = form.password.data
        user = verify_user(username, password)
        if user:
            login_user(user)

    return render('login.html')


@main.route('/')
@login_required
@roles_required('admin')
def index():
    return render('index.html')


@main.route('/betonether', method=['GET', 'POST'])
@login_required
@roles_required('admin')
def betonether():
    if request.method == 'POST':
        pass

    return render('betonether_setting.html')
