# -*- coding: utf-8 -*-

from sqlalchemy.ext.declarative import declarative_base, declared_attr
from sqlalchemy.types import TypeDecorator, Integer, UnicodeText
import json

__all__ = [
    'user',
    'media',
]


class DefaultBase(object):
    @declared_attr
    def __tablename__(cls):
        return cls.__name__

    __table_args__ = {
        'mysql_charset': 'utf8',
        'mysql_engine': 'InnoDB',
    }

    def __repr__(self):
        return '<%s id_int=%d>' % (type(self).__name__, self.id_int)

Base = declarative_base(cls=DefaultBase)


class IntegerChoiceType(TypeDecorator):
    impl = Integer

    def __init__(self, choices, **kw):
        self.choices = dict(choices)
        super(IntegerChoiceType, self).__init__(**kw)

    def process_bind_param(self, value, dialect):
        return [k for k, v in self.choices.iteritems() if v == value][0]

    def process_result_value(self, value, dialect):
        return self.choices[value]


class JSONEncodedDict(TypeDecorator):
    impl = UnicodeText

    def process_bind_param(self, value, dialect):
        if value is not None:
            value = json.dumps(value)
        return value

    def process_result_value(self, value, dialect):
        if value is not None:
            value = json.loads(value)
        return value