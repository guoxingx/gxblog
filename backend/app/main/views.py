#!coding: utf-8

import functools

from flask import request, redirect, url_for, render_template
from flask_login import login_user, login_required, current_user

from . import main
from .forms import LoginForm, BetOnEtherCreateForm, BetOnEtherDeployForm
from ..models import User, BetOnEther
from .. import login_manager, db


login_manager.login_view = "main.login"


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
            return redirect(request.args.get("next") or url_for("main.index"))

    return render('login.html')


@main.route('/')
@login_required
@roles_required('admin')
def index():
    return render('index.html')


@main.route('/betonether', methods=['GET', 'POST'])
@login_required
@roles_required('admin')
def betonether():
    _id = request.args.get('id')
    boe = BetOnEther.query.get(_id) if _id else None

    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'deploy':
            form = BetOnEtherDeployForm(request.form)
            if boe and form.validate_on_submit():
                boe.deploy(**form.data)

        elif action == 'load':
            address = request.form.get('address')
            if address:
                if not boe:
                    boe = BetOnEther()
                boe.load_contract(address)

        elif action == 'create':
            form = BetOnEtherCreateForm(request.form)
            if form.validate_on_submit():
                if not boe:
                    boe = BetOnEther()
                for k, v in form.data.items():
                    setattr(boe, k, v)
                db.session.add(boe)
                db.session.commit()

    boe_list = BetOnEther.query.all()
    if boe and boe.has_contract:
        boe.sync_data()
    return render('betonether.html', boe=boe, boe_list=boe_list)
