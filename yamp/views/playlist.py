# -*- coding: utf-8 -*-

from flask import Blueprint, url_for, session, flash, redirect, render_template, request
from yamp.controllers.playlist import PlaylistController
from yamp.helpers.user import login_required

view = Blueprint('playlist', __name__, url_prefix='/playlist')


def apply_view(app):
    app.register_blueprint(view)


@view.route('/<id_int>')
def media_list(id_int):
    playlist = PlaylistController.get_playlist_by_id_int(id_int)
    all_media = playlist.media_list

    opt = {
        'playlist': playlist,
        'media_list': all_media,
    }

    return render_template('playlist/medialist.html', **opt)