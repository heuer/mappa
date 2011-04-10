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
Tests against the mio.deserializer module.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
from unittest import TestCase
import tm.mio as mio
from tm.mio.handler import MapHandler, simplify
from tm.mio.deserializer import Deserializer
from tm.mio import syntax

_TEST_SYNTAX = syntax.Syntax('Test-Syntax', 'application/something', 'blub')

class _MapHandler(MapHandler):
    pass

class TestDeserializer(TestCase):

    def test_subordinate(self):
        deser = Deserializer()
        self.assertFalse(deser.subordinate)
        deser.subordinate = True
        self.assertTrue(deser.subordinate)

    def test_handler(self):
        deser = Deserializer()
        self.assert_(deser.handler is None)
        handler = simplify(_MapHandler())
        deser.handler = handler
        self.assert_(handler is deser.handler)

    def test_autosimplify(self):
        deser = Deserializer()
        self.assert_(deser.handler is None)
        handler = _MapHandler()
        deser.handler = handler
        self.assertTrue(hasattr(deser.handler, 'ako'))
        self.assert_(deser.handler is simplify(deser.handler))

    def test_create_deserializer_unknown_syntax(self):
        self.assert_(None is mio.create_deserializer(format='xy'))
        self.assert_(None is mio.create_deserializer(mimetype='xy'))
        self.assert_(None is mio.create_deserializer(extension='xy'))

    def test_deserializer_discovery(self):
        deser = mio.create_deserializer(mimetype=syntax.XTM.mimetypes[0])
        self.assert_(deser)
        for ext in syntax.XTM.extensions:
            deser = mio.create_deserializer(extension=ext)
            self.assert_(deser)
            deser = mio.create_deserializer(extension=ext.upper())
            self.assert_(deser)
            deser = mio.create_deserializer(extension='.%s' %ext)
            self.assert_(deser)
            deser = mio.create_deserializer(extension='.%s' % ext.upper())
            self.assert_(deser)

    def test_register_deserializer(self):
        self.assert_(None is mio.create_deserializer(_TEST_SYNTAX))
        self.assert_(None is mio.create_deserializer(format='Test-Syntax'))
        self.assert_(None is mio.create_deserializer(extension=_TEST_SYNTAX.extensions[0]))
        self.assert_(None is mio.create_deserializer(mimetype=_TEST_SYNTAX.mimetypes[0]))
        mio.register_deserializer('mio.xtm', _TEST_SYNTAX)
        self.assert_(mio.create_deserializer(_TEST_SYNTAX))
        self.assert_(mio.create_deserializer(format='Test-Syntax'))
        self.assert_(mio.create_deserializer(extension=_TEST_SYNTAX.extensions[0]))
        self.assert_(mio.create_deserializer(mimetype=_TEST_SYNTAX.mimetypes[0]))


if __name__ == '__main__':
    import nose
    nose.core.runmodule()
