#!coding: utf-8

from flask import url_for

from .base import BaseResource
from ..models import Blog as BlogModel


class Blogs(BaseResource):

    def get(self):
        blogs = BlogModel.query.order_by(BlogModel.created_at.desc()).all()
        return [b.to_json() for b in blogs]


class Blog(BaseResource):

    def get(self, id):
        blog = BlogModel.query.get(id)
        return blog.to_json()


class Articles(BaseResource):

    def get(self):
        articles = []
        return articles


class Article(BaseResource):

    def get(self, _id):
        fname = 'python-stdout-buffer.html'
        fname = 'betonether.html'
        path = url_for('static', filename='blogs/{}'.format(fname))

        return {
            'image': 'http://ac-hcebow9l.clouddn.com/a72529f44be3cdb0d620.jpeg',
            'title': 'Python std buffer problem.',
            'tags': ['ethereum', '智能合约', 'web3'],
            'summary': 'Some log issue while using "print()"',
            'html': path,
            'type': 'markdown',
        }
