# -*- coding: utf-8 -*-

from hashlib import md5
from flask import session, g
from yamp.controllers import BaseController
from yamp.helpers.oauth import GoogleAPI
from yamp.app import db
from yamp.models.playlist import Playlist
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

        created_playlist = Playlist(title=title, owner=user, limit=limit)
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
            'limmit': 0,
        }

        return cls.create(**params)

    @classmethod
    def get_archived_media(cls, **kwargs):
        """
        Parameters:
        user: owner of playlist
        page: page number (integer, default=1)
        """
        playlist = db.query(Playlist)

        user = kwargs.get('user', g.user)
        if isinstance(user, User):
            playlist = playlist.filter_by(owner=user.id_int)
        elif isinstance(user, int):
            playlist = playlist.filter_by(owner=user)

        playlist = playlist.order_by('created_at').first()

        media_ea = 20
        page = kwargs.get('page', 1)
        media_f = -1 * media_ea * page
        media_t = media_f + media_ea

        media_list = []
        if playlist:
            if media_t == 0:
                media_list = playlist.media_list[media_f:]
            else:
                media_list = playlist.media_list[media_f:media_t]

        media_list.reverse()
        return media_list

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
        if None in [playlist, media]:
            return False

        playlist.media_list.append(media)
        db.add(playlist)
        db.commit()

        return True