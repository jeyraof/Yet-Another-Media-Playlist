# -*- coding: utf-8 -*-

from sqlalchemy.sql.expression import func
from sqlalchemy import Column, types
from yayp.models import Base


class User(Base):
    __tablename__ = u'yayp_user'

    id_int = Column('id_int', types.Integer, nullable=False, primary_key=True, autoincrement=True)
    id_str = Column('id_str', types.Unicode(255), nullable=False, default=u'', index=True)
    email = Column('email', types.Unicode(255), nullable=False, default=u'', index=True)
    password = Column('password', types.Unicode(255), nullable=False, default=u'')

    registered_at = Column('mb_datetime', types.DateTime, nullable=False, default=func.now(), index=True)