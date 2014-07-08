# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
This module provides a JSON writer.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
from __future__ import absolute_import
import codecs
try:
    import simplejson as json
except ImportError:
    import json
from json.encoder import encode_basestring_ascii as escape

load = json.load
loads = json.loads


class JSONWriter(object):
    """\
    A JSON writer.
    
    An instance of this class assumes that the caller knows what it is doing,
    it is possible to create an invalid JSON instance if the methods of this
    class are invoked in the wrong order.
    """
    __slots__ = ['_out', '_want_comma', '_depth', 'prettify']

    def __init__(self, out):
        """\
        Initializes the writer with the provided ``out`` file-alike object.
        """
        self._out = codecs.getwriter('utf-8')(out)
        self._want_comma = False
        self._depth = 0
        self.prettify = False

    def start(self):
        """\
        Indicates the start of JSON output.
        """
        self._want_comma = False
        self._depth = 0
    
    def end(self):
        """\
        Indicates the end of the serialization process.
        """
        self._out.write(u'\n')
        self._out.flush()

    def key(self, key):
        """\
        Writes ``"key":``. The `key` is not escaped.
        """
        if self._want_comma:
            self._out.write(u',')
            self._indent()
        self._out.write(u'"%s":' % key)
        self._want_comma = False

    def key_value(self, key, value):
        """\
        Writes ``"key": "value"`` where the `value` is escaped according to
        the JSON rules, but `key` is left untouched.
        """
        self.key(key)
        self.value(value)
    
    def value(self, val):
        """\
        Writes ``"value"`` where `value` is escaped accoring to the JSON rules.
        """
        if self._want_comma:
            self._out.write(u',')
        self._out.write(escape(val))
        self._want_comma = True

    def start_object(self):
        """\
        Indicates the start of an object.
        """
        if self._want_comma:
            self._out.write(u',')
        self._indent()
        self._out.write(u'{')
        self._depth += 1
        self._want_comma = False

    def end_object(self):
        """\
        Indicates the end of an object.
        """
        self._out.write(u'}')
        self._depth -= 1
        self._want_comma = True

    def start_array(self):
        """\
        Indicates the start of an array.
        """
        self._out.write(u'[')
        self._depth += 1
        self._want_comma = False

    def end_array(self):
        """\
        Indicates the end of an array.
        """
        self._out.write(u']')
        self._depth -= 1
        self._want_comma = True

    def array(self, key, iterable):
        """\
        Writes ``"key":["element-0", ... "element-n"]`` iff the `iterable` is
        not empty. If the iterable is empty, this method does nothing. 
        All elements of the ``iterable`` are written in an escaped form while
        the ``key`` is not escaped.
        """
        write = self._out.write
        written = False
        for c, e in enumerate(iterable):
            if not c:
                self.key(key)
                write(u'[')
                written = True
            else:
                write(u',')
            write(escape(e))
        if written:
            write(u']')
        self._want_comma = written or self._want_comma

    def _indent(self):
        """\
        Indents a line.
        """
        if self.prettify:
            if self._depth:
                self._out.write(u'\n')
            self._out.write(u' ' * self._depth * 2)
