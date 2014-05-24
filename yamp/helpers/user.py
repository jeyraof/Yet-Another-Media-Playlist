# -*- coding: utf-8 -*-

from functools import wraps
from flask import g, redirect, url_for, flash


def login_required(f):
    @wraps(f)
    def return_func(*args, **kwargs):
        if g.user:
            return f(*args, **kwargs)

        flash(u'로그인 후 이용하실 수 있습니다.')
        return redirect(url_for('main.index'))
    return return_func


def disable_if_not_active(f):
    @wraps(f)
    def return_func(*args, **kwargs):
        if g.user and g.user.active:
            return f(*args, **kwargs)

        return 'login required!'
    return return_func