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
#     * Neither the project name nor the names of the contributors may be 
#       used to endorse or promote products derived from this software 
#       without specific prior written permission.
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
This module provides a JSON writer.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
from __future__ import absolute_import
try:
    import simplejson as json
except ImportError:
    try:
        import json
    except ImportError:
        try:
            # Google Appengine offers simplejson via django
            from django.utils import simplejson as json
        except ImportError:
            raise ImportError('Cannot find a JSON module')

load = json.load
loads = json.loads

# Try to import some (json|simplejson) specific stuff. 
# If json or simplejson is available the JSONWriter may operate faster 
# (at least if the C version of the encoder is available)
#pylint: disable-msg=E0102
found = False
try:
    #pylint: disable-msg=E0611, F0401
    from json.encoder import encode_basestring_ascii as escape
    found = True
except ImportError:
    pass
if not found:
    # Code from simplejson.encoder Copyright (c) Bob Ippolito
    # License: MIT
    # http://undefined.org/python/#simplejson
    import re
    ESCAPE = re.compile(r'[\x00-\x1f\\"\b\f\n\r\t]')
    ESCAPE_ASCII = re.compile(r'([\\"]|[^\ -~])')
    HAS_UTF8 = re.compile(r'[\x80-\xff]')
    ESCAPE_DCT = {
        '\\': '\\\\',
        '"': '\\"',
        '\b': '\\b',
        '\f': '\\f',
        '\n': '\\n',
        '\r': '\\r',
        '\t': '\\t',
        }
    for i in range(0x20):
        #ESCAPE_DCT.setdefault(chr(i), '\\u{0:04x}'.format(i))
        ESCAPE_DCT.setdefault(chr(i), '\\u%04x' % (i,))
    def escape(s):
        """\
        Return an ASCII-only JSON representation of a Python string
        """
        if isinstance(s, str) and HAS_UTF8.search(s) is not None:
            s = s.decode('utf-8')
        def replace(match):
            s = match.group(0)
            try:
                return ESCAPE_DCT[s]
            except KeyError:
                n = ord(s)
                if n < 0x10000:
                    #return '\\u{0:04x}'.format(n)
                    return '\\u%04x' % (n,)
                else:
                    # surrogate pair
                    n -= 0x10000
                    s1 = 0xd800 | ((n >> 10) & 0x3ff)
                    s2 = 0xdc00 | (n & 0x3ff)
                    #return '\\u{0:04x}\\u{1:04x}'.format(s1, s2)
                    return '\\u%04x\\u%04x' % (s1, s2)
        return '"' + str(ESCAPE_ASCII.sub(replace, s)) + '"'

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
        self._out = out
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
        self._depth+=1
        self._want_comma = False

    def end_object(self):
        """\
        Indicates the end of an object.
        """
        self._out.write(u'}')
        self._depth-=1
        self._want_comma = True

    def start_array(self):
        """\
        Indicates the start of an array.
        """
        self._out.write(u'[')
        self._depth+=1
        self._want_comma = False

    def end_array(self):
        """\
        Indicates the end of an array.
        """
        self._out.write(u']')
        self._depth-=1
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
                write('[')
                written = True
            else:
                write(',')
            write(escape(e))
        if written:
            write(']')
        self._want_comma = written or self._want_comma

    def _indent(self):
        """\
        Indents a line.
        """
        if self.prettify:
            if self._depth:
                self._out.write(u'\n')
            self._out.write(u' ' * self._depth * 2)
