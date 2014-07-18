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
from nose.tools import ok_
import tm.mio as mio
from tm.mio.handler import MapHandler, simplify
from tm.mio.deserializer import Deserializer
from tm.mio import syntax

_TEST_SYNTAX = syntax.Syntax('Test-Syntax', 'application/something', 'blub')


class _MapHandler(MapHandler):
    pass


def test_subordinate():
    deser = Deserializer()
    ok_(not deser.subordinate)
    deser.subordinate = True
    ok_(deser.subordinate)


def test_handler():
    deser = Deserializer()
    ok_(deser.handler is None)
    handler = simplify(_MapHandler())
    deser.handler = handler
    ok_(handler is deser.handler)


def test_autosimplify():
    deser = Deserializer()
    ok_(deser.handler is None)
    handler = _MapHandler()
    deser.handler = handler
    ok_(hasattr(deser.handler, 'ako'))
    ok_(deser.handler is simplify(deser.handler))


def test_create_deserializer_unknown_syntax():
    ok_(None is mio.create_deserializer(format='xy'))
    ok_(None is mio.create_deserializer(mimetype='xy'))
    ok_(None is mio.create_deserializer(extension='xy'))


#TODO
# def test_deserializer_discovery():
#     deser = mio.create_deserializer(mimetype=syntax.XTM.mimetypes[0])
#     ok_(deser)
#     for ext in syntax.XTM.extensions:
#         deser = mio.create_deserializer(extension=ext)
#         ok_(deser)
#         deser = mio.create_deserializer(extension=ext.upper())
#         ok_(deser)
#         deser = mio.create_deserializer(extension='.%s' %ext)
#         ok_(deser)
#         deser = mio.create_deserializer(extension='.%s' % ext.upper())
#         ok_(deser)


def test_register_deserializer():
    ok_(None is mio.create_deserializer(_TEST_SYNTAX))
    ok_(None is mio.create_deserializer(format='Test-Syntax'))
    ok_(None is mio.create_deserializer(extension=_TEST_SYNTAX.extensions[0]))
    ok_(None is mio.create_deserializer(mimetype=_TEST_SYNTAX.mimetypes[0]))
    mio.register_deserializer('mio.xtm', _TEST_SYNTAX)
    ok_(mio.create_deserializer(_TEST_SYNTAX))
    ok_(mio.create_deserializer(format='Test-Syntax'))
    ok_(mio.create_deserializer(extension=_TEST_SYNTAX.extensions[0]))
    ok_(mio.create_deserializer(mimetype=_TEST_SYNTAX.mimetypes[0]))


if __name__ == '__main__':
    import nose
    nose.core.runmodule()
