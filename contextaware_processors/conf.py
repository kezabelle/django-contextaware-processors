# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

__all__ = ['CallbackRegistry', 'callback_registry']

class CallbackRegistry(object):
    __slots__ = ('callbacks', 'callback_paths')
    def __init__(self, defaults=None):
        if defaults is None:
            defaults = settings.CONTEXTAWARE_PROCESSORS
        self.callbacks = []
        self.callback_paths = []
        for default in defaults:
            self.register(default)

    def register(self, callback):
        if callback in self.callback_paths:
            raise ValueEror("")
        self.callback_paths.append(callback)
        _callback = import_string(callback)
        self.callbacks.append(_callback)

    def __iter__(self):
        return iter(self.callbacks)

callback_registry = CallbackRegistry()
