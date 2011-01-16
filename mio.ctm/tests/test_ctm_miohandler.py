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
Tests against the CTM 1.0 MIOHandler

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:version:      $Rev: 168 $ - $Date: 2009-06-26 14:22:56 +0200 (Fr, 26 Jun 2009) $
:license:      BSD license
"""
import unittest
from StringIO import StringIO
import codecs
import os
import mappa
from mappa.miohandler import MappaMapHandler
from mappa.writer.cxtm import CXTMTopicMapWriter
from tm.mio import Source, MIOException
from mio.ctm import create_deserializer, CTMHandler

class TestCTMHandler(unittest.TestCase):

    def __init__(self, file):
        unittest.TestCase.__init__(self, 'test_cxtm')
        self.file = file
        self.expected = os.path.abspath(os.path.dirname(file) + '/../baseline/%s.cxtm' % os.path.split(file)[1])

    def setUp(self):
        conn = mappa.connect()
        self._tm = conn.create('http://www.semagia.com/test-ctm-handler')

    def _make_handler(self):
        return MappaMapHandler(self._tm)

    def _make_ctmhandler(self, out):
        return CTMHandler(out)

    def test_cxtm(self):
        src = Source(file=open(self.file))
        # 1. Generate CTM 1.0 via CTMHandler
        out = StringIO()
        deser = create_deserializer()
        deser.handler = self._make_ctmhandler(out)
        try:
            deser.parse(src)
        except MIOException, ex:
            self.fail('failed: %s.\nError: %s' % (self.file, ex))            
        # 2. Read the generated CTM
        deser = create_deserializer()
        deser.handler = self._make_handler()
        new_src = Source(data=out.getvalue(), iri=src.iri)
        try:
            deser.parse(new_src)
        except MIOException, ex:
            self.fail('failed: %s.\nError: %s\nGenerated CTM: %s' % (self.file, ex, out.getvalue()))
        # 3. Generate the CXTM
        f = codecs.open(self.expected, encoding='utf-8')
        expected = f.read()
        f.close()
        result = StringIO()
        c14n = CXTMTopicMapWriter(result, src.iri)
        c14n.write(self._tm)
        res = result.getvalue()
        if not expected == res:
            self.fail('failed: %s.\nExpected: %s\nGot: %s\nGenerated CTM: %s' % (self.file, expected, res, out.getvalue()))

class TestPrefixes(unittest.TestCase):

    def make_handler(self, out=None):
        if out == None:
            out = StringIO()
        return CTMHandler(out)

    def test_registering(self):
        handler = self.make_handler()
        self.assertTrue(len(handler.prefixes) == 0)
        prefix, iri = 'base', 'http://www.semagia.com/base'
        handler.add_prefix(prefix, iri)
        prefixes = handler.prefixes
        self.assertTrue(len(prefixes) == 1)
        self.assertEquals(iri, prefixes[prefix])
        new_iri = iri + '/something-different'
        prefixes[prefix] = new_iri
        self.assertEquals(new_iri, prefixes[prefix])
        # The IRI must not have changed at the handler
        self.assertEquals(iri, handler.prefixes[prefix])
        handler.remove_prefix(prefix)
        self.assert_(prefix not in handler.prefixes)

    def test_registering_illegal(self):
        handler = self.make_handler()
        try:
            handler.add_prefix('.aaa', 'http://www.semagia.com/')
            self.fail('Expected an exception, illegal CTM identifier as prefix')
        except ValueError:
            pass
        try:
            handler.add_prefix('', 'http://www.semagia.com/')
            self.fail('Expected an exception, illegal CTM identifier as prefix')
        except ValueError:
            pass
        try:
            handler.add_prefix(None, 'http://www.semagia.com/')
            self.fail('Expected an exception, illegal CTM identifier as prefix')
        except ValueError:
            pass
        try:
            handler.add_prefix('a', '')
            self.fail('Expected an exception, illegal CTM IRI')
        except ValueError:
            pass
        try:
            handler.add_prefix('a', None)
            self.fail('Expected an exception, illegal CTM IRI')
        except ValueError:
            pass
        try:
            handler.add_prefix('a', 'http://www.{semagia}.com/')
            self.fail('Expected an exception, illegal CTM IRI')
        except ValueError:
            pass

    def test_illegal_removal(self):
        pass


def suite():
    def make_test(testcls):
        return unittest.TestLoader().loadTestsFromTestCase(testcls)
    import glob
    suite = unittest.TestSuite([make_test(TestPrefixes)])
    excluded = ['occurrence-string-multiline2.ctm', 'tm-reifier2.ctm']
    dir = os.path.abspath('./cxtm/ctm/in/')
    for filename in glob.glob(dir + '/*.ctm'):
        if os.path.split(filename)[-1] in excluded:
            continue
        testcase = TestCTMHandler(filename)
        suite.addTest(testcase)
    return suite

if __name__ == '__main__':
    unittest.main(defaultTest='suite')
