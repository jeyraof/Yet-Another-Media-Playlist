# -*- coding: utf-8 -*-

from flask import Blueprint, url_for, session, flash, redirect, render_template, request
from yamp.controllers.playlist import PlaylistController
from yamp.helpers.user import login_required

view = Blueprint('playlist', __name__, url_prefix='/playlist')


def apply_view(app):
    app.register_blueprint(view)