# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2012 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#
#     * Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
#     * Neither the name of the project nor the names of the contributors 
#       may be used to endorse or promote products derived from this 
#       software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
"""\
Module for XSLT stylesheets.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
import os
import glob
from lxml import etree, sax

_PATH = None
_NOT_FOUND = object()
_STYLESHEETS = None

DEFAULT_TRANSFORMERS = ('query-c14n', 
                         'inline-rules', 
                         'annotate-predicates', 
                         'remove-redundant-predicates', 
                         'annotate-costs', 
                         'reorder-predicates') #TODO

def _init():
    global _PATH, _STYLESHEETS
    _PATH = os.path.dirname(__file__)
    _STYLESHEETS = dict((os.path.basename(f)[:-4], None) for f in glob.glob(_PATH + '/*.xsl'))

def _compile(name):
    """\

    """
    return etree.XSLT(etree.parse(open(os.path.join(_PATH, name + '.xsl'))))    

def get_transformator_names():
    """\
    Returns an iterable of available transformator names (which can be
    used to retrieve a transformator via `get_transformator`.
    """
    return _STYLESHEETS.keys()
    
def get_transformator(name):
    """\
    Returns a function to transform an etree.Element
    """
    t = _STYLESHEETS.get(name, _NOT_FOUND)
    if t is _NOT_FOUND:
        raise ValueError('%s is not available' % name)
    elif t is None:
        t = _compile(name)
        _STYLESHEETS[name] = t
    return t


def apply_transformation(doc, name, callback=None, **params):
    """\
    Applies the provided transformer (referenced by name) against the provided 
    `doc` and returns the result unless the `callback` does not return a result.
    
    `doc` 
        An Etree
    `name`
        The transformer to apply.
    `callback`
        An optional function which receives the final result of the 
        transformation.
    """
    res = get_transformator(name)(doc, **params)
    return res if callback is None else callback(res)


def apply_transformations(doc, names, callback=None, **params):
    """\
    Applies a sequence of transformations against the provided `doc` and
    returns the result unless the `callback` does not return a result.
    
    `doc` 
        An Etree
    `names`
        An iterable of transformator names (c.f. `get_transformator_names()`)
        to apply (in the provided order).
    `callback`
        An optional function which receives the final result of the 
        transformations.
    """
    result = doc
    for name in names:
        result = get_transformator(name)(result, **params)
    return result if callback is None else callback(result)


def saxify(doc, handler):
    """\
    Issues SAX events from the provided lxml.etree document.
    
    `doc` 
        An Etree.
    `handler` 
        A xml.sax.ContentHandler instance
    """
    sax.saxify(doc, handler)

_init()
del _init
del glob
del os
