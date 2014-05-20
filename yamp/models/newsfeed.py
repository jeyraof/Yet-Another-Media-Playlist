# -*- coding: utf-8 -*-

from sqlalchemy import Column, types
from sqlalchemy.sql.expression import func
from yamp.models import Base, IntegerChoiceType, JSONEncodedDict


class NewsFeed(Base):
    __tablename__ = u'newsfeed'

    id_int = Column('id_int', types.Integer, nullable=False, primary_key=True, autoincrement=True)
    media_type = Column('news_type',
                        IntegerChoiceType(choices=[
                            (1, 'archived'),
                            (2, 'append'),
                        ]),
                        nullable=False, default=0, index=True)
    data = Column('data', JSONEncodedDict, nullable=True, default=u'')

    created_at = Column('created_at', types.DateTime, default=func.now())

    @property
    def user(self):
        return self.data.get(u'user', {u'id_int': 0, u'id_str': u''})

    @property
    def media(self):
        return self.data.get(u'media', {u'id_int': 0, u'title': u''})

    @property
    def playlist(self):
        return self.data.get(u'playlist', {u'id_int': 0, u'title': u''})