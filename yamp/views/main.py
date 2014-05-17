# -*- coding: utf-8 -*-

from flask import Blueprint

view = Blueprint('main', __name__)


def apply_view(app):
    app.register_blueprint(view)


@view.route('/')
def index():
    return 'hello world!'