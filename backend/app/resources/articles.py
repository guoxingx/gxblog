#!coding: utf-8

from .base import BaseResource


class Articles(BaseResource):

    def get(self):
        articles = [
            {
                'title': 'Python std buffer problem.',
                'summary': 'Some log issue while using "print()"',
                'image': 'http://ac-hcebow9l.clouddn.com/a72529f44be3cdb0d620.jpeg',
                'tags': ['Python', '日志'],
                'id': 17260
            },
            {
                'title': 'World of Warcraft used to be a world, now it\'s a piece of SHIT.',
                'summary': 'And it\'s even getting worse.',
                'image': 'http://ac-hcebow9l.clouddn.com/b841287d9467f01353b7.jpeg',
                'tags': ['游戏', '魔兽世界', '吐槽'],
                'id': 17261
            },
        ]

        return articles


class Article(BaseResource):

    def get(self, _id):
        if not _id == 17261:
            return None
        fname = 'python-stdout-buffer.md'

        with open('static/articles/{}'.format(fname)) as f:
            content = f.read()
        return {
            'image': 'http://ac-hcebow9l.clouddn.com/a72529f44be3cdb0d620.jpeg',
            'title': 'Python std buffer problem.',
            'tags': ['Python', '日志'],
            'summary': 'Some log issue while using "print()"',
            'content': content or 'failed to load info.',
            'type': 'markdown',
        }
