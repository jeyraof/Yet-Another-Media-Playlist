# -*- coding: utf-8 -*-

from flask import Blueprint, url_for, session, flash, redirect, render_template, request
from yamp.controllers.newsfeed import NewsFeedController
from yamp.helpers.user import login_required

view = Blueprint('newsfeed', __name__, url_prefix='/newsfeed')


def apply_view(app):
    app.register_blueprint(view)


@view.route('/')
def get_newsfeed():
    id_int = request.args.get('id_int', None)
    age = request.args.get('age', 'new')

    news_feed_list = NewsFeedController.get_newsfeed(id_int=id_int, age=age)

    return render_template('newsfeed/newsfeed.html',
                           news_feed_list=news_feed_list)