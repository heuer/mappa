# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\


:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
import io
from nose.tools import ok_
from tm.voc import XSD
from mappaext.cxtm.cxtm_test import create_writer_cxtm_cases
from mio.jtm import create_deserializer
from mappaext.jtm import create_writer


fail = AssertionError


def create_jtm10_writer(out, base):
    return create_writer(out, base, version=1.0)


def create_jtm11_writer(out, base):
    writer = create_writer(out, base, version=1.1)
    writer.add_prefix(u'_', base)
    return writer


def test_jtm_10_writer():
    for test in create_writer_cxtm_cases(create_jtm10_writer, create_deserializer, 'jtm', 'jtm'):
        yield test


def test_jtm_11_writer():
    for test in create_writer_cxtm_cases(create_jtm11_writer, create_deserializer, 'jtm', 'jtm'):
        yield test
    for test in create_writer_cxtm_cases(create_jtm11_writer, create_deserializer, 'jtm11', 'jtm'):
        yield test


def test_add_prefix11():
    iri = 'http://www.semagia.com/'
    writer = create_jtm11_writer(io.BytesIO(), iri)
    writer.add_prefix('x', iri)
    ok_('x' in writer.prefixes)
    ok_(iri == writer.prefixes['x'])


def test_prefixes_keyword_arg():
    iri = 'http://www.semagia.com/'
    writer = writer = create_writer(io.BytesIO(), iri, version=1.1, prefixes={'x': iri})
    ok_('x' in writer.prefixes)
    ok_(iri == writer.prefixes['x'])


def test_add_prefix10():
    iri = 'http://www.semagia.com/'
    writer = create_jtm10_writer(io.BytesIO(), iri)
    try:
        writer.add_prefix('x', iri)
        fail('Expected an error for registering a prefix in JTM 1.0')
    except ValueError:
        pass


def test_add_xsd_prefix():
    iri = 'http://www.semagia.com/'
    writer = create_jtm11_writer(io.BytesIO(), iri)
    writer.add_prefix('Xsd', XSD)
    writer.add_prefix('xsd', XSD)
    writer.add_prefix('XSD', XSD)


def test_add_xsd_prefix_invalid():
    iri = 'http://www.semagia.com/'
    writer = create_jtm11_writer(io.BytesIO(), iri)
    try:
        writer.add_prefix('Xsd', iri)
        fail('The prefix "xsd" is reserved')
    except ValueError:
        pass


if __name__ == '__main__':
    import nose
    nose.core.runmodule()
