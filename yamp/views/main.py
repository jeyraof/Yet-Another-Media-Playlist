# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, session, g

view = Blueprint('main', __name__)


def apply_view(app):
    app.register_blueprint(view)


@view.route('/')
def index():
    opt = {
        'user': g.user,
    }
    return render_template('main/index.html', **opt)