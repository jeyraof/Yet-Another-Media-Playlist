# -*- coding: utf-8 -*-
from importlib import import_module
from yamp import views
from yamp.app import app


for view_name in views.__all__:
    import_module('.views.' + view_name, package=__name__).apply_view(app)