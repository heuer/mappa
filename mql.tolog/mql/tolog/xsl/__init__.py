# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2011 -- Lars Heuer - Semagia <http://www.semagia.com/>.
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
from lxml import etree

_PATH = None
_NOT_FOUND = object()
_STYLESHEETS = None

def _init():
    global _PATH, _STYLESHEETS
    _PATH = os.path.split(__file__)[0]
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

_init()

