# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
Tests against the XTM content handler.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
from unittest import TestCase
from tm import Source
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

    def test_xtm21_detection1(self):
        deser = self._parse('<topicMap version="2.1"></topicMap>')
        self.assert_('2.1' == deser.version)

    def test_xtm21_detection2(self):
        deser = self._parse('<topicMap xmlns="http://www.topicmaps.org/xtm/" version="2.1"></topicMap>')
        self.assert_('2.1' == deser.version)


if __name__ == '__main__':
    import nose
    nose.core.runmodule()
