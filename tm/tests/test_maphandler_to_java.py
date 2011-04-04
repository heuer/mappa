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
from java.lang import Exception as JavaException
from tm import mio, XSD, TMDM
from tm.mio import handler
from jmio_test import JMIOTestCase

class TestMapHandlerToJava(JMIOTestCase):

    def test_simplify(self):
        handler_ = self._make_handler()
        self.assert_(handler.simplify(handler_) is handler_)

    def test_empty(self):
        handler = self._make_handler()
        self.assertEqual(0, self._tm.getTopics().size())
        self.assertEqual(0, self._tm.getAssociations().size())
        handler.startTopicMap()
        handler.endTopicMap()
        self.assertEqual(0, self._tm.getTopics().size())
        self.assertEqual(0, self._tm.getAssociations().size())

    def test_tm_reifier(self):
        handler = self._make_handler()
        iid = 'http://example.semagia.com/map/#1'
        self.assertEqual(0, self._tm.getTopics().size())
        self.assertEqual(0, self._tm.getAssociations().size())
        handler.startTopicMap()
        handler.startReifier()
        handler.startTopic((mio.ITEM_IDENTIFIER, iid))
        handler.endTopic()
        handler.endReifier()
        handler.endTopicMap()
        self.assertEqual(1, self._tm.getTopics().size())
        self.assertEqual(0, self._tm.getAssociations().size())
        topic = self._topic(iid=iid)
        self.assert_(topic is not None)
        self.assert_(self._tm.reifier is not None)
        self.assertEqual(topic, self._tm.reifier)

    def test_tm_reifier2(self):
        handler = self._make_handler()
        iid = 'http://example.semagia.com/map/#1'
        self.assertEqual(0, self._tm.getTopics().size())
        self.assertEqual(0, self._tm.getAssociations().size())
        handler.startTopicMap()
        handler.startReifier()
        handler.topicRef((mio.ITEM_IDENTIFIER, iid))
        handler.endReifier()
        handler.endTopicMap()
        self.assertEqual(1, self._tm.getTopics().size())
        self.assertEqual(0, self._tm.getAssociations().size())
        topic = self._topic(iid=iid)
        self.assert_(topic is not None)
        self.assert_(self._tm.reifier is not None)
        self.assertEqual(topic, self._tm.reifier)

    def test_topic_creation_sid(self):
        sid = 'http://psi.example.org/semagia'
        self.assert_(None is self._topic(sid=sid))
        handler = self._make_handler()
        handler.startTopicMap()
        handler.topic((mio.SUBJECT_IDENTIFIER, sid))
        handler.endTopicMap()
        topic = self._topic(sid=sid)
        self.assert_(topic is not None)

    def test_topic_creation_slo(self):
        slo = 'http://www.semagia.com/'
        self.assert_(None is self._topic(slo=slo))
        handler = self._make_handler()
        handler.startTopicMap()
        handler.topic((mio.SUBJECT_LOCATOR, slo))
        handler.endTopicMap()
        topic = self._topic(slo=slo)
        self.assert_(topic is not None)

    def test_topic_creation_iid(self):
        iid = 'http://www.semagia.com/something#x'
        self.assert_(None is self._topic(iid=iid))
        handler = self._make_handler()
        handler.startTopicMap()
        handler.topic((mio.ITEM_IDENTIFIER, iid))
        handler.endTopicMap()
        topic = self._topic(iid=iid)
        self.assert_(topic is not None)

    def test_topic_type_instance(self):
        iid = 'http://www.semagia.com/something#x'
        iid2 = 'http://www.semagia.com/something#y'
        topic = self._topic(iid=iid)
        self.assert_(None is topic)
        handler = self._make_handler()
        handler.startTopicMap()
        handler.startTopic((mio.ITEM_IDENTIFIER, iid))
        handler.isa((mio.ITEM_IDENTIFIER, iid2))
        handler.endTopic()
        handler.endTopicMap()
        topic = self._topic(iid=iid)
        self.assert_(topic is not None)
        topic2 = self._topic(iid=iid2)
        self.assert_(topic2 is not None)
        self.assert_(topic2 in topic.types)

    def test_type_instance_invalid(self):
        iid = 'http://www.semagia.com/something#x'
        handler = self._make_handler()
        handler.startTopicMap()
        handler.startAssociation()
        try:
            handler.isa((mio.ITEM_IDENTIFIER, iid))
            self.fail('startIsa is disallowed outside a topic context')
        except JavaException:
            pass

    def test_association_creation(self):
        assoc_type = 'http://psi.example.org/assoc'
        role_type = 'http://psi.example.org/role-type'
        role_player = 'http://psi.example.org/role-player'
        for ident in (assoc_type, role_type, role_player):
            topic = self._topic(sid=ident)
            self.assert_(topic is None)
        handler = self._make_handler()
        handler.startTopicMap()
        handler.startAssociation((mio.SUBJECT_IDENTIFIER, assoc_type))
        handler.startRole((mio.SUBJECT_IDENTIFIER, role_type))
        handler.player((mio.SUBJECT_IDENTIFIER, role_player))
        handler.endRole()
        handler.endAssociation()
        handler.endTopicMap()
        for ident in (assoc_type, role_type, role_player):
            topic = self._topic(sid=ident)
            self.assert_(topic is not None)
        self.assertEqual(1, self._tm.getAssociations().size())
        assoc = self._tm.getAssociations().iterator().next()
        self.assert_(assoc is not None)
        self.assertEqual(1, assoc.getAssociationRoles().size())
        typ = self._topic(sid=assoc_type)
        self.assert_(typ is not None)
        self.assertEqual(typ, assoc.type)
        r_typ = self._topic(sid=role_type)
        player = self._topic(sid=role_player)
        self.assert_(r_typ is not None)
        self.assert_(player is not None)
        for role in assoc.getAssociationRoles():
            self.assertEqual(r_typ, role.type)
            self.assertEqual(player, role.player)

    def test_occurrence(self):
        iid1 = 'http://www.semagia.com/test#1'
        iid2 = 'http://www.semagia.com/test#2'
        handler = self._make_handler()
        handler.startTopicMap()
        handler.startTopic((mio.ITEM_IDENTIFIER, iid1))
        handler.startOccurrence()
        handler.type((mio.ITEM_IDENTIFIER, iid2))
        handler.value('Semagia', XSD.string)
        handler.endOccurrence()
        handler.endTopic()
        handler.endTopicMap()
        self.assertEqual(2, self._tm.topics.size())
        topic = self._topic(iid=iid1)
        self.assertEqual(1, topic.occurrences.size())
        occ = topic.occurrences.iterator().next()
        self.assertEqual('Semagia', occ.value)
        #TODO: Update if TMAPI is datatype aware
        #self.assertEqual(XSD.string, occ.datatype)
        typ = self._topic(iid=iid2)
        self.assert_(typ is not None)
        self.assertEqual(typ, occ.type)

    def test_name(self):
        iid1 = 'http://www.semagia.com/test#1'
        iid2 = 'http://www.semagia.com/test#2'
        handler = self._make_handler()
        handler.startTopicMap()
        handler.startTopic((mio.ITEM_IDENTIFIER, iid1))
        handler.startName()
        handler.type((mio.ITEM_IDENTIFIER, iid2))
        handler.value('Semagia')
        handler.endName()
        handler.endTopic()
        handler.endTopicMap()
        self.assertEqual(2, self._tm.topics.size())
        topic = self._topic(iid=iid1)
        self.assertEqual(1, topic.getTopicNames().size())
        name = topic.getTopicNames().iterator().next()
        self.assertEqual('Semagia', name.value)
        typ = self._topic(iid=iid2)
        self.assert_(typ is not None)
        self.assertEqual(typ, name.type)

    def test_name_defaulttype(self):
        iid1 = 'http://www.semagia.com/test#1'
        handler = self._make_handler()
        handler.startTopicMap()
        handler.startTopic((mio.ITEM_IDENTIFIER, iid1))
        handler.startName()
        handler.value('Semagia')
        handler.endName()
        handler.endTopic()
        handler.endTopicMap()
        self.assertEqual(2, self._tm.topics.size())
        topic = self._topic(iid=iid1)
        self.assertEqual(1, topic.getTopicNames().size())
        name = topic.getTopicNames().iterator().next()
        self.assertEqual('Semagia', name.value)
        self.assert_(self._create_locator(TMDM.topic_name) in name.type.subjectIdentifiers)

    def test_name_invalid_value(self):
        iid1 = 'http://www.semagia.com/test#1'
        handler = self._make_handler()
        handler.startTopicMap()
        handler.startTopic((mio.ITEM_IDENTIFIER, iid1))
        handler.startName()
        try:
            handler.value('Semagia', XSD.string)
            self.fail('Datatype in a name-context is disallowed')
        except JavaException:
            pass

    def test_occurrence_invalid_value(self):
        iid1 = 'http://www.semagia.com/test#1'
        handler = self._make_handler()
        handler.startTopicMap()
        handler.startTopic((mio.ITEM_IDENTIFIER, iid1))
        handler.startOccurrence()
        try:
            handler.value('Semagia')
            self.fail('Datatype in an occurrence-context is necessary')
        except JavaException:
            pass

    def test_variant(self):
        iid1 = 'http://www.semagia.com/test#1'
        iid2 = 'http://www.semagia.com/test#2'
        iid3 = 'http://www.semagia.com/test#3'
        handler = self._make_handler()
        handler.startTopicMap()
        handler.startTopic((mio.ITEM_IDENTIFIER, iid1))
        handler.startName()
        handler.type((mio.ITEM_IDENTIFIER, iid2))
        handler.value('Semagia')
        handler.startVariant()
        handler.value('semagia', XSD.string)
        handler.startScope()
        handler.theme((mio.ITEM_IDENTIFIER, iid3))
        handler.endScope()
        handler.endVariant()
        handler.endName()
        handler.endTopic()
        handler.endTopicMap()
        self.assertEqual(3, self._tm.topics.size())
        topic = self._topic(iid=iid1)
        self.assertEqual(1, topic.getTopicNames().size())
        name = topic.getTopicNames().iterator().next()
        self.assertEqual('Semagia', name.value)
        self.assertEqual(1, name.variants.size())
        var = name.variants.iterator().next()
        self.assertEqual('semagia', var.value)
        #TODO: Update if TMAPI is datatype aware
        #self.assertEqual(XSD.string, var.datatype)
        theme = self._topic(iid=iid3)
        self.assert_(theme in var.scope)

    def test_variant_no_scope(self):
        iid1 = 'http://www.semagia.com/test#1'
        iid2 = 'http://www.semagia.com/test#2'
        handler = self._make_handler()
        handler.startTopicMap()
        handler.startTopic((mio.ITEM_IDENTIFIER, iid1))
        handler.startName()
        handler.type((mio.ITEM_IDENTIFIER, iid2))
        handler.value('Semagia')
        handler.startVariant()
        handler.value('semagia', XSD.string)
        try:
            handler.endVariant()
            self.fail('Map handler accepts a variant in the unconstrained scope')
        except JavaException:
            pass

    def test_variant_eq_scope(self):
        iid1 = 'http://www.semagia.com/test#1'
        iid2 = 'http://www.semagia.com/test#2'
        iid3 = 'http://www.semagia.com/test#3'
        iid4 = 'http://www.semagia.com/test#4'
        handler = self._make_handler()
        handler.startTopicMap()
        handler.startTopic((mio.ITEM_IDENTIFIER, iid1))
        handler.startName()
        handler.type((mio.ITEM_IDENTIFIER, iid2))
        handler.startScope()
        handler.theme((mio.ITEM_IDENTIFIER, iid3))
        handler.theme((mio.ITEM_IDENTIFIER, iid4))
        handler.endScope()
        handler.value('Semagia')
        handler.startVariant()
        handler.startScope()
        handler.theme((mio.ITEM_IDENTIFIER, iid4))
        handler.theme((mio.ITEM_IDENTIFIER, iid3))
        handler.endScope()
        handler.value('semagia', XSD.string)
        try:
            handler.endVariant()
            self.fail('Map handler accepts a variant in the same scope as the name scope')
        except JavaException:
            pass

if __name__ == '__main__':
    from test import test_support
    test_support.run_unittest(TestMapHandlerToJava)
