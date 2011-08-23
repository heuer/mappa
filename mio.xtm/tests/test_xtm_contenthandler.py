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
Tests against the XTM content handler.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:version:      $Rev: 402 $ - $Date: 2011-01-14 16:30:38 +0100 (Fr, 14 Jan 2011) $
:license:      BSD license
"""
from unittest import TestCase
from xml import sax
from StringIO import StringIO
from tm.mio.handler import MapHandler
from mio.xtm import XTMContentHandler
from mio.xtm.xtm1 import XTM10ContentHandler
from mio.xtm.xtm2 import XTM2ContentHandler

#pylint: disable-msg=W0212
class TestXTMContentHandler(TestCase):
    
    def _parse(self, source):
        ch = XTMContentHandler()
        ch.map_handler = MapHandler()
        ch.doc_iri = 'http://www.semagia.com/'
        parser = sax.make_parser()
        parser.setFeature(sax.handler.feature_namespaces, True)
        parser.setContentHandler(ch)
        parser.parse(StringIO(source))
        return ch._content_handler
    
    def test_xtm10_detection(self):
        ch = self._parse('<topicMap xmlns="http://www.topicmaps.org/xtm/1.0/"></topicMap>')
        self.assert_(isinstance(ch, XTM10ContentHandler))

    def test_xtm10_detection2(self):
        ch = self._parse('<topicMap></topicMap>')
        self.assert_(isinstance(ch, XTM10ContentHandler))

    def test_xtm20_detection1(self):
        ch = self._parse('<topicMap version="2.0"></topicMap>')
        self.assert_(isinstance(ch, XTM2ContentHandler))

    def test_xtm20_detection2(self):
        ch = self._parse('<topicMap xmlns="http://www.topicmaps.org/xtm/" version="2.0"></topicMap>')
        self.assert_(isinstance(ch, XTM2ContentHandler))

    def test_xtm21_detection1(self):
        ch = self._parse('<topicMap version="2.1"></topicMap>')
        self.assert_(isinstance(ch, XTM2ContentHandler))

    def test_xtm21_detection2(self):
        ch = self._parse('<topicMap xmlns="http://www.topicmaps.org/xtm/" version="2.1"></topicMap>')
        self.assert_(isinstance(ch, XTM2ContentHandler))


if __name__ == '__main__':
    import nose
    nose.core.runmodule()
