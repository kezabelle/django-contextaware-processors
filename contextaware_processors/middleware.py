# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals
try:
    from django.utils.deprecation import MiddlewareMixin
except ImportError:  # < Django 1.10
    class MiddlewareMixin(object):
        pass
from .conf import callback_registry


__all__ = ['ContextawareProcessors']


class ContextawareProcessors(MiddlewareMixin):
    def process_response(self, request, response):
        # Let ContextawareTemplateResponse handle adding and applying them,
        # if its being used.
        if hasattr(response, 'add_context_callback'):
            for callback in callback_registry:
                response.add_context_callback(callback)
        elif hasattr(response, 'rendering_attrs') and hasattr(response, '_request') and response.is_rendered is False:
            context_data = response.context_data
            new_context_data = update_context_from_callbacks(request=response._request, context=context_data,
                                                             callbacks=callback_registry)
            response.context_data = new_context_data
        elif hasattr(response, 'rendering_attrs') and getattr(response, 'request', None) is not None and hasattr(response, 'renderer_context') and response.is_rendered is False:
            context_data = response.renderer_context
            new_context_data = update_context_from_callbacks(request=response.request, context=context_data,
                                                             callbacks=callback_registry)
            response.renderer_context = new_context_data
        return response
