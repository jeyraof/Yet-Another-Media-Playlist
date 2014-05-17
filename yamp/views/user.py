# -*- coding: utf-8 -*-

from flask import Blueprint, url_for, request
from yamp.helpers.oauth import google

view = Blueprint('user', __name__, url_prefix='/user')


def apply_view(app):
    app.register_blueprint(view)


@view.route('/login')
def login_html():
    return u'<a href="/user/oauth/google">로그인</a>'


@view.route('/oauth/google')
def oauth_google():
    return google.authorize(callback=url_for(
        'user.google_authorized',
        _external=True,
    ))


@view.route('/oauth/google/authorized')
@google.authorized_handler
def google_authorized(response):
    print response
    return 'Done'