# -*- coding: utf-8 -*-

from yamp.controllers import BaseController
from yamp.app import db
from yamp.models.newsfeed import NewsFeed
from flask import g
import json


class NewsFeedController(BaseController):
    """
    NewsFeed Controller
    """
    @classmethod
    def create(cls, **kwargs):
        """
        Parameters:
        news_type: type of news
                    * 1: archive
                    * 2: add media to playlist

        user: user object (models.User)
        media: media object (models.Media)
        playlist: playlist object (models.Playlist)
        """
        news_type = kwargs.get(u'news_type', 0)

        user = kwargs.get(u'user', g.user)
        if not user:
            return {u'ok': False, u'msg': u'login required.'}

        media = kwargs.get(u'media', None)
        if not media:
            return {u'ok': False, u'msg': u'media was required.'}

        playlist = kwargs.get(u'playlist', None)
        if not playlist:
            return {u'ok': False, u'msg': u'playlist was required.'}

        param = {
            u'user': {
                u'id_int': user.id_int,
                u'id_str': user.id_str,
            },
            u'media': {
                u'id_int': media.id_int,
                u'title': media.title,
                u'duration': media.duration,
                u'thumbnail': media.thumbnail,
            },
            u'playlist': {
                u'id_int': playlist.id_int,
                u'title': playlist.title,
            },
        }

        created_news_feed = NewsFeed(media_type=(news_type, ),
                                     data=param)
        db.add(created_news_feed)
        db.commit()

        return {u'ok': True}