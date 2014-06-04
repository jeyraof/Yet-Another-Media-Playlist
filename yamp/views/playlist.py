# -*- coding: utf-8 -*-

from flask import Blueprint, render_template, request, jsonify
from yamp.controllers.playlist import PlaylistController

view = Blueprint('playlist', __name__, url_prefix='/playlist')


def apply_view(app):
    app.register_blueprint(view)


@view.route('/<id_int>')
def media_list(id_int):
    playlist = PlaylistController.get_playlist_by_id_int(id_int)
    all_media = playlist.media_list

    res_type = request.args.get('v', None)
    if res_type == 'json':
        tmp_list = []
        for media in all_media:
            tmp_list.append({
                'media_type': media.media_type,
                'title': media.title,
                'duration': media.duration,
                'id_str': media.id_str,
                'url': media.url,
            })

        return jsonify(media_list=tmp_list)

    else:
        opt = {
            'playlist': playlist,
            'media_list': all_media,
        }

        return render_template('playlist/medialist.html', **opt)