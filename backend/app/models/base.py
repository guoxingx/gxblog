
from .. import db


class BaseModel(db.Model):
    """
    Base model include id, created_at, updated_at columns
    """
    __abstract__ = True

    created_at = db.Column(db.TIMESTAMP(timezone=True), nullable=False,
                        server_default=db.text('CURRENT_TIMESTAMP'))
    updated_at = db.Column(db.TIMESTAMP(timezone=True), nullable=False,
                        server_default=db.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    id = db.Column(db.Integer, primary_key=True)


class NoIdBaseModel(db.Model):
    __abstract__ = True

    created_at = db.Column(db.TIMESTAMP(timezone=True), nullable=False,
                        server_default=db.text('CURRENT_TIMESTAMP'))
    updated_at = db.Column(db.TIMESTAMP(timezone=True), nullable=False,
                        server_default=db.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))


def BaseRelationTable(*args, **kw):
    """
    Base relation table include created_at, updated_at columns.
    """
    created_at = db.Column('created_at', db.TIMESTAMP(timezone=True), nullable=False,
                        server_default=db.text('CURRENT_TIMESTAMP'))
    updated_at = db.Column('updated_at', db.TIMESTAMP(timezone=True), nullable=False,
                        server_default=db.text('CURRENT_TIMESTAMP ON UPDATE CURRENT_TIMESTAMP'))
    args += (created_at, updated_at)
    return db.Table(*args, **kw)
