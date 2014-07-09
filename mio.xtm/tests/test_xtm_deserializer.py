# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
Tests against the XTM content handler.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
from nose.tools import ok_
from tm import Source
from tm.mio.handler import MapHandler
from mio.xtm import create_deserializer


fail = AssertionError


def _parse(source):
    deser = create_deserializer()
    deser.handler = MapHandler()
    deser.parse(Source(data=source, iri='http://www.semagia.com/'))
    return deser


def test_illegalstate():
    deser = create_deserializer()
    try:
        deser.version
        fail('The version should not be available yet')
    except AttributeError:
        pass


def test_xtm10():
    deser = create_deserializer(version='1.0')
    ok_('1.0' == deser.version)


def test_xtm20():
    deser = create_deserializer(version='2.0')
    ok_('2.0' == deser.version)


def test_xtm10_detection():
    deser = _parse(u'<topicMap xmlns="http://www.topicmaps.org/xtm/1.0/"></topicMap>')
    ok_('1.0' == deser.version)


def test_xtm10_detection2():
    deser = _parse(u'<topicMap></topicMap>')
    ok_('1.0' == deser.version)


def test_xtm20_detection1():
    deser = _parse(u'<topicMap version="2.0"></topicMap>')
    ok_('2.0' == deser.version)


def test_xtm20_detection2():
    deser = _parse(u'<topicMap xmlns="http://www.topicmaps.org/xtm/" version="2.0"></topicMap>')
    ok_('2.0' == deser.version)


def test_xtm21_detection1():
    deser = _parse(u'<topicMap version="2.1"></topicMap>')
    ok_('2.1' == deser.version)


def test_xtm21_detection2():
    deser = _parse(u'<topicMap xmlns="http://www.topicmaps.org/xtm/" version="2.1"></topicMap>')
    ok_('2.1' == deser.version)


if __name__ == '__main__':
    import nose
    nose.core.runmodule()
