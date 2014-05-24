# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request

view = Blueprint('main', __name__)


def apply_view(app):
    app.register_blueprint(view)


@view.route('/')
def index():
    if request.is_xhr:
        _template = 'main/index.ajax.html'
    else:
        _template = 'main/index.html'

    return render_template(_template)