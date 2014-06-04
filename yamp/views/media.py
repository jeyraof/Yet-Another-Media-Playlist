# -*- coding: utf-8 -*-

from flask import Blueprint, url_for, g, session, flash, redirect, render_template, request
from yamp.controllers.user import UserController
from yamp.controllers.media import MediaController
from yamp.controllers.playlist import PlaylistController
from yamp.helpers.user import disable_if_not_active

view = Blueprint('media', __name__, url_prefix='/media')


def apply_view(app):
    app.register_blueprint(view)


@view.route('/')
def media():
    return redirect(url_for('main.index'))


@view.route('/archive', methods=['GET', 'POST'])
@disable_if_not_active
def archive():
    if request.method == 'GET':
        opt = {
            'bookmarklet_address': url_for('media.bookmarklet', _external=True),
        }
        return render_template("media/archive.html", **opt)

    else:
        inspected_data = MediaController.inspect_url(request.form)
        created_media, created_flag = MediaController.get_or_create(inspected_data)

        playlist = UserController.get_archived_playlist()
        success = PlaylistController.add_media(playlist=playlist, media=created_media)
        if not success:
            flash(u'failed to archive')

        return redirect(url_for('user.archived'))


@view.route('/archive/bookmarklet', methods=['GET', 'POST'])
def bookmarklet():
    opt = {
        'is_login': False,
        'is_active': False,
        'done': False,
    }

    if g.user:
        opt['is_login'] = True

        if g.user.active:
            opt['is_active'] = True

    if request.method == 'GET':
        opt['address'] = request.args.get('url', '')

        media_tuple = MediaController.inspect_url(form_data=opt)
        opt['result'] = MediaController.route_parser(media_tuple=media_tuple)

    elif request.method == 'POST':
        inspected_data = MediaController.inspect_url(request.form)
        created_media, created_flag = MediaController.get_or_create(inspected_data)

        playlist = UserController.get_archived_playlist()
        success = PlaylistController.add_media(playlist=playlist, media=created_media)
        if success:
            opt['done'] = True
        else:
            opt['fail'] = True

    return render_template("media/bookmarklet.html", **opt)