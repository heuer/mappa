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
from tm.mio import Source
from tm.mio.handler import MapHandler
from mio.xtm import create_deserializer

#pylint: disable-msg=W0212
class TestXTMDeserializer(TestCase):
    
    def _parse(self, source):
        deser = create_deserializer()
        deser.handler = MapHandler()
        deser.parse(Source(data=source, iri='http://www.semagia.com/'))
        return deser
    
    def test_illegalstate(self):
        deser = create_deserializer()
        try:
            deser.version
            self.fail('The version should not be available yet')
        except AttributeError:
            pass

    def test_xtm10(self):
        deser = create_deserializer(version='1.0')
        self.assert_('1.0' == deser.version)

    def test_xtm20(self):
        deser = create_deserializer(version='2.0')
        self.assert_('2.0' == deser.version)

    def test_xtm10_detection(self):
        deser = self._parse('<topicMap xmlns="http://www.topicmaps.org/xtm/1.0/"></topicMap>')
        self.assert_('1.0' == deser.version)

    def test_xtm10_detection2(self):
        deser = self._parse('<topicMap></topicMap>')
        self.assert_('1.0' == deser.version)

    def test_xtm20_detection1(self):
        deser = self._parse('<topicMap version="2.0"></topicMap>')
        self.assert_('2.0' == deser.version)

    def test_xtm20_detection2(self):
        deser = self._parse('<topicMap xmlns="http://www.topicmaps.org/xtm/" version="2.0"></topicMap>')
        self.assert_('2.0' == deser.version)


if __name__ == '__main__':
    import nose
    nose.core.runmodule()
