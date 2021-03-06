# -*- coding: utf-8 -*-

from sqlalchemy import Column, types
from yamp.models import Base, IntegerChoiceType, JSONEncodedDict


class Media(Base):
    __tablename__ = u'media'

    id_int = Column('id_int', types.Integer, nullable=False, primary_key=True, autoincrement=True)
    id_str = Column('id_str', types.Unicode(255), nullable=False, default=u'', index=True)
    media_type = Column('media_type',
                        IntegerChoiceType(choices=[
                            (1, 'youtube'),
                        ]),
                        nullable=False, default=0, index=True)
    data = Column('data', JSONEncodedDict, nullable=True, default=u'')

    @property
    def duration(self):
        return self.data.get(u'duration', 0)

    @property
    def title(self):
        return self.data.get(u'title', u'Nof found')

    @property
    def thumbnail(self):
        return self.data.get(u'thumbnail', None)

    @property
    def url(self):
        if self.media_type == 'youtube':
            return u'http://www.youtube.com/watch?v=%s' % self.id_str

        return u''