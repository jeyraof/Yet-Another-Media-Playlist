# -*- coding: utf-8 -*-

from flask import g
from yamp.controllers import BaseController
from yamp.controllers.newsfeed import NewsFeedController
from yamp.app import db
from yamp.models.playlist import Playlist
from yamp.models.media import Media
from yamp.models.user import User


class PlaylistController(BaseController):
    """
    Playlist Controller
    """

    @classmethod
    def create(cls, **kwargs):
        """
        Parameters:
        user: owner of playlist (default: connected_user)
        title: title of playlist (default: None, *required)
        limit: embargo of media in playlist (default: 20)
        """
        user = kwargs.get('user', g.user)
        if not user:
            return {u'ok': False, u'msg': u'Need to sign in.'}

        title = kwargs.get('title', None)
        if not title:
            return {u'ok': False, u'msg': u'title was required'}

        limit = kwargs.get('limit', 20)
        default = kwargs.get('default', False)

        created_playlist = Playlist(title=title, owner=user, limit=limit, default=default)
        db.add(created_playlist)
        db.commit()

        return {u'ok': True, u'playlist': created_playlist}

    @classmethod
    def create_default_playlist(cls, **kwargs):
        """
        Parameters:
        user: owner of playlist (default: connected_user)
        """
        user = kwargs.get('user', g.user)
        params = {
            'user': user,
            'title': u'%s\'s Archived Media' % user.id_str,
            'default': True,
            'limmit': 0,
        }

        return cls.create(**params)

    @classmethod
    def get_playlist_by_id_int(cls, id_int):
        playlist = db.query(Playlist).filter_by(id_int=id_int).first()
        return playlist

    @classmethod
    def get_playlist_number(cls, **kwargs):
        """
        Parameters:
        user: owner of playlist
        """

        playlist = db.query(Playlist)
        user = kwargs.get('user', g.user)
        if isinstance(user, User):
            playlist = playlist.filter_by(owner=user.id_int)
        elif isinstance(user, int):
            playlist = playlist.filter_by(owner=user)

        return playlist.count() or 0

    @classmethod
    def add_media(cls, playlist, media):
        if isinstance(playlist, int):
            playlist = db.query(Playlist).get(playlist)

        if isinstance(media, int):
            media = db.query(Media).get(media)

        if None in [playlist, media]:
            return False

        playlist.media_list.append(media)
        db.add(playlist)
        db.commit()

        NewsFeedController.create(news_type=1 if playlist.default else 2,
                                  media=media,
                                  playlist=playlist)

        return True