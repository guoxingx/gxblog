#!coding: utf-8

import functools

from flask import request, redirect, url_for, render_template, current_app
from flask_login import login_user, login_required, current_user

from . import main
from .forms import LoginForm, BetOnEtherCreateForm, BetOnEtherDeployForm
from ..models import User, BetOnEther, Role
from ..utils import get_node_status
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
    qa = request.args.get('q')
    boe = BetOnEther.query.get(_id) if _id else None
    if boe and boe.deleted:
        boe = None

    if request.method == 'POST':
        action = request.form.get('action')
        if action == 'deploy':
            form = BetOnEtherDeployForm(request.form)
            if boe and form.validate_on_submit():
                boe.deploy(**form.data)

        if action == 'txhash':
            boe.load_contract_by_tx_hash()

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

        elif action == 'delete':
            boe.deleted = True
            db.session.add(boe)
            db.session.commit()

        elif action == 'confirm':
            result = request.form.get('result')
            password = request.form.get('password')
            boe.confirm(int(result), password)

        elif action == 'clear':
            password = request.form.get('password')
            boe.clear(password)

    node_status_dict = get_node_status()
    node_status = node_status_dict.get('status')

    boe_list = BetOnEther.query.filter_by(deleted=False).order_by(BetOnEther.created_at.desc()).all()
    if not node_status and boe and boe.has_contract:
        boe.sync_data()

    bet_list = None
    if boe and boe.contract_status == 2 and qa:
        bet_list = boe.query_bets(qa)

    return render('betonether.html', boe=boe, boe_list=boe_list, bet_list=bet_list, node_status_dict=node_status_dict)


@main.before_app_first_request
def before_first_request():
    create_admin()


def create_admin():
    username = current_app.config.get('ADMIN_USERNAME', 'admin')
    password = current_app.config.get('ADMIN_PASSWORD', 'admin123')

    user = User.query.filter_by(username=username).first()
    if not user:
        user = User(username=username, password=password)
        db.session.add(user)

    Role.add_role(user, 'admin')
    db.session.commit()
