# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
Tests against ``tm.mio.Source``.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
from nose.tools import ok_, eq_
from urllib import pathname2url
from urlparse import urljoin
from tm import irilib, Source


fail = AssertionError

def test_file():
    f = open(__file__)
    src = Source(file=f)
    ok_(src.stream)
    ok_(src.encoding is None)
    url = irilib.normalize(urljoin('file:', pathname2url(f.name)))
    eq_(url, src.iri)


def test_file_iri():
    f = open('__init__.py')
    src = Source('http://www.semagia.com/', file=f)
    ok_(src.stream)
    ok_(src.encoding is None)
    eq_('http://www.semagia.com/', src.iri)


def test_iri():
    src = Source('http://www.semagia.com/')
    ok_(src.stream is None)
    ok_(src.encoding is None)
    eq_('http://www.semagia.com/', src.iri)


def test_data():
    src = Source('http://www.semagia.com/', data='Semagia')
    ok_(src.stream)
    ok_(src.encoding is None)
    eq_('http://www.semagia.com/', src.iri)


def test_invalid():
    try:
        Source(encoding='utf-8')
        fail('Expected an exception, only the encoding is provided')
    except ValueError:
        pass


def test_invalid_no_args():
    try:
        Source()
        fail('Expected an exception: No args are provided')
    except ValueError:
        pass


def test_data_invalid():
    try:
        Source(data='Semagia')
        fail('Expected an exception, only the data is provided, no IRI')
    except ValueError:
        pass


def test_immutable():
    src = Source('http://www.semagia.com/')
    try:
        src.iri = 'http://www.google.com/'
        fail('.iri should be immutable')
    except AttributeError:
        pass
    try:
        src.encoding = 'utf-8'
        fail('.encoding should be immutable')
    except AttributeError:
        pass
    try:
        src.stream = None
        fail('.stream should be immutable')
    except AttributeError:
        pass


if __name__ == '__main__':
    import nose
    nose.core.runmodule()
