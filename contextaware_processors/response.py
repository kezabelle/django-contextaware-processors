# -*- coding: utf-8 -*-
from __future__ import absolute_import, unicode_literals

from django.template.response import TemplateResponse


__all__ = ['AlreadyRendered', 'ContextawareTemplateResponse']


class AlreadyRendered(TypeError): pass


class ContextawareTemplateResponse(TemplateResponse):
    rendering_attrs = TemplateResponse.rendering_attrs + ['_post_context_callbacks']

    def __init__(self, request, template, context=None, content_type=None,
                 status=None, charset=None, using=None):
        super(ContextawareTemplateResponse, self).__init__(
            request, template, context=context, content_type=content_type,
            status=status, charset=charset, using=using)
        self._post_context_callbacks = []

    def add_context_callback(self, callback):
        if self._is_rendered:
            raise AlreadyRendered("Cannot apply a new context-mutating "
                                  "callback after rendering the content, "
                                  "without having to re-render it")
        self._post_context_callbacks.append(callback)

    def resolve_context(self, context):
        retval = super(ContextawareTemplateResponse, self).resolve_context(context=context)
        for context_callback in self._post_context_callbacks:
            newretval = context_callback(request=self._request, context=retval)
            # if a callback marks itself as irrelevant, skip to the
            # next processor in the list.
            if newretval is NotImplemented:
                continue
            if newretval is not None:
                retval.update(newretval)
        return retval
