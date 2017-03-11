django-contextaware_processors
================================

:author: Keryn Knight
:version: 0.1.0

.. |travis_stable| image:: https://travis-ci.org/kezabelle/django-contextaware-processors.svg?branch=0.1.0
  :target: https://travis-ci.org/kezabelle/django-contextaware-processors

.. |travis_master| image:: https://travis-ci.org/kezabelle/django-contextaware-processors.svg?branch=master
  :target: https://travis-ci.org/kezabelle/django-contextaware-processors

==============  ======
Release         Status
==============  ======
stable (0.1.0)  |travis_stable|
master          |travis_master|
==============  ======

.. contents:: Sections
   :depth: 2

What it does
------------

Ever used `Django`_ and wished you could have a `context processor`_ which
received the existing context, along with the request, so that it could do
different things depending on the values the view provided? This does that.

Installation & Usage
--------------------

Installation
^^^^^^^^^^^^

Usage
^^^^^

Add a new ``CONTEXTAWARE_PROCESSORS`` setting to your project configuration. It
should be an iterable of strings representing the dotted paths to your
processors, just the same as the `Django`_ context processors are configured::

    CONTEXTAWARE_PROCESSORS = ('path.to.my_processor', 'another_processor.lives.here')

Processors are executed in the order in which they are declared, and update the
original context data. The new context is given to subsequent processors, such
that the last processor above (``another_processor.lives.here``) will see any
changes made by ``path.to.my_processor``.

Using the middleware
********************

In most cases, if you're using ``TemplateResponse`` objects (or any `Class
Based View`_ which uses them for you), you want to use the provided
middleware::

    MIDDLEWARE_CLASSES = (
        # ...
        'contextaware_processors.middleware.ContextawareProcessors',
        # ...
    )

As this makes use of ``process_response(request, response)`` you probably want
it somewhere near the bottom, so that it modifies the context on the way out
as soon as possible. The middleware will automatically apply any processors
defined in ``CONTEXTAWARE_PROCESSORS``

Using the TemplateResponse subclass
***********************************

For custom situations, there is
``context_processors.response.ContextawareTemplateResponse`` class which
exposes an ``add_context_callback(callback_function)`` which can be used to
apply view-specific context modifiers, though why you'd need to is not
immeidiately obvious to me ;)
If the ``ContextawareProcessors`` middleware notices a ``ContextawareTemplateResponse`` it
will add those defined in ``CONTEXTAWARE_PROCESSORS`` *after* any previously
registered custom modifiers.


Writing a context-aware processor
*********************************

The API contract for a processor is the same as a normal context processor, but
with the addition of a ``context`` parameter, sent as a *named-kwarg*.

A normal context processor looks like::

    def my_processor(request):
        return {'MY_VALUE': 1}

While a context-aware processor looks like::
    def my_processor(request, context):
        if 'MY_KEY' in context:
            return {'MY_VALUE': 2}
        return {'MY_VALUE': None}

Return values
"""""""""""""

A context-aware processor must return one of 3 things:
- A ``dictionary`` to ``.update(...)`` the existing context with,
- ``NotImplemented`` may be used to mark it as irrelevant for the request
- For convienience, ``None`` may also be used to skip updating the context.

The license
-----------

It's the `FreeBSD`_. There's should be a ``LICENSE`` file in the root of the repository, and in any archives.

.. _FreeBSD: http://en.wikipedia.org/wiki/BSD_licenses#2-clause_license_.28.22Simplified_BSD_License.22_or_.22FreeBSD_License.22.29
