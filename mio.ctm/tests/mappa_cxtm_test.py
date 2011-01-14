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

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:version:      $Rev: 169 $ - $Date: 2009-06-26 14:44:17 +0200 (Fr, 26 Jun 2009) $
:license:      BSD license
"""
from unittest import TestCase
import mappa
from mappa.miohandler import MappaMapHandler

class JMIOTestCase(TestCase):

    def setUp(self):
        conn = mappa.connect()
        self._tm = conn.create('http://www.semagia.com/pytm')

    def _make_handler(self):
        return MappaMapHandler(self._tm)


from StringIO import StringIO
import codecs
import os
from mappa.writer.cxtm import CXTMTopicMapWriter
from tm.mio import Source

class JCXTMTestCase(JMIOTestCase):
    """\
    
    """
    def __init__(self, deserializer, input):
        JMIOTestCase.__init__(self, 'test_cxtm')
        self.input = input
        self.expected = os.path.abspath(os.path.dirname(input) + '/../baseline/%s.cxtm' % os.path.split(input)[1])
        self.deserializer = deserializer

    def test_cxtm(self):
        src = Source(file=open(self.input, 'rb'))
        self.deserializer.handler = self._make_handler()
        try:
            self.deserializer.parse(src)
        except Exception, ex:
            raise Exception(ex, 'Error in ' + self.input)
        # CXTM is always UTF-8
        f = codecs.open(self.expected, encoding='utf-8')
        expected = f.read()
        f.close()
        result = StringIO()
        c14n = CXTMTopicMapWriter(result, src.iri)
        c14n.write(self._tm)
        res = result.getvalue()
        if not expected == res:
            self.fail('failed: %s.\nExpected: %s\nGot: %s' % (self.input, expected, res))
