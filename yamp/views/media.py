# -*- coding: utf-8 -*-

from flask import Blueprint, url_for, session, flash, redirect, render_template, request
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
        return render_template("media/archive.html")

    else:
        inspected_data = MediaController.inspect_url(request.form)
        created_media, created_flag = MediaController.get_or_create(inspected_data)

        playlist = UserController.get_archived_playlist()
        success = PlaylistController.add_media(playlist=playlist, media=created_media)
        if not success:
            flash(u'failed to archive')

        return redirect(url_for('user.archived'))