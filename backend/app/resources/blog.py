#!coding: utf-8

from flask import abort

from .base import BaseResource
from ..models import Blog as BlogModel


class Blogs(BaseResource):

    def get(self):
        blogs = BlogModel.query.order_by(BlogModel.created_at.desc()).all()
        return [b.to_json() for b in blogs]


class Blog(BaseResource):

    def get(self, id):
        blog = BlogModel.query.get(id)
        if not blog:
            abort(404)
        return blog.to_json()
