# -*- coding: utf-8 -*-

import os.path
from flask import Flask
from sqlalchemy import create_engine, event
from sqlalchemy.orm import scoped_session, sessionmaker
from raven.contrib.flask import Sentry

path = os.path.dirname(__file__)
app = Flask(__name__)
app.config.from_pyfile(os.path.join(path, '..', 'config.cfg'))
app.secret_key = app.config.get('SECRET_KEY')

if 'SENTRY_DSN' in app.config:
    sentry = Sentry(app)

engine = create_engine(app.config.get('DB_URI'))
maker = sessionmaker(autocommit=False, autoflush=False, bind=engine)
db = scoped_session(maker)


@event.listens_for(engine, 'connect')
def database_connect(connection, record):
    connection.query("SET time_zone = 'Asia/Seoul';")
    # 서버 시간대를 한국으로 맞춘다. 이런 고귀한 사용법이 있을줄이야..
