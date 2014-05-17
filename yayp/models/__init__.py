# -*- coding: utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base, declared_attr


class DefaultBase(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__

    __table_args__ = {
        'mysql_charset': 'utf8',
        'mysql_engine': 'InnoDB',
    }

    def __repr__(self):
        return '<%s id=%d>' % (type(self).__name__, self.id)

Base = declarative_base(cls=DefaultBase)

__all__ = [
    'user'
]