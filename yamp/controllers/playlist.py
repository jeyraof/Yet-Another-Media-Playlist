# -*- coding: utf-8 -*-

from hashlib import md5
from flask import session, g
from yamp.controllers import BaseController
from yamp.helpers.oauth import GoogleAPI
from yamp.app import db
from yamp.models.playlist import Playlist


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