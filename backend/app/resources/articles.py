#!coding: utf-8

from flask import url_for

from .base import BaseResource


class Articles(BaseResource):

    def get(self):
        articles = []
        return articles


class Article(BaseResource):

    def get(self, _id):
        return None
        if not _id == 17261:
            return None
        fname = 'python-stdout-buffer.html'
        path = url_for('static', filename='blogs/{}'.format(fname))

        return {
            'image': 'http://ac-hcebow9l.clouddn.com/a72529f44be3cdb0d620.jpeg',
            'title': 'Python std buffer problem.',
            'tags': ['Python', '日志'],
            'summary': 'Some log issue while using "print()"',
            'html': path,
            'type': 'markdown',
        }
