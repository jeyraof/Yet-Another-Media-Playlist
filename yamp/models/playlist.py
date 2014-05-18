# -*- coding: utf-8 -*-

from sqlalchemy import Column, types, ForeignKey, Table
from sqlalchemy.orm import relationship
from yamp.models import Base, IntegerChoiceType, JSONEncodedDict
from yamp.models.media import Media


playlist_media_association = Table(u'playlist_media_assoc', Base.metadata,
    Column('playlist_id', types.Integer, ForeignKey(u'playlist.id_int')),
    Column('media_id', types.Integer, ForeignKey(u'media.id_int'))
)


class Playlist(Base):
    __tablename__ = u'playlist'

    id_int = Column('id_int', types.Integer, nullable=False, primary_key=True, autoincrement=True)
    title = Column('title', types.Unicode(255), nullable=False, default=u'')
    owner = Column('owner_id', types.Integer, ForeignKey(u'user.id_int'))
    limit = Column('limit', types.Integer, default=20)

    medias = relationship(u'Media',
                          secondary=playlist_media_association,
                          backref=u'playlist_list')