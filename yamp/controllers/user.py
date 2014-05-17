# -*- coding: utf-8 -*-

from hashlib import md5
from flask import session
from yamp.controllers import BaseController
from yamp.helpers.oauth import GoogleAPI
from yamp.app import db
from yamp.models.user import User


class UserController(BaseController):
    u"""
    User Controller
    """
    @classmethod
    def login(cls, user_info, password=u''):
        if isinstance(user_info, User):
            # user_info 가 User 객체인경우
            session['id_str'] = user_info.id_str
            session.permanent = False
            return True

        elif isinstance(user_info, basestring):
            # user_info 가 id_str 혹은 email 인 경우
            # 만들일이 있을지 모르겠음..
            pass

        return False

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
        db.add(created_user)
        db.commit()

        return {u'ok': True, u'user': created_user, u'created': True}