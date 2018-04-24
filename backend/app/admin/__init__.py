
from flask import Blueprint
from flask_admin import Admin

from ..models import User


manager = Blueprint('manager', __name__)


from .views import UserView, SettingView


def init_admin(app, db):
    app.config['FLASK_ADMIN_SWATCH'] = 'simplex'
    admin = Admin(app, name='gxblog', template_mode='bootstrap3', base_template='admin/my_master.html')
    admin.add_view(UserView(User, db.session, name='用户'))
    admin.add_view(SettingView(name='设置', endpoint='setting'))

    return admin
