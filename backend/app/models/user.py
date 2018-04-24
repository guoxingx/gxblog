
import time
from flask_login import UserMixin

from .base import BaseModel
from .base import BaseRelationTable
from .. import db


class RoleMixin(object):
    """Mixin for `Role` model definitions"""

    def __eq__(self, other):
        return (self.name == other or
                self.name == getattr(other, 'name', None))

    def __ne__(self, other):
        return not self.__eq__(other)

    def __hash__(self):
        return hash(self.name)


user_role = BaseRelationTable('user_role',
    db.Column('user_id', db.Integer(), db.ForeignKey('user.id')),
    db.Column('role_id', db.Integer(), db.ForeignKey('role.id')),
)


class Role(BaseModel, RoleMixin):
    name = db.Column(db.String(63), unique=True)

    @classmethod
    def add_role(cls, user, rolename):
        from .. import user_datastore
        role = user_datastore.find_or_create_role(rolename)
        user_datastore.add_role_to_user(user, role)

    @classmethod
    def remove_role(cls, user, rolename):
        from .. import user_datastore
        role = user_datastore.find_or_create_role(rolename)
        user_datastore.remove_role_from_user(user, role)


class User(BaseModel, UserMixin):
    username = db.Column(db.String(255), nullable=False, unique=True, index=True)
    password = db.Column(db.String(255), default=time.time())

    roles = db.relationship('Role', secondary=user_role,
                            backref=db.backref('user', lazy='dynamic'))
