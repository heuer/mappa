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
Topic merging tests.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD License
"""
from . mappa_test import MappaTestCase, len_
from mappa import TMDM, ModelConstraintViolation

class TestTopicMerge(MappaTestCase):

    def test_reified(self):
        t = self.create_topic()
        t2 = self.create_topic()
        a = self.create_association(self.create_topic())
        a2 = self.create_association(self.create_topic())
        a.reifier = t
        a2.reifier = t2
        self.assertEqual(t, a.reifier)
        self.assertEqual(t2, a2.reifier)
        self.assertEqual(a, t.reified)
        self.assertEqual(a2, t2.reified)
        try:
            t.merge(t2)
            self.fail('Topics with different reified constructs cannot be merged')
        except ModelConstraintViolation:
            pass
        
    def test_role_playing(self):
        t = self.create_topic()
        t2 = self.create_topic()
        a = self.create_association(self.create_topic())
        role = a.create_role(self.create_topic(), t2)
        self.assertEqual(4, len_(self._tm.topics))
        self.assertTrue(role not in t.roles_played)
        self.assertTrue(role in t2.roles_played)
        t.merge(t2)
        self.assertEqual(3, len_(self._tm.topics))
        self.assertTrue(role in t.roles_played)

    def test_topicmerge(self):
        t = self.create_topic()
        iid = self.random_locator()
        t.add_iid(iid)
        
        t2 = self.create_topic()
        sid = self.random_locator()
        t2.add_sid(sid)

        self.assert_(sid in t2.sids)
        self.assert_(sid not in t.sids)
        
        t.merge(t2)
        
        self.assertEqual(1, len_(self._tm.topics))
        self.assert_(sid in t.sids)
        self.assert_(iid in t.iids)
        
    def test_duplicatesupression(self):
        t = self.create_topic()
        t['-name'] = 'Semagia'
        t2 = self.create_topic()
        t2['-name'] = 'Semagia'
        t2['-name'] = 'something'
        t.merge(t2)
        self.assertEqual(2, len_(t.names))

    def test_duplicatesupression_variant(self):
        t = self.create_topic()
        name_type = self._tm.create_topic(sid=TMDM.topic_name)
        theme = self.create_topic()
        n1 = t.create_name(type=name_type, value='Semagia')
        v1 = n1.create_variant(value='semagia', scope=[theme])
        t2 = self.create_topic()
        n2 = t2.create_name(type=name_type, value='Semagia')
        v2 = n2.create_variant(value='semagia', scope=[theme])
        t.merge(t2)
        self.assertEqual(1, len_(t.names))
        name = tuple(t.names)[0]
        self.assertEqual(1, len_(name.variants))
        
    def test_reifier_merge(self):
        # Tests if the reifiers of equal names get merged
        t = self.create_topic()
        t2 = self.create_topic()
        name_type = self.create_topic()
        n = t.create_name(name_type, 'Semagia')
        n2 = t2.create_name(name_type, 'Semagia')
        n_reifier = self.create_topic()
        n2_reifier = self.create_topic()
        n_reifier_iid = 'http://www.semagia.com/reifier1'
        n2_reifier_iid = 'http://www.semagia.com/reifier2'
        n_reifier.add_iid(n_reifier_iid)
        n2_reifier.add_iid(n2_reifier_iid)
        n.reifier = n_reifier
        n2.reifier = n2_reifier
        self.assertEqual(1, len_(t.names))
        self.assertEqual(1, len_(t2.names))
        self.assertEqual(5, len_(self._tm.topics))
        self.assertTrue(n_reifier_iid in n.reifier.iids)
        self.assertTrue(n2_reifier_iid not in n.reifier.iids)
        self.assertTrue(n2_reifier_iid in n2.reifier.iids)
        self.assertTrue(n_reifier_iid not in n2.reifier.iids)
        self.assertNotEqual(n.reifier, n2.reifier)
        t.merge(t2)
        self.assertEqual(3, len_(self._tm.topics))
        self.assertEqual(1, len_(t.names))
        name = tuple(t.names)[0]
        self.assertTrue(n_reifier_iid in name.reifier.iids)
        self.assertTrue(n2_reifier_iid in name.reifier.iids)
        
    def test_type_scope_replacement(self):
        t = self.create_topic()
        t2 = self.create_topic()
        t3 = self.create_topic()
        n = t3.create_name(type=t2, scope=(t2,), value='Semagia')
        self.assertEqual(t2, n.type)
        self.assertTrue(t2 in n.scope)
        self.assertTrue(t not in n.scope)
        t.merge(t2)
        n = tuple(t3.names)[0]
        self.assertEqual(t, n.type)
        self.assertTrue(t in n.scope)

if __name__ == '__main__':
    import nose
    nose.core.runmodule()
