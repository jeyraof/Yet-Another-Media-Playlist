# -*- coding: utf-8 -*-

from sqlalchemy.sql.expression import func
from sqlalchemy import Column, types
from yamp.models import Base


class User(Base):
    __tablename__ = u'user'

    id_int = Column('id_int', types.Integer, nullable=False, primary_key=True, autoincrement=True)
    id_str = Column('id_str', types.Unicode(255), nullable=False, default=u'', index=True)
    email = Column('email', types.Unicode(255), nullable=False, default=u'', unique=True, index=True)
    password = Column('password', types.Unicode(255), nullable=False, default=u'')
    picture = Column('picture', types.Unicode(255), nullable=True, default=u'')

    active = Column('active', types.Boolean, default=False)

    joined_at = Column('joined_at', types.DateTime, nullable=False, default=func.now(), index=True)

    @property
    def is_active(self):
        if self.active:
            return True
        return False