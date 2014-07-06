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
from unittest import TestCase
from urllib import pathname2url
from urlparse import urljoin
from tm import irilib, Source


class TestSource(TestCase):

    def test_file(self):
        f = open(__file__)
        src = Source(file=f)
        self.assert_(src.stream)
        self.assert_(src.encoding is None)
        url = irilib.normalize(urljoin('file:', pathname2url(f.name)))
        self.assertEqual(url, src.iri)

    def test_file_iri(self):
        f = open('__init__.py')
        src = Source('http://www.semagia.com/', file=f)
        self.assert_(src.stream)
        self.assert_(src.encoding is None)
        self.assertEqual('http://www.semagia.com/', src.iri)

    def test_iri(self):
        src = Source('http://www.semagia.com/')
        self.assert_(src.stream is None)
        self.assert_(src.encoding is None)
        self.assertEqual('http://www.semagia.com/', src.iri)

    def test_data(self):
        src = Source('http://www.semagia.com/', data='Semagia')
        self.assert_(src.stream)
        self.assert_(src.encoding is None)
        self.assertEqual('http://www.semagia.com/', src.iri)

    def test_invalid(self):
        try:
            Source(encoding='utf-8')
            self.fail('Expected an exception, only the encoding is provided')
        except ValueError:
            pass

    def test_invalid_no_args(self):
        try:
            Source()
            self.fail('Expected an exception: No args are provided')
        except ValueError:
            pass

    def test_data_invalid(self):
        try:
            Source(data='Semagia')
            self.fail('Expected an exception, only the data is provided, no IRI')
        except ValueError:
            pass

    def test_immutable(self):
        src = Source('http://www.semagia.com/')
        try:
            src.iri = 'http://www.google.com/'
            self.fail('.iri should be immutable')
        except AttributeError:
            pass
        try:
            src.encoding = 'utf-8'
            self.fail('.encoding should be immutable')
        except AttributeError:
            pass
        try:
            src.stream = None
            self.fail('.stream should be immutable')
        except AttributeError:
            pass


if __name__ == '__main__':
    import nose
    nose.core.runmodule()
