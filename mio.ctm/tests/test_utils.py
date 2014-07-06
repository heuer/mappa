# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
Tests against mio.ctm.utils

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
from nose.tools import eq_
from mio.ctm.utils import *


def test_is_native_datatype():
    eq_(False, is_native_datatype(XSD.string))
    eq_(True, is_native_datatype(XSD.integer))
    eq_(True, is_native_datatype(u'http://www.w3.org/2001/XMLSchema#dateTime'))
    eq_(True, is_native_datatype(u'http://psi.topicmaps.org/iso13250/ctm-integer'))


def test_keyword_valid():
    eq_(True, is_keyword(u'isa'))
    eq_(True, is_keyword(u'ako'))
    eq_(True, is_keyword(u'def'))
    eq_(True, is_keyword(u'end'))


def test_keyword_invalid():
    eq_(False, is_keyword(u'isa '))
    eq_(False, is_keyword(u'ISA'))


def test_iri_valid():
    data = (u'http://www.semagia.com/',)
    for iri in data:
        eq_(True, is_valid_iri(iri))


def test_iri_invalid():
    data = (u'<http://www.semagia.com/>', u'http://{www.semagia.com/}',
            u'http:// www.semagia.com/',)
    for iri in data:
        eq_(False, is_valid_iri(iri))


def test_valid_id_start():
    data = (u'_', u'A', u'a', u'ü', u'ä')
    for c in data:
        eq_(True, is_valid_id_start(c))


def test_invalid_id_start():
    data = (u'0', u'-', u'.')
    for c in data:
        eq_(False, is_valid_id_start(c))


def test_valid_localid_start():
    data = (u'0', u'ü',)
    for c in data:
        eq_(True, is_valid_localid_start(c))

def test_invalid_localid_start():
    data = (u'.', u'-')
    for c in data:
        eq_(False, is_valid_localid_start(c))


def test_valid_id_part():
    data = (u'-', u'.', u'0', u'a', u'ä', u'ö', u'ü', u'_')
    for c in data:
        eq_(True, is_valid_id_part(c))


def test_invalid_id_part():
    data = (' ',)
    for c in data:
        eq_(False, is_valid_id_part(c))


def test_valid_id():
    data = (u'ident', u'_ident', u'ident.ifier', u'a1976-09-19', u'isa', u'öüä')
    for c in data:
        eq_(True, is_valid_id(c))

def test_invalid_id():
    data = (u'ident.', u'-ident', u'2ident.ifier', u'.isa')
    for c in data:
        eq_(False, is_valid_id(c))


def test_valid_local_part():
    data = (u'1976-09-19', u'1semagia')
    for c in data:
        eq_(True, is_valid_local_part(c))


def test_invalid_local_part():
    data = (u'1976-09-19.', u'-semagia', u'.semagia', u'.1semagia')
    for c in data:
        eq_(False, is_valid_local_part(c))


def test_valid_iri_part():
    data = (u'a', u')')
    for c in data:
        eq_(True, is_valid_iri_part(c))

def test_invalid_iri_part():
    data = (u' ', u'"')
    for c in data:
        eq_(False, is_valid_iri_part(c))


def test_find_variables():
    def check(expected, res):
        eq_(expected, res)
    data = u"$a, $b, djddjd, $c, $______-d"
    res = (u'$a', '$b', '$c', '$______-d')
    for i, v in enumerate(find_variables(data)):
        yield check, res[i], v


def test_find_variables_omit_dollar():
    def check(expected, res):
        eq_(expected, res)
    data = u"$a, $b, djddjd, $c, $______-d"
    res = (u'a', 'b', 'c', '______-d')
    for i, v in enumerate(find_variables(data, True)):
        yield check, res[i], v


if __name__ == '__main__':
    import nose
    nose.core.runmodule()
