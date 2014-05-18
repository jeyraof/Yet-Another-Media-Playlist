# -*- coding: utf-8 -*-
from flask import session, g
from importlib import import_module
from yamp import views
from yamp.app import app, db
from yamp.models.user import User
from yamp.controllers.user import UserController
from yamp.controllers.playlist import PlaylistController


# Apply views to app
for view_name in views.__all__:
    import_module('.views.' + view_name, package=__name__).apply_view(app)


# Process of before request
@app.before_request
def before_request():
    session.permanent = True
    g.user = None

    if 'id_int' in session:
        g.user = db.query(User).get(session['id_int'])


# Context processor
@app.context_processor
def context_processor():
    return {
        'user': g.user,
        'archived_playlist': UserController.get_archived_playlist(),
        'playlist_number': PlaylistController.get_playlist_number(),
    }


# Custom filters
@app.template_filter()
def int_with_comma(n):
    return format(n, ',d')