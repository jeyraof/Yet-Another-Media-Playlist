# -*- coding: utf-8 -*-

from sqlalchemy import Column, types, ForeignKey, Table
from sqlalchemy.orm import relationship
from yamp.models import Base, IntegerChoiceType, JSONEncodedDict


playlist_media_association = Table(u'playlist_media_assoc', Base.metadata,
    Column('playlist_id', types.Integer, ForeignKey(u'playlist.id')),
    Column('media_id', types.Integer, ForeignKey(u'media.id_int'))
)


class Playlist(Base):
    __tablename__ = u'playlist'

    id = Column('id', types.Integer, nullable=False, primary_key=True, autoincrement=True)
    title = Column('title', types.Unicode(255), nullable=False, default=u'')
    owner = Column('owner_id', types.Integer, ForeignKey(u'user.id_int'))

    medias = relationship(u'Media',
                          secondary=playlist_media_association,
                          backref=u'playlist_list')


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