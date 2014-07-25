# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
Tests against the Mappa MIO ``MapHandler``.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD License
"""
from os import path
import sys
sys.path.append(path.join(path.dirname(__file__), '..'))
from tm import mio
from tm.mio.handler import simplify
from . mappa_test import MappaTestCase, len_
from mappa import XSD, TMDM
from mappa.miohandler import MappaMapHandler

# pylint: disable-msg=W0703
class TestMappaHandler(MappaTestCase):
    """\
    
    """
    
    def _make_handler(self):
        return simplify(MappaMapHandler(self._tm))

    def test_variant_no_value(self):
        theTopic = (mio.ITEM_IDENTIFIER, "http://test.semagia.com/the-topic")
        theme = (mio.ITEM_IDENTIFIER, "http://test.semagia.com/theme")
        handler = self._make_handler()   
        handler.startTopicMap()
        handler.startTopic(theTopic)
        handler.startName()
        handler.value("Semagia")
        handler.startVariant()
        handler.startScope()
        handler.startTheme()
        handler.topicRef(theme)
        handler.endTheme()
        handler.endScope()
        try:
            handler.endVariant()
            self.fail("Expected an error since the variant has no value")
        except mio.MIOException:
            pass

    def test_name_no_value(self):
        theTopic = (mio.ITEM_IDENTIFIER, "http://test.semagia.com/the-topic")
        handler = self._make_handler()    
        handler.startTopicMap()
        handler.startTopic(theTopic)
        handler.startName()
        try:
            handler.endName()
            self.fail("Expected an error since the name has no value")
        except mio.MIOException:
            pass

    def test_issue_23(self):
        # http://code.google.com/p/mappa/issues/detail?id=23
        iid = 'http://mappa.semagia.com/issue-23'
        iid2 = 'http://mappa.semagia.com/issue-23_'
        handler = self._make_handler()
        handler.startTopicMap()
        handler.startTopic((mio.ITEM_IDENTIFIER, iid))
        handler.startName()
        handler.value('test')
        handler.type((mio.SUBJECT_IDENTIFIER, TMDM.topic_name))
        handler.endName()
        handler.endTopic()
        handler.startTopic((mio.ITEM_IDENTIFIER, iid2))
        handler.startName()
        handler.value('a test')
        handler.type((mio.SUBJECT_IDENTIFIER, TMDM.topic_name))
        handler.endName()
        handler.subjectIdentifier(TMDM.topic_name)
        handler.endTopic()
        handler.endTopicMap()

    def test_issue_34(self):
        # http://code.google.com/p/mappa/issues/detail?id=34
        assocType = mio.ITEM_IDENTIFIER, "http://test.semagia.com/assoc-type"
        roleType = mio.ITEM_IDENTIFIER, "http://test.semagia.com/role-type"
        rolePlayer = mio.ITEM_IDENTIFIER, "http://test.semagia.com/role-player"
        reifier = mio.ITEM_IDENTIFIER, "http://test.semagia.com/reifier"
        roleIID = "http://test.semagia.com/role-iid";
        handler = self._make_handler()
        handler.startTopicMap()
        handler.startAssociation()
        handler.startReifier()
        handler.topicRef(reifier)
        handler.endReifier()
        handler.startType()
        handler.topicRef(assocType)
        handler.endType()
        handler.startRole()
        handler.itemIdentifier(roleIID)
        handler.startType()
        handler.topicRef(roleType)
        handler.endType()
        handler.startPlayer()
        handler.topicRef(rolePlayer)
        handler.endPlayer()
        handler.endRole()
        handler.endAssociation()
        
        handler.startAssociation()
        handler.startReifier()
        handler.topicRef(reifier)
        handler.endReifier()
        handler.startType()
        handler.topicRef(assocType)
        handler.endType()
        handler.startRole()
        handler.startType()
        handler.topicRef(roleType)
        handler.endType()
        handler.startPlayer()
        handler.topicRef(rolePlayer)
        handler.endPlayer()
        handler.endRole()
        handler.endAssociation()
        handler.endTopicMap()
        self.assertEquals(1, len_(self._tm.associations))
        assoc = tuple(self._tm.associations)[0]
        self.assert_(assoc.reifier)
        tmc = self._tm.construct(iid=roleIID)
        self.assert_(tmc)
        self.assertEquals(assoc, tmc.parent)

    def test_issue_34_2(self):
        # http://code.google.com/p/mappa/issues/detail?id=34
        assocType = mio.ITEM_IDENTIFIER, "http://test.semagia.com/assoc-type"
        roleType = mio.ITEM_IDENTIFIER, "http://test.semagia.com/role-type"
        rolePlayer = mio.ITEM_IDENTIFIER, "http://test.semagia.com/role-player"
        reifier = mio.ITEM_IDENTIFIER, "http://test.semagia.com/reifier"
        roleIID = "http://test.semagia.com/role-iid"
        handler = self._make_handler()
        handler.startTopicMap()
        handler.startAssociation()
        handler.startReifier()
        handler.topicRef(reifier)
        handler.endReifier()
        handler.startType()
        handler.topicRef(assocType)
        handler.endType()
        handler.startRole()
        handler.startType()
        handler.topicRef(roleType)
        handler.endType()
        handler.startPlayer()
        handler.topicRef(rolePlayer)
        handler.endPlayer()
        handler.endRole()
        handler.endAssociation()
        
        handler.startAssociation()
        handler.startReifier()
        handler.topicRef(reifier)
        handler.endReifier()
        handler.startType()
        handler.topicRef(assocType)
        handler.endType()
        handler.startRole()
        handler.itemIdentifier(roleIID)
        handler.startType()
        handler.topicRef(roleType)
        handler.endType()
        handler.startPlayer()
        handler.topicRef(rolePlayer)
        handler.endPlayer()
        handler.endRole()
        handler.endAssociation()
        handler.endTopicMap()
        self.assertEquals(1, len_(self._tm.associations))
        assoc = tuple(self._tm.associations)[0]
        self.assert_(assoc.reifier)
        tmc = self._tm.construct(iid=roleIID)
        self.assert_(tmc)
        self.assertEquals(assoc, tmc.parent)
        
    def test_issue_34_role_reifier(self):
        # http://code.google.com/p/mappa/issues/detail?id=34
        assocType = mio.ITEM_IDENTIFIER, "http://test.semagia.com/assoc-type"
        roleType = mio.ITEM_IDENTIFIER, "http://test.semagia.com/role-type"
        rolePlayer = mio.ITEM_IDENTIFIER, "http://test.semagia.com/role-player"
        reifier = mio.ITEM_IDENTIFIER, "http://test.semagia.com/reifier"
        roleIID = "http://test.semagia.com/role-iid"
        handler = self._make_handler()
        handler.startTopicMap()
        handler.startAssociation()
        handler.startType()
        handler.topicRef(assocType)
        handler.endType()
        handler.startRole()
        handler.startReifier()
        handler.topicRef(reifier)
        handler.endReifier()
        handler.itemIdentifier(roleIID)
        handler.startType()
        handler.topicRef(roleType)
        handler.endType()
        handler.startPlayer()
        handler.topicRef(rolePlayer)
        handler.endPlayer()
        handler.endRole()
        handler.endAssociation()
        
        handler.startAssociation()
        handler.startType()
        handler.topicRef(assocType)
        handler.endType()
        handler.startRole()
        handler.startReifier()
        handler.topicRef(reifier)
        handler.endReifier()
        handler.startType()
        handler.topicRef(roleType)
        handler.endType()
        handler.startPlayer()
        handler.topicRef(rolePlayer)
        handler.endPlayer()
        handler.endRole()
        handler.endAssociation()
        handler.endTopicMap()
        self.assertEquals(1, len_(self._tm.associations))
        assoc = tuple(self._tm.associations)[0]
        self.assert_(assoc.reifier is None)
        tmc = self._tm.construct(iid=roleIID)
        self.assert_(tmc)
        self.assertEquals(assoc, tmc.parent)

    def test_issue_34_role_reifier_invalid(self):
        # http://code.google.com/p/mappa/issues/detail?id=34
        assocType = mio.ITEM_IDENTIFIER, "http://test.semagia.com/assoc-type"
        assocType2 = mio.ITEM_IDENTIFIER, "http://test.semagia.com/assoc-type2"
        roleType = mio.ITEM_IDENTIFIER, "http://test.semagia.com/role-type"
        rolePlayer = mio.ITEM_IDENTIFIER, "http://test.semagia.com/role-player"
        reifierIID = "http://test.semagia.com/reifier"
        reifier = mio.ITEM_IDENTIFIER, reifierIID
        roleIID = "http://test.semagia.com/role-iid"
        handler = self._make_handler()
        handler.startTopicMap()
        handler.startAssociation()
        handler.startType()
        handler.topicRef(assocType)
        handler.endType()
        handler.startRole()
        handler.startReifier()
        handler.topicRef(reifier)
        handler.endReifier()
        handler.itemIdentifier(roleIID)
        handler.startType()
        handler.topicRef(roleType)
        handler.endType()
        handler.startPlayer()
        handler.topicRef(rolePlayer)
        handler.endPlayer()
        handler.endRole()
        handler.endAssociation()
        try:
            handler.startAssociation()
            handler.startType()
            handler.topicRef(assocType2)
            handler.endType()
            handler.startRole()
            handler.startReifier()
            handler.topicRef(reifier)
            handler.endReifier()
            handler.startType()
            handler.topicRef(roleType)
            handler.endType()
            handler.startPlayer()
            handler.topicRef(rolePlayer)
            handler.endPlayer()
            handler.endRole()
            handler.endAssociation()
            self.fail('The topic "%s" reifies another role' % reifierIID)
        except mio.MIOException:
            pass

    def test_issue_34_variant_reifier(self):
        # http://code.google.com/p/mappa/issues/detail?id=34
        topic_iid = "http://test.semagia.com/the-topic"
        theTopic = (mio.ITEM_IDENTIFIER, topic_iid);
        reifierIID = "http://test.semagia.com/reifier";
        variantIID = "http://test.semagia.com/variant";
        reifier = (mio.ITEM_IDENTIFIER, reifierIID);
        theme = (mio.ITEM_IDENTIFIER, "http://test.semagia.com/theme");
        handler = self._make_handler()
        handler.startTopicMap();
        handler.startTopic(theTopic);
        handler.startName();
        handler.value("Semagia");
        handler.startVariant();
        handler.startReifier();
        handler.topicRef(reifier);
        handler.endReifier();
        handler.value("variant", XSD.string);
        handler.itemIdentifier(variantIID);
        handler.startScope();
        handler.startTheme();
        handler.topicRef(theme);
        handler.endTheme();
        handler.endScope();
        handler.endVariant();
        handler.endName();

        handler.startName();
        handler.value("Semagia");
        handler.startVariant();
        handler.startReifier();
        handler.topicRef(reifier);
        handler.endReifier();
        handler.value("variant", XSD.string);
        handler.startScope();
        handler.startTheme();
        handler.topicRef(theme);
        handler.endTheme();
        handler.endScope();
        handler.endVariant();
        handler.endName();
        handler.endTopic();
        handler.endTopicMap();
        reifying = self._tm.topic(iid=reifierIID);
        self.assert_(reifying);
        self.assert_(reifying.reified);
        self.assertEquals(reifying.reified, self._tm.construct(iid=variantIID));
        topic = self._tm.topic(iid=topic_iid)
        self.assert_(topic)
        self.assertEqual(1, len_(topic.names))
        name = tuple(topic.names)[0]
        self.assertEqual(1, len_(name.variants))

    def test_issue_34_variant_reifier2(self):
        # http://code.google.com/p/mappa/issues/detail?id=34
        topic_iid = "http://test.semagia.com/the-topic"
        theTopic = (mio.ITEM_IDENTIFIER, topic_iid);
        reifierIID = "http://test.semagia.com/reifier";
        variantIID = "http://test.semagia.com/variant";
        reifier = (mio.ITEM_IDENTIFIER, reifierIID);
        theme = (mio.ITEM_IDENTIFIER, "http://test.semagia.com/theme");
        handler = self._make_handler()
        handler.startTopicMap();
        handler.startTopic(theTopic);
        handler.startName();
        handler.value("Semagia");
        handler.startVariant();
        handler.startReifier();
        handler.topicRef(reifier);
        handler.endReifier();
        handler.value("variant", XSD.string);
        handler.startScope();
        handler.startTheme();
        handler.topicRef(theme);
        handler.endTheme();
        handler.endScope();
        handler.endVariant();
        handler.endName();

        handler.startName();
        handler.value("Semagia");
        handler.startVariant();
        handler.startReifier();
        handler.topicRef(reifier);
        handler.endReifier();
        handler.value("variant", XSD.string);
        handler.itemIdentifier(variantIID);
        handler.startScope();
        handler.startTheme();
        handler.topicRef(theme);
        handler.endTheme();
        handler.endScope();
        handler.endVariant();
        handler.endName();
        handler.endTopic();
        handler.endTopicMap();
        reifying = self._tm.topic(iid=reifierIID);
        self.assert_(reifying);
        self.assert_(reifying.reified);
        self.assertEquals(reifying.reified, self._tm.construct(iid=variantIID));
        topic = self._tm.topic(iid=topic_iid)
        self.assert_(topic)
        self.assertEqual(1, len_(topic.names))
        name = tuple(topic.names)[0]
        self.assertEqual(1, len_(name.variants))

    def test_issue_34_variant_reifier_invalid(self):
        # http://code.google.com/p/mappa/issues/detail?id=34
        topic_iid = "http://test.semagia.com/the-topic"
        theTopic = (mio.ITEM_IDENTIFIER, topic_iid);
        reifierIID = "http://test.semagia.com/reifier";
        variantIID = "http://test.semagia.com/variant";
        reifier = (mio.ITEM_IDENTIFIER, reifierIID);
        theme = (mio.ITEM_IDENTIFIER, "http://test.semagia.com/theme");
        handler = self._make_handler()
        handler.startTopicMap();
        handler.startTopic(theTopic);
        handler.startName();
        handler.value("Semagia");
        handler.startVariant();
        handler.startReifier();
        handler.topicRef(reifier);
        handler.endReifier();
        handler.value("variant", XSD.string);
        handler.startScope();
        handler.startTheme();
        handler.topicRef(theme);
        handler.endTheme();
        handler.endScope();
        handler.endVariant();
        handler.endName();

        try:
            handler.startName();
            handler.value("Not Semagia");
            handler.startVariant();
            handler.startReifier();
            handler.topicRef(reifier);
            handler.endReifier();
            handler.value("variant", XSD.string);
            handler.itemIdentifier(variantIID);
            handler.startScope();
            handler.startTheme();
            handler.topicRef(theme);
            handler.endTheme();
            handler.endScope();
            handler.endVariant();
            handler.endName();
            handler.endTopic();
            self.fail('The topic "%s" reifies reifies a variant of another name which is not equal' % reifierIID)
        except mio.MIOException:
            pass

    def test_issue_35(self):
        # http://code.google.com/p/mappa/issues/detail?id=35
        assocType = mio.ITEM_IDENTIFIER, "http://test.semagia.com/assoc-type"
        roleType = mio.ITEM_IDENTIFIER, "http://test.semagia.com/role-type"
        rolePlayer = mio.ITEM_IDENTIFIER, "http://test.semagia.com/role-player"
        iid = "http://test.semagia.com/iid"
        handler = self._make_handler()
        handler.startTopicMap()
        handler.startAssociation()
        handler.itemIdentifier(iid)
        handler.startType()
        handler.topicRef(assocType)
        handler.endType()
        handler.startRole()
        handler.startType()
        handler.topicRef(roleType)
        handler.endType()
        handler.startPlayer()
        handler.topicRef(rolePlayer)
        handler.endPlayer()
        handler.endRole()
        handler.endAssociation()
        
        handler.startAssociation()
        handler.itemIdentifier(iid)
        handler.startType()
        handler.topicRef(assocType)
        handler.endType()
        handler.startRole()
        handler.startType()
        handler.topicRef(roleType)
        handler.endType()
        handler.startPlayer()
        handler.topicRef(rolePlayer)
        handler.endPlayer()
        handler.endRole()
        handler.endAssociation()
        handler.endTopicMap()
        self.assertEquals(1, len_(self._tm.associations))
        assoc = tuple(self._tm.associations)[0]
        tmc = self._tm.construct(iid=iid)
        self.assert_(tmc)
        self.assertEquals(assoc, tmc)

    def test_empty(self):
        handler = self._make_handler()
        self.assertEqual(0, len_(self._tm.topics))
        self.assertEqual(0, len_(self._tm.associations))
        handler.startTopicMap()
        handler.endTopicMap()
        self.assertEqual(0, len_(self._tm.topics))
        self.assertEqual(0, len_(self._tm.associations))

    def test_tm_reifier(self):
        handler = self._make_handler()
        iid = 'http://example.semagia.com/map/#1'
        self.assertEqual(0, len_(self._tm.topics))
        self.assertEqual(0, len_(self._tm.associations))
        handler.startTopicMap()
        handler.startReifier()
        handler.startTopic((mio.ITEM_IDENTIFIER, iid))
        handler.endTopic()
        handler.endReifier()
        handler.endTopicMap()
        self.assertEqual(1, len_(self._tm.topics))
        self.assertEqual(0, len_(self._tm.associations))
        topic = self._tm.topic(iid=iid)
        self.assert_(topic is not None)
        self.assert_(self._tm.reifier is not None)
        self.assertEqual(topic, self._tm.reifier)

    def test_tm_reifier2(self):
        handler = self._make_handler()
        iid = 'http://example.semagia.com/map/#1'
        self.assertEqual(0, len_(self._tm.topics))
        self.assertEqual(0, len_(self._tm.associations))
        handler.startTopicMap()
        handler.startReifier()
        handler.topicRef((mio.ITEM_IDENTIFIER, iid))
        handler.endReifier()
        handler.endTopicMap()
        self.assertEqual(1, len_(self._tm.topics))
        self.assertEqual(0, len_(self._tm.associations))
        topic = self._tm.topic(iid=iid)
        self.assert_(topic is not None)
        self.assert_(self._tm.reifier is not None)
        self.assertEqual(topic, self._tm.reifier)

    def test_topic_creation_sid(self):
        sid = 'http://psi.example.org/semagia'
        self.assertTrue(None is self._tm.topic(sid=sid))
        handler = self._make_handler()
        handler.startTopicMap()
        handler.topic((mio.SUBJECT_IDENTIFIER, sid))
        handler.endTopicMap()
        topic = self._tm.topic(sid=sid)
        self.assertFalse(topic is None)

    def test_topic_creation_slo(self):
        slo = 'http://www.semagia.com/'
        self.assertTrue(None is self._tm.topic(slo=slo))
        handler = self._make_handler()
        handler.startTopicMap()
        handler.topic((mio.SUBJECT_LOCATOR, slo))
        handler.endTopicMap()
        topic = self._tm.topic(slo=slo)
        self.assertFalse(topic is None)

    def test_topic_creation_iid(self):
        iid = 'http://www.semagia.com/something#x'
        self.assertTrue(None is self._tm.topic(iid=iid))
        handler = self._make_handler()
        handler.startTopicMap()
        handler.topic((mio.ITEM_IDENTIFIER, iid))
        handler.endTopicMap()
        topic = self._tm.topic(iid=iid)
        self.assertFalse(topic is None)

    def test_topic_type_instance(self):
        iid = 'http://www.semagia.com/something#x'
        iid2 = 'http://www.semagia.com/something#y'
        self.assertTrue(None is self._tm.topic(iid=iid))
        handler = self._make_handler()
        handler.startTopicMap()
        handler.startTopic((mio.ITEM_IDENTIFIER, iid))
        handler.isa((mio.ITEM_IDENTIFIER, iid2))
        handler.endTopic()
        handler.endTopicMap()
        topic = self._tm.topic(iid=iid)
        self.assertFalse(topic is None)
        topic2 = self._tm.topic(iid=iid2)
        self.assertFalse(topic2 is None)
        self.assert_(topic2 in topic.types)

    def test_type_instance_invalid(self):
        iid = 'http://www.semagia.com/something#x'
        handler = self._make_handler()
        handler.startTopicMap()
        handler.startAssociation()
        try:
            handler.isa((mio.ITEM_IDENTIFIER, iid))
            self.fail('startIsa is disallowed outside a topic context')
        except Exception:
            pass

    def test_association_creation(self):
        assoc_type = 'http://psi.example.org/assoc'
        role_type = 'http://psi.example.org/role-type'
        role_player = 'http://psi.example.org/role-player'
        for ident in (assoc_type, role_type, role_player):
            topic = self._tm.topic(ident)
            self.assertTrue(topic is None)
        handler = self._make_handler()
        handler.startTopicMap()
        handler.startAssociation((mio.SUBJECT_IDENTIFIER, assoc_type))
        handler.startRole((mio.SUBJECT_IDENTIFIER, role_type))
        handler.player((mio.SUBJECT_IDENTIFIER, role_player))
        handler.endRole()
        handler.endAssociation()
        handler.endTopicMap()
        for ident in (assoc_type, role_type, role_player):
            topic = self._tm.topic(ident)
            self.assertFalse(topic is None)
        self.assertEqual(1, len_(self._tm.associations))
        assoc = self._tm.associations.__iter__().next()
        self.assertFalse(assoc is None)
        self.assertEqual(1, len_(assoc))
        typ = self._tm.topic(sid=assoc_type)
        self.assert_(typ is not None)
        self.assertEqual(typ, assoc.type)
        r_typ = self._tm.topic(sid=role_type)
        player = self._tm.topic(sid=role_player)
        self.assert_(r_typ is not None)
        self.assert_(player is not None)
        for t, p in assoc.roles:
            self.assertEqual(r_typ, t)
            self.assertEqual(player, p)

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
        self.assertEqual(2, len_(self._tm.topics))
        topic = self._tm.topic(iid=iid1)
        self.assertEqual(1, len_(topic.occurrences))
        occ = topic.occurrences.__iter__().next()
        self.assertEqual('Semagia', occ.value)
        self.assertEqual(XSD.string, occ.datatype)
        typ = self._tm.topic(iid=iid2)
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
        self.assertEqual(2, len_(self._tm.topics))
        topic = self._tm.topic(iid=iid1)
        self.assertEqual(1, len_(topic.names))
        name = topic.names.__iter__().next()
        self.assertEqual('Semagia', name.value)
        typ = self._tm.topic(iid=iid2)
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
        self.assertEqual(2, len_(self._tm.topics))
        topic = self._tm.topic(iid=iid1)
        self.assertEqual(1, len_(topic.names))
        name = topic.names.__iter__().next()
        self.assertEqual('Semagia', name.value)
        self.assert_(TMDM.topic_name in name.type.sids)

    def test_name_invalid_value(self):
        iid1 = 'http://www.semagia.com/test#1'
        handler = self._make_handler()
        handler.startTopicMap()
        handler.startTopic((mio.ITEM_IDENTIFIER, iid1))
        handler.startName()
        try:
            handler.value('Semagia', XSD.string)
            self.fail('Datatype in a name-context is disallowed')
        except Exception:
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
        except Exception:
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
        self.assertEqual(3, len_(self._tm.topics))
        topic = self._tm.topic(iid=iid1)
        self.assertEqual(1, len_(topic.names))
        name = topic.names.__iter__().next()
        self.assertEqual('Semagia', name.value)
        self.assertEqual(1, len_(name.variants))
        var = name.variants.__iter__().next()
        self.assertEqual('semagia', var.value)
        self.assertEqual(XSD.string, var.datatype)
        theme = self._tm.topic(iid=iid3)
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
        except Exception:
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
        except Exception:
            pass

    def test_nested_topics(self):
        base = 'http://tinytim.sourceforge.net/test-nesting#'
        MAX = 1000
        handler = self._make_handler()
        iids = []
        handler.startTopicMap()
        for i in xrange(MAX):
            iid = base + str(i)
            iids.append(iid)
            handler.startTopic((mio.ITEM_IDENTIFIER, iid))
        for i in xrange(MAX):
            handler.endTopic()
        handler.endTopicMap()
        for iid in iids:
            self.assert_(self._tm.topic(iid=iid))


if __name__ == '__main__':
    import nose
    nose.core.runmodule()
