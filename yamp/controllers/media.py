# -*- coding: utf-8 -*-

from yamp.controllers import BaseController
from yamp.app import db
from yamp.models.media import Media
from urlparse import urlparse
from urllib2 import urlopen
import json


class MediaController(BaseController):
    u"""
    Media Controller
    """
    @classmethod
    def get_by_id_str(cls, id_str):
        media = None
        if isinstance(id_str, tuple):
            media = db.query(Media).filter_by(id_str=id_str[1]).first()
        elif isinstance(id_str, basestring):
            media = db.query(Media).filter_by(id_str=id_str).first()
        return media

    @classmethod
    def create(cls, media_info):
        """
        Parameters:
        media_info: tuple like this (<int>media_type, <str>id_str)
        """
        created_media = None
        parsed_data = cls.route_parser(media_info)
        if parsed_data.get(u'ok'):
            info = parsed_data.get(u'info')
            created_media = Media(id_str=media_info[1],
                                  media_type=media_info,
                                  data=info)
            db.add(created_media)
            db.commit()

        return created_media

    @classmethod
    def get_or_create(cls, media_tuple):
        """
        return media, created_flag
        """
        if media_tuple[0] == 0:
            return None, False

        created_flag = False

        media = cls.get_by_id_str(media_tuple)
        if not media:
            media = cls.create(media_info=media_tuple)
            if media:
                created_flag = True

        return media, created_flag

    @classmethod
    def inspect_url(cls, form_data):
        address = form_data.get('address', u'').strip()

        media_type = 0
        id_str = u''

        if 'youtube.com' in address:
            media_type = 1
            media_query = urlparse(url=address).query

            for media_query_once in media_query.split(u'&'):
                [media_query_key, media_query_val] = media_query_once.split(u'=')
                if media_query_key == u'v':
                    id_str = media_query_val
                    break

        return media_type, id_str

    @classmethod
    def route_parser(cls, media_tuple):
        if media_tuple[0] == 1:
            return cls.youtube_parser(media_tuple[1])

        return {u'ok': False}

    @classmethod
    def youtube_parser(cls, id_str):
        url = "http://gdata.youtube.com/feeds/api/videos/%s?v=2&alt=jsonc" % id_str
        r = urlopen(url)
        json_data = json.loads(r.read())

        if 'error' in json_data:
            return {u'ok': False}

        data = json_data.get('data')

        thumbnail = data.get('thumbnail')
        thumb_str = u'http://i1.ytimg.com/vi/%s/' % id_str
        if 'hqDefault' in thumbnail:
            thumb_str += u'hqdefault.jpg'
        else:
            thumb_str += u'default.jpg'

        param = {
            u'duration': data.get('duration'),
            u'title': data.get('title'),
            u'thumbnail': thumb_str,
        }

        return {u'ok': True, u'info': param}