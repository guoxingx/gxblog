# coding: utf-8

from flask import request, url_for, redirect, current_app, render_template, flash
from flask_admin import expose, BaseView
from flask_admin.contrib.sqla import ModelView
from flask_login import current_user, login_user, logout_user

from . import manager
from .forms import AdminLoginForm
from .. import db
from ..utils import form_by_json_request, db_commit
from ..models import User, Role


class WCDModelView(ModelView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('admin'):
            return True

        return False

    def inaccessible_callback(self, *args, **kw):
        return redirect(url_for('backend.login', next=request.url))


class SettingView(BaseView):

    def is_accessible(self):
        if not current_user.is_active or not current_user.is_authenticated:
            return False

        if current_user.has_role('admin'):
            return True

        return False

    @expose('/', methods=['GET', 'POST'])
    def index(self):

        if request.method == 'POST':
            submit = request.args.get('submit')

            if submit == 'headline':
                headline_id = request.args.get('headline_id')
                image = request.files.get('image')
                url = request.form.get('url')
                remove = True if request.args.get('action') == 'remove' else False

                if remove:
                    self.alter_headline(headline_id, remove=True)
                else:
                    if headline_id is not None and (image or url):
                        create = True if headline_id == 'new' else False
                        self.alter_headline(headline_id, image=image, url=url, create=create, remove=False)

        return self.render('admin/setting.html',
                           image_url=lambda name: url_for('static', filename='images/{}'.format(name)),
                           assert_url=lambda name: url_for('static', filename='asserts/{}'.format(name)))


class UserView(WCDModelView):
    can_delete = False
    column_list = ('username',)
    column_details_exclude_list = ('password',)


@manager.before_app_first_request
def before_first_request():
    create_admin()


def create_admin():
    username = current_app.config.get('ADMIN_USERNAME', 'admin')
    password = current_app.config.get('ADMIN_PASSWORD', 'admin123')

    user = User.query.filter_by(username=username).first()
    if not user:
        user = User(username=username, openid=username, password=password)
        db.session.add(user)

    Role.add_role(user, 'admin')
    db_commit()


@manager.route('/', methods=['GET'])
def index():
    if not current_user.is_authenticated:
        return redirect(url_for('backend.login'))
    return render_template('admin/custom/index.html')


@manager.route('/status', methods=['GET', 'POST'])
def status():
    users = User.query.filter_by(active=1).count()
    registers = User.query.filter(User.mobile > 0).count()
    status = {
        'user': users,
        'register': registers
    }
    return render_template('security/status.html', status=status)


@manager.route('/login', methods=['GET', 'POST'])
def login():
    form = form_by_json_request(AdminLoginForm)

    if form.validate_on_submit():
        current_app.logger.info('backend login ok')
        user = verify_user(form.username.data, form.password.data)
        if user:
            login_user(user)
            return redirect('/admin/user')
        else:
            flash('Failed to login. username or password error.', 'error')

    return render_template('admin/custom/login.html', login_user_form=form)


@manager.route('/logout', methods=['GET', 'POST'])
def logout():
    logout_user()
    return redirect(url_for('backend.index'))


def verify_user(username, password):
    user = User.query.filter_by(username=username).filter_by(password=password).first()
    if user:
        return user
