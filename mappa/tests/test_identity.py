# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
Identity tests (item identifier, subject identifier, subject locator).

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD License
"""
from mappa_test import MappaTestCase, len_
from mappa import IdentityViolation

class TestIdentity(MappaTestCase):
    
    def test_iid(self):
        topic = self.create_topic()
        iid = self.random_locator()
        topic.add_iid(iid)
        self.assertEqual(topic, self._tm.topic(iid))
        self.assertEqual(topic, self._tm.topic(iid=iid))
        self.assertEqual(topic, self._tm.construct(iid))
        self.assertEqual(topic, self._tm.construct(iid=iid))
        topic2 = self.create_topic()
        try:
            topic2.add_iid(iid)
        except IdentityViolation, ex:
            self.assertEqual(topic2, ex.reporter)
            self.assertEqual(topic, ex.existing)
        self.assertEqual(1, len_(topic2.iids))
        
    def test_slo(self):
        topic = self.create_topic()
        slo = self.random_locator()
        topic.add_slo(slo)
        self.assertEqual(topic, self._tm.topic(slo=slo))
        topic2 = self.create_topic()
        try:
            topic2.add_slo(slo)
        except IdentityViolation, ex:
            self.assertEqual(topic2, ex.reporter)
            self.assertEqual(topic, ex.existing)
        self.assertEqual(0, len_(topic2.sids))
        
    def test_sid(self):
        topic = self.create_topic()
        sid = self.random_locator()
        topic.add_sid(sid)
        self.assertEqual(topic, self._tm.topic(sid=sid))
        topic2 = self.create_topic()
        try:
            topic2.add_sid(sid)
        except IdentityViolation, ex:
            self.assertEqual(topic2, ex.reporter)
            self.assertEqual(topic, ex.existing)
        self.assertEqual(0, len_(topic2.sids))
        
    def test_sid_iid(self):
        topic = self.create_topic()
        sid = self.random_locator()
        topic.add_sid(sid)
        self.assertEqual(topic, self._tm.topic(sid=sid))
        topic2 = self.create_topic()
        self.assertEqual(1, len_(topic2.iids))
        try:
            topic2.add_iid(sid)
        except IdentityViolation, ex:
            self.assertEqual(topic2, ex.reporter)
            self.assertEqual(topic, ex.existing)
        self.assertEqual(1, len_(topic2.iids))
        
    def test_sid_iid2(self):
        # A Topic Maps construct != topic may have an item identifier that
        # is equal with a subject identifier
        assoc = self.create_association()
        topic = self.create_topic()
        loc = self.random_locator()
        topic.add_sid(loc)
        self.assertEqual(topic, self._tm.topic(sid=loc))
        assoc.add_iid(loc)
        self.assertEqual(1, len_(assoc.iids))
        self.assertEqual(assoc, self._tm.construct(iid=loc))
        
        loc2 = self.random_locator()
        assoc.add_iid(loc2)
        self.assertEqual(2, len_(assoc.iids))
        self.assertEqual(assoc, self._tm.construct(iid=loc2))
        
        topic.add_sid(loc2)
        self.assertEqual(topic, self._tm.topic(sid=loc2))

if __name__ == '__main__':
    import nose
    nose.core.runmodule()
