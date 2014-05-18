# -*- coding: utf-8 -*-
from flask import session, g
from importlib import import_module
from yamp import views
from yamp.app import app, db
from yamp.models.user import User


for view_name in views.__all__:
    import_module('.views.' + view_name, package=__name__).apply_view(app)


@app.before_request
def before_request():
    session.permanent = True
    g.user = None

    if 'id_int' in session:
        g.user = db.query(User).get(session['id_int'])


@app.context_processor
def context_processor():
    return {
        'user': g.user,
    }