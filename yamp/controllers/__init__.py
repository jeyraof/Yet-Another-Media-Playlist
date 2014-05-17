# -*- coding: utf-8 -*-


class BaseController(object):
    def __init__(self, obj=None):
        self.obj = obj


def register_controller(model_cls, controller_cls):
    model_cls.controller = controller_cls
    controller_cls.model = model_cls