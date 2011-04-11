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
Tests against the topic map impl.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD License
"""
from . mappa_test import MappaTestCase, len_

class TestTopicMap(MappaTestCase):

    def test_anon_topic(self):
        for i in xrange(5):
            t = self._tm.create_topic()
            self.assertEqual(1, len_(t.iids))

    def test_topic_creation_sid_iid(self):
        loc = 'http://www.semagia.com/mymap#test'
        t = self._tm.create_topic(sid=loc)
        self.assert_(loc in t.sids)
        t2 = self._tm.create_topic(iid=loc)
        self.assert_(loc in t2.iids)
        self.assertEqual(t, t2)

    def test_topic_creation_sid(self):
        loc = 'http://www.semagia.com/mymap#test'
        t = self._tm.create_topic(sid=loc)
        self.assert_(loc in t.sids)
        t2 = self._tm.create_topic(sid=loc)
        self.assert_(loc in t2.sids)
        self.assertEqual(t, t2)

    def test_topic_creation_sid2(self):
        loc = 'http://www.semagia.com/mymap#test'
        t = self._tm.create_topic_by_sid(loc)
        self.assert_(loc in t.sids)
        t2 = self._tm.create_topic_by_sid(loc)
        self.assert_(loc in t2.sids)
        self.assertEqual(t, t2)

    def test_topic_creation_iid(self):
        loc = 'http://www.semagia.com/mymap#test'
        t = self._tm.create_topic(iid=loc)
        self.assert_(loc in t.iids)
        t2 = self._tm.create_topic(iid=loc)
        self.assert_(loc in t2.iids)
        self.assertEqual(t, t2)

    def test_topic_creation_iid2(self):
        loc = 'http://www.semagia.com/mymap#test'
        t = self._tm.create_topic_by_iid(loc)
        self.assert_(loc in t.iids)
        t2 = self._tm.create_topic_by_iid(loc)
        self.assert_(loc in t2.iids)
        self.assertEqual(t, t2)

    def test_topic_creation_iid_sid(self):
        loc = 'http://www.semagia.com/mymap#test'
        t = self._tm.create_topic(iid=loc)
        self.assert_(loc in t.iids)
        t2 = self._tm.create_topic(sid=loc)
        self.assert_(loc in t2.sids)
        self.assertEqual(t, t2)

    def test_topic_creation_slo(self):
        loc = 'http://www.semagia.com/mymap#test'
        t = self._tm.create_topic(slo=loc)
        self.assert_(loc in t.slos)
        t2 = self._tm.create_topic(slo=loc)
        self.assert_(loc in t2.slos)
        self.assertEqual(t, t2)

    def test_topic_creation_slo2(self):
        loc = 'http://www.semagia.com/mymap#test'
        t = self._tm.create_topic_by_slo(loc)
        self.assert_(loc in t.slos)
        t2 = self._tm.create_topic_by_slo(loc)
        self.assert_(loc in t2.slos)
        self.assertEqual(t, t2)

    def test_sid(self):
        loc = self.random_locator()
        t = self.create_topic()
        t.add_sid(loc)
        self.assertEqual(t, self._tm.topic(sid=loc))
        self.assertEqual(t, self._tm.topic(loc))
        self.assertTrue(None is self._tm.topic(sid=self.random_locator()))

    def test_slo(self):
        loc = self.random_locator()
        t = self.create_topic()
        t.add_slo(loc)
        self.assertEqual(t, self._tm.topic(slo=loc))
        self.assertTrue(None is self._tm.topic(sid=self.random_locator()))
        self.assertEqual(t, self._tm.topic('= ' + loc))

    def test_iid(self):
        loc = self.random_locator()
        t = self.create_topic()
        t.add_iid(loc)
        self.assertEqual(t, self._tm.topic(iid=loc))
        self.assertTrue(None is self._tm.topic(iid=self.random_locator()))
        self.assertEqual(t, self._tm.topic(loc))

    def test_sid_or_iid(self):
        base = 'http://www.semagia.com/test/'
        tm = self.create_map(base)
        frag = 'sid_or_iid'
        loc = base + '#' + frag
        t = self.create_topic(tm)
        t.add_iid(loc)
        self.assertEqual(None, tm.topic(sid=loc))
        self.assertEqual(t, tm.topic(iid=loc))
        self.assertEqual(t, tm.topic(loc))

    def test_removed_contains_magic(self):
        # Removed the ITopicMap.__contains__ magic
        # This test tests if it is gone from all backends
        t = self.create_topic()
        try:
            t in self._tm
            self.fail('Remove the __contains__ magic from the topic map!')
        except TypeError:
            pass
        try:
            'http://www.semagia.com/' in self._tm
            self.fail('Remove the __contains__ magic from the topic map!')
        except TypeError:
            pass

    def test_construct(self):
        def _construct_by_id(obj):
            self.assertEqual(obj, self._tm.construct(id=obj.id))
        
        def _construct_by_iid(obj):
            loc = self.random_locator()
            obj.add_iid(loc)
            self.assertEqual(obj, self._tm.construct(loc))
            self.assertEqual(obj, self._tm.construct(iid=loc))
        
        t = self.create_topic()
        _construct_by_id(t)
        _construct_by_iid(t)
        
        a = self.create_association(self.create_topic())
        r = a.create_role(self.create_topic(), self.create_topic())
        _construct_by_id(a)
        _construct_by_iid(a)
        _construct_by_id(r)
        _construct_by_iid(a)
        
        o = t.create_occurrence(value='Semagia', type=self.create_topic())
        _construct_by_id(o)
        _construct_by_iid(o)
        
        n = t.create_name(value='Semagia', type=self.create_topic())
        _construct_by_id(n)
        _construct_by_iid(n)
        
        v = n.create_variant('Semagia', (self.create_topic(), self.create_topic()))
        _construct_by_id(v)
        _construct_by_iid(v)

        _construct_by_id(self._tm)
        _construct_by_iid(self._tm)


if __name__ == '__main__':
    import nose
    nose.core.runmodule()
