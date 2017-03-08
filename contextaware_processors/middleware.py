# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:  # < Django 1.10
    class MiddlewareMixin(object):
        pass


__all__ = ['ContextawareProcessors']

class ContextawareProcessors(MiddlewareMixin):
    def process_response(self, request, response):
        # TODO; if its got rendering_attrs and _request, load contextaware & apply.
        return response
