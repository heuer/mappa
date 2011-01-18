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
Tests the Python -> Java MIO compatibility; requires
`Jython <http://www.jython.org/>`_,
`Semagia MIO <http://mio.semagia.com/>`_ and 
`tinyTiM <http://tinytim.sourceforge.net/>`_

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:version:      $Rev: 167 $ - $Date: 2009-06-26 14:13:53 +0200 (Fr, 26 Jun 2009) $
:license:      BSD license
"""
from unittest import TestCase
from tm.mio import handler
from org.tmapi.core import TopicMapSystemFactory, Topic
from org.tinytim import Property
from org.tinytim.mio import MapInputHandler as TinyTimHandler

#TODO: This requires the outdated tinyTiM 1.5 (TMAPI 1.0) version. Update to TMAPI 2.0
class JMIOTestCase(TestCase):

    def setUp(self):
        tmSysFac = TopicMapSystemFactory.newInstance()
        tmSysFac.setProperty(Property.XTM10_REIFICATION, "false")
        tmSys = tmSysFac.newTopicMapSystem()
        self._tm = tmSys.createTopicMap('http://www.semagia.com/pytm')

    def _create_locator(self, iri):
        return self._tm.createLocator(iri)
    
    def _topic(self, **kw):
        iri = kw.get('sid')
        if iri:
            return self._tm.getTopicBySubjectIdentifier(self._create_locator(iri))
        iri = kw.get('slo')
        if iri:
            return self._tm.getTopicBySubjectLocator(self._create_locator(iri))
        iri = kw.get('iid')
        if iri:
            obj = self._tm.getObjectByItemIdentifier(self._create_locator(iri))
            return isinstance(obj, Topic) and obj or None
        raise Exception('No identity specified (iid, sid, slo)')

    def _make_handler(self):
        return handler.MIOHandlerToJava(TinyTimHandler(self._tm))
