# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
This module tries to provide definitions of `Zope Interfaces`_.
If the package is not available, this module provides dummy implementations.

.. _Zope Interfaces: http://www.python.org/pypi/zope.interface
   

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD License
"""
from __future__ import absolute_import
try:
    from zope.interface import Interface, Attribute, implements
except ImportError:
    class Interface(object): 
        def __call__(self, default=None):
            return default
    class Attribute(object):
        def __init__(self, descr): pass
    def implements(i): pass
try:
    from zope.component import adapts
except ImportError:
    def adapts(i): pass
