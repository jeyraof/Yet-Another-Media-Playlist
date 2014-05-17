# -*- coding: utf-8 -*-

from flask import Blueprint, url_for, session, flash, redirect, make_response
from yamp.helpers.oauth import google, GOOGLE_TOKEN_NAME
from yamp.controllers.user import UserController

view = Blueprint('user', __name__, url_prefix='/user')


def apply_view(app):
    app.register_blueprint(view)


@view.route('/login')
def login():
    return u'<a href="/user/oauth/google">로그인</a>'


@view.route('/logout', methods=['GET'])
def logout():
    UserController.logout()
    return redirect(url_for('main.index'))


@view.route('/oauth/google')
def oauth_google():
    return google.authorize(callback=url_for(
        'user.google_authorized',
        _external=True,
    ))


@view.route('/oauth/google/authorized')
@google.authorized_handler
def google_authorized(response):
    if not response:
        return u'Failed to login using google OAuth'

    next_url = url_for('main.index')
    session[GOOGLE_TOKEN_NAME] = (response.get('access_token'), '')

    result = UserController.register_google(response)
    if result.get(u'ok', False):
        user = result.get(u'user')

        login_request = UserController.login(user_info=user)
        if login_request:
            if result.get(u'created', False):
                # 새로운 회원으로 가입 되었을때
                flash(u'%s, 가입을 진심으로 환영합니다!' % user.id_str)

            else:
                # 기존 회원일때
                flash(u'%s, 재방문을 진심으로 환영합니다!' % user.id_str)
        else:
            flash(u'로그인에 실패하였습니다.')

    else:
        # 뭔가 잘못됨.
        flash(result.get(u'msg'))

    return redirect(next_url)