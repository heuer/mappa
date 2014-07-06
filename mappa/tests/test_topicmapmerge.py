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
Topic map merging tests.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD License
"""
from . mappa_test import MappaTestCase, len_

class TestTopicMapMerge(MappaTestCase):

    def setUp(self):
        super(TestTopicMapMerge, self).setUp()
        self._tm2 = self._conn.create('http://www.semagia.com/mappa/testtm2')

    def test_merge1(self):
        # Tests merging of topics by equal item identifiers.
        ref = 'http://mappa.semagia.com/loc'
        topicA = self._tm.create_topic(iid=ref)
        topicB = self._tm2.create_topic(iid=ref)
        self.assertEqual(1, len_(self._tm.topics))
        self.assertEqual(1, len_(self._tm2.topics))

        self._tm.merge(self._tm2)
        self.assertEqual(1, len_(self._tm.topics))
        self.assertEqual(topicA, self._tm.construct_by_iid(ref))

    def test_merge2(self):
        # Tests merging of topics by equal subject identifiers.
        ref = 'http://mappa.semagia.com/loc'
        topicA = self._tm.create_topic(sid=ref)
        topicB = self._tm2.create_topic(sid=ref)
        self.assertEqual(1, len_(self._tm.topics))
        self.assertEqual(1, len_(self._tm2.topics))

        self._tm.merge(self._tm2)
        self.assertEqual(1, len_(self._tm.topics))
        self.assertEqual(topicA, self._tm.topic_by_sid(ref))

    def test_merge3(self):
        # Tests merging of topics by equal subject locators.
        ref = 'http://mappa.semagia.com/loc'
        topicA = self._tm.create_topic(slo=ref)
        topicB = self._tm2.create_topic(slo=ref)
        self.assertEqual(1, len_(self._tm.topics))
        self.assertEqual(1, len_(self._tm2.topics))

        self._tm.merge(self._tm2)
        self.assertEqual(1, len_(self._tm.topics))
        self.assertEqual(topicA, self._tm.topic_by_slo(ref))

    def test_merge4(self):
        # Tests merging of topics by existing topic with item identifier equals
        # to a topic's subject identifier from the other map.
        ref = 'http://mappa.semagia.com/loc'
        topicA = self._tm.create_topic(iid=ref)
        topicB = self._tm2.create_topic(sid=ref)
        self.assertEqual(1, len_(self._tm.topics))
        self.assertEqual(1, len_(self._tm2.topics))

        self._tm.merge(self._tm2)
        self.assertEqual(1, len_(self._tm.topics))
        self.assertEqual(topicA, self._tm.topic_by_sid(ref))
        self.assertEqual(topicA, self._tm.topic_by_iid(ref))

    def test_merge5(self):
        # Tests merging of topics by existing topic with subject identifier equals
        # to a topic's item identifier from the other map.
        ref = 'http://mappa.semagia.com/loc'
        topicA = self._tm.create_topic(sid=ref)
        topicB = self._tm2.create_topic(iid=ref)
        self.assertEqual(1, len_(self._tm.topics))
        self.assertEqual(1, len_(self._tm2.topics))

        self._tm.merge(self._tm2)
        self.assertEqual(1, len_(self._tm.topics))
        self.assertEqual(topicA, self._tm.topic_by_sid(ref))
        self.assertEqual(topicA, self._tm.topic_by_iid(ref))

    def test_merge_type(self):
        ref = 'http://mappa.semagia.com/loc'
        type_ref = 'http://mappa.semagia.com/type'
        topicA = self._tm.create_topic(iid=ref)
        topicB = self._tm2.create_topic(sid=ref)
        topicB.add_type(self._tm2.create_topic(sid=type_ref))
        self.assert_(not self._tm.topic_by_sid(type_ref))
        self.assertEqual(1, len_(self._tm.topics))
        self.assertEqual(5, len_(self._tm2.topics))

        self._tm.merge(self._tm2)
        self.assertEqual(5, len_(self._tm.topics))
        self.assertEqual(topicA, self._tm.topic_by_sid(ref))
        self.assertEqual(topicA, self._tm.topic_by_iid(ref))
        type = self._tm.topic_by_sid(type_ref)
        self.assert_(type)
        self.assert_(type in self._tm.topic_by_sid(ref).types)

if __name__ == '__main__':
    import nose
    nose.core.runmodule()
