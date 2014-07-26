# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
Tests the XTM 1.0 utility module.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD License
"""
from . mappa_test import MappaTestCase, len_
from mappa import ModelConstraintViolation, xtm1utils

class TestXTM10Utils(MappaTestCase):
    
    def test_convert_reification(self):
        loc = 'http://www.semagia.com/somemap#reification'
        topic = self.create_topic(sid=loc)
        topic2 = self.create_topic()
        occ = topic2.create_occurrence(value='Semagia', type=self.create_topic())
        occ.add_iid(loc)
        self.assertTrue(loc in topic.sids)
        self.assertTrue(loc in occ.iids)
        self.assertTrue(occ.reifier is None)
        xtm1utils.convert_reification(self._tm)
        self.assertFalse(occ.reifier is None)
        self.assertEqual(occ.reifier, topic)
        self.assertFalse(loc in topic.sids)
        self.assertFalse(loc in occ.iids)
        
    def test_convert_reification_remove_sid(self):
        loc = 'http://www.semagia.com/somemap#reification'
        topic = self.create_topic(sid=loc)
        topic2 = self.create_topic()
        occ = topic2.create_occurrence(value='Semagia', type=self.create_topic())
        occ.add_iid(loc)
        self.assertTrue(loc in topic.sids)
        self.assertTrue(loc in occ.iids)
        self.assertTrue(occ.reifier is None)
        xtm1utils.convert_reification(self._tm, remove_sid=True, remove_iid=False)
        self.assertFalse(occ.reifier is None)
        self.assertEqual(occ.reifier, topic)
        self.assertTrue(loc not in topic.sids)
        self.assertTrue(loc in occ.iids)
        
    def test_convert_reification_remove_iid(self):
        loc = 'http://www.semagia.com/somemap#reification'
        topic = self.create_topic(sid=loc)
        topic2 = self.create_topic()
        occ = topic2.create_occurrence(value='Semagia', type=self.create_topic())
        occ.add_iid(loc)
        self.assertTrue(loc in topic.sids)
        self.assertTrue(loc in occ.iids)
        self.assertTrue(occ.reifier is None)
        xtm1utils.convert_reification(self._tm, remove_sid=False, remove_iid=True)
        self.assertFalse(occ.reifier is None)
        self.assertEqual(occ.reifier, topic)
        self.assertTrue(loc in topic.sids)
        self.assertTrue(loc not in occ.iids)
        
    def test_convert_reification_merge(self):
        loc = 'http://www.semagia.com/somemap#reification1'
        loc2 = 'http://www.semagia.com/somemap#reification2'
        topic = self.create_topic(sid=loc)
        topic2 = self.create_topic()
        topic3 = self.create_topic(sid=loc2)
        occ = topic2.create_occurrence(value='Semagia', type=self.create_topic())
        occ.add_iid(loc)
        occ.add_iid(loc2)
        self.assertTrue(loc in topic.sids)
        self.assertTrue(loc2 in topic3.sids)
        self.assertTrue(loc in occ.iids)
        self.assertTrue(loc2 in occ.iids)
        self.assertTrue(occ.reifier is None)
        self.assertEqual(4, len_(self._tm.topics))
        self.assertNotEqual(self._tm.topic(sid=loc), self._tm.topic(sid=loc2))
        xtm1utils.convert_reification(self._tm)
        self.assertEqual(3, len_(self._tm.topics))
        self.assertEqual(self._tm.topic(sid=loc), self._tm.topic(sid=loc2))
        
    def test_convert_reification_invalid(self):
        loc = 'http://www.semagia.com/somemap#reification1'
        loc2 = 'http://www.semagia.com/somemap#reification2'
        topic = self.create_topic(sid=loc)
        topic.add_sid(loc2)
        topic2 = self.create_topic()
        topic3 = self.create_topic()
        occ = topic2.create_occurrence(value='Semagia', type=self.create_topic())
        occ.add_iid(loc)
        name = topic3.create_name(value='Semagia', type=self.create_topic())
        name.add_iid(loc2)
        self.assertTrue(loc in topic.sids)
        self.assertTrue(loc2 in topic.sids)
        self.assertTrue(loc in occ.iids)
        self.assertTrue(loc2 in name.iids)
        self.assertTrue(occ.reifier is None)
        self.assertTrue(name.reifier is None)
        try:
            xtm1utils.convert_reification(self._tm)
            self.fail('The topic reifies two different Topic Maps constructs, must fail')
        except ModelConstraintViolation:
            pass
        
if __name__ == '__main__':
    import nose
    nose.core.runmodule()
