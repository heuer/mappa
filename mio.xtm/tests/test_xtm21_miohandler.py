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
import unittest
from mappaext.cxtm.cxtm_test import find_valid_cxtm_cases
from StringIO import StringIO
import codecs
import os
import mappa
from mappa.miohandler import MappaMapHandler
from mappaext.cxtm import create_writer
from tm.mio import Source
from mio.xtm import create_deserializer, XTM21Handler

class _TestXTM21Handler(unittest.TestCase):

    def __init__(self, file):
        unittest.TestCase.__init__(self, 'test_cxtm')
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
        c14n = create_writer(result, src.iri)
        c14n.write(self._tm)
        res = unicode(result.getvalue(), 'utf-8')
        if expected != res:
            self.fail('failed: %s.\nExpected: %s\nGot: %s\nGenerated XTM 2.1: %s' % (self.file, expected, res, out.getvalue()))

def test_xtm_20():
    for filename in find_valid_cxtm_cases('xtm2', 'xtm'):
        yield _TestXTM21Handler(filename)

def test_xtm_21():
    for filename in find_valid_cxtm_cases('xtm1', 'xtm'):
        yield _TestXTM21Handler(filename)


if __name__ == '__main__':
    import nose
    nose.core.runmodule()
