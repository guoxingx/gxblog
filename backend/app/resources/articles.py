#!coding: utf-8

from flask import url_for

from .base import BaseResource


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
