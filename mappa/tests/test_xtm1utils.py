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
#     * Neither the name 'Semagia' nor the name 'Mappa' nor the names of the
#       contributors may be used to endorse or promote products derived from 
#       this software without specific prior written permission.
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
