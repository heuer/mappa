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
Tests against the XTM 2.1 MIOHandler

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:version:      $Rev: 168 $ - $Date: 2009-06-26 14:22:56 +0200 (Fr, 26 Jun 2009) $
:license:      BSD license
"""
from unittest import TestCase
from StringIO import StringIO
import codecs
import os
import mappa
from mappa.miohandler import MappaMapHandler
from mappa.writer.cxtm import CXTMTopicMapWriter
from tm.mio import Source
from mio.xtm import create_deserializer
from mio.xtm.miohandler import XTM21Handler

class TestXTM21Handler(TestCase):

    def __init__(self, file):
        TestCase.__init__(self, 'test_cxtm')
        self.file = file
        self.expected = os.path.abspath(os.path.dirname(file) + '/../baseline/%s.cxtm' % os.path.split(file)[1])

    def setUp(self):
        conn = mappa.connect()
        self._tm = conn.create('http://www.semagia.com/test-xtm21-handler')

    def _make_handler(self):
        return MappaMapHandler(self._tm)

    def _make_xtmhandler(self, out):
        return XTM21Handler(out, prettify=True)

    def test_cxtm(self):
        src = Source(file=open(self.file))
        # 1. Generate XTM 2.1 via XTM21Handler
        out = StringIO()
        deser = create_deserializer()
        deser.handler = self._make_xtmhandler(out)
        deser.parse(src)
        # 2. Read the generated XTM 2.1
        deser = create_deserializer()
        deser.handler = self._make_handler()
        new_src = Source(data=out.getvalue(), iri=src.iri)
        try:
            deser.parse(new_src)
        except Exception, ex:
            self.fail('failed: %s.\nError: %s\nGenerated XTM 2.1: %s' % (self.file, ex, out.getvalue()))
        # 3. Generate the CXTM
        f = codecs.open(self.expected, encoding='utf-8')
        expected = f.read()
        f.close()
        result = StringIO()
        c14n = CXTMTopicMapWriter(result, src.iri)
        c14n.write(self._tm)
        res = result.getvalue()
        if not expected == res:
            self.fail('failed: %s.\nExpected: %s\nGot: %s\nGenerated XTM 2.1: %s' % (self.file, expected, res, out.getvalue()))

if __name__ == '__main__':
    import unittest, glob
    suite = unittest.TestSuite()
    dir = os.path.abspath('./cxtm/xtm2/in/')
    for filename in glob.glob(dir + '/*.xtm'):
        testcase = TestXTM21Handler(filename)
        suite.addTest(testcase)
    dir = os.path.abspath('./cxtm/xtm21/in/')
    for filename in glob.glob(dir + '/*.xtm'):
        testcase = TestXTM21Handler(filename)
        suite.addTest(testcase)    
    unittest.main(defaultTest='suite')
