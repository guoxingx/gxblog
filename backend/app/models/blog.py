#!coding: utf-8

from flask import url_for

from .base import BaseModel, BaseRelationTable
from .. import db


blog_tag = BaseRelationTable('blog_tag',
    db.Column('blog_id', db.Integer(), db.ForeignKey('blog.id')),
    db.Column('tag_id', db.Integer(), db.ForeignKey('tag.id')),
)


class Tag(BaseModel):
    """
    """
    name = db.Column(db.String(63), unique=True)


class Blog(BaseModel):
    """
    """
    title = db.Column(db.String(63))
    image = db.Column(db.String(255))
    summary = db.Column(db.String(63))
    path = db.Column(db.String(63))
    tags = db.relationship('Tag', secondary=blog_tag,
                           backref=db.backref('Blog', lazy='dynamic'))

    def add_tags(self, *tagnames):
        print('add_tags', tagnames)
        for name in tagnames:
            if not name:
                continue
            tag = Tag.query.filter_by(name=name).first()
            if not tag:
                tag = Tag(name=name)
                db.session.add(tag)
            self.tags.append(tag)
        db.session.add(self)
        db.session.commit()

    @property
    def tagstring(self):
        tags = self.tags
        res = ('{},' * len(tags)).format(*[t.name for t in tags])
        while res.endswith(','):
            res = res[:-1]
        return res

    @tagstring.setter
    def tagstring(self, tagstring):
        self.add_tags(*[n.strip() for n in tagstring.split(',')])

    def to_json(self):
        return {
            'id': self.id,
            'title': self.title,
            'image': self.image,
            'summary': self.summary,
            'path': url_for('static', filename='blogs/{}'.format(self.path)),
            'tags': [t.name for t in self.tags],
            'created_at': self.created_at.strftime('%Y-%m-%d'),
            'updated_at': self.updated_at.strftime('%Y-%m-%d')
        }
