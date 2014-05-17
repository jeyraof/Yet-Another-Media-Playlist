# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, session

view = Blueprint('main', __name__)


def apply_view(app):
    app.register_blueprint(view)


@view.route('/')
def index():
    return render_template('main/index.html', user_id=session.get('id_int'))