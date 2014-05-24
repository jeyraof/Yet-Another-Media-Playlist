# -*- coding: utf-8 -*-

from hashlib import md5
from flask import session, g
from yamp.controllers import BaseController
from yamp.helpers.oauth import GoogleAPI
from yamp.app import db
from yamp.models.user import User
from yamp.models.playlist import Playlist
from yamp.models.newsfeed import NewsFeed


class UserController(BaseController):
    """
    User Controller
    """
    @classmethod
    def login(cls, user_info, password=u''):
        if isinstance(user_info, User):
            # user_info 가 User 객체인경우
            session['id_str'] = user_info.id_str
            session['id_int'] = user_info.id_int
            return True

        elif isinstance(user_info, basestring):
            # user_info 가 id_str 혹은 email 인 경우
            # 만들일이 있을지 모르겠음..
            pass

        return False

    @classmethod
    def is_login(cls):
        return g.user or None

    @classmethod
    def logout(cls):
        session.clear()
        return

    @classmethod
    def register_google(cls, response):
        access_token = response.get(u'access_token', None)
        if not access_token:
            return {u'ok': False, u'msg': u'Google 로그인에 실패했습니다.'}

        r = GoogleAPI(access_token=access_token).fetch()

        if r.status != 200:
            return {u'ok': False, u'msg': u'개인 정보를 불러오는 데 실패했습니다.'}

        data = r.data
        user_email = data.get('email')
        user_data = db.query(User).filter_by(email=user_email).first()
        if user_data:
            return {u'ok': True, u'user': user_data, u'created': False}

        user_id = user_email.split('@')[0]
        user_pw = md5('%s%s%s' % ('go', user_id, 'google')).hexdigest()[:20]
        user_pic = data.get('picture')

        created_user = User(id_str=user_email.split('@')[0],
                            email=user_email,
                            password=user_pw,
                            picture=user_pic)

        created_feed = NewsFeed(news_type=(3,),
                                data={
                                    u'user': {
                                        u'picture': user_pic,
                                        u'id_int': created_user.id_int,
                                        u'id_str': user_id,
                                    }
                                })
        db.add(created_user, created_feed)
        db.commit()

        return {u'ok': True, u'user': created_user, u'created': True}

    @classmethod
    def get_archived_playlist(cls, **kwargs):
        playlist = db.query(Playlist)
        user = kwargs.get('user', g.user)
        if isinstance(user, User):
            playlist = playlist.filter_by(owner=user.id_int)
        elif isinstance(user, int):
            playlist = playlist.filter_by(owner=user)

        playlist = playlist.order_by('created_at').first()
        return playlist

    @classmethod
    def get_archived_media(cls, **kwargs):
        """
        Parameters:
        page: page number (integer, default=1)
        """
        user = kwargs.get('user', g.user)
        if user:
            playlist = cls.get_archived_playlist(user=user)
        else:
            playlist = cls.get_archived_playlist()

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