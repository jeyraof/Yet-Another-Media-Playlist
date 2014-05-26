# -*- coding: utf-8 -*-
from flask import session, g
from importlib import import_module
from datetime import datetime
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
    #db.commit()

    if 'id_int' in session:
        g.user = db.query(User).get(session['id_int'])


# Context processor
@app.context_processor
def context_processor():
    return {
        'user': g.user,
        'archived_playlist': UserController.get_archived_playlist(),
        'playlist_number': PlaylistController.get_playlist_number(),
        'today': datetime.now().replace(microsecond=0),
    }

@app.teardown_request
def cleanup_db_session(exc=None):
    _exc = exc
    db.remove()

# Custom filters
@app.template_filter()
def int_with_comma(n):
    return format(n, ',d')


@app.template_filter()
def pretty_duration(sec):
    try:
        sec = int(sec)
        result = ''

        days = sec / 86400
        sec -= 86400*days
        if days > 0:
            result += ' %sday' % days

        hrs = sec / 3600
        sec -= 3600*hrs
        if hrs > 0:
            result += ' %shr' % hrs

        mins = sec / 60
        sec -= 60*mins
        if mins > 0:
            result += ' %smin' % mins

        if sec > 0:
            result += ' %ssec' % sec

        return result.strip()
    except:
        return '0'
