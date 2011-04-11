# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2009 -- Lars Heuer - Semagia <http://www.semagia.com/>.
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
Tests against ``tm.mio.Source``.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
from unittest import TestCase
from urllib import pathname2url
from urlparse import urljoin
from tm.mio import Source
from tm import irilib

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
