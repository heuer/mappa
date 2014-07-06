# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
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
