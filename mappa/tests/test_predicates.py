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
Tests the `predicates` module.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD License
"""
from . mappa_test import MappaTestCase
from mappa import predicates as pred

class TestPredicates(MappaTestCase):
    
    def test_reifier(self):
        t = self.create_topic()
        a = self.create_association(self.create_topic())
        self.assertEqual(None, pred.reifier(a))
        a.reifier = t
        self.assertEqual(t, pred.reifier(a))
        try:
            pred.reifier(t)
            self.fail('Topic has no reifier attribute')
        except Exception: # pylint: disable-msg=W0703
            pass

    def test_parent(self):
        t = self.create_topic()
        self.assertEqual(self._tm, pred.parent(t))
        n = t.create_name(type=self.create_topic(), value='Semagia')
        self.assertEqual(t, pred.parent(n))

    def test_player(self):
        a = self.create_association(self.create_topic())
        p1 = self.create_topic()
        p2 = self.create_topic()
        r1 = a.create_role(self.create_topic(), p1)
        r2 = a.create_role(self.create_topic(), p2)
        self.assertEqual(p1, pred.player(r1))
        self.assertEqual(p2, pred.player(r2))
        players = map(pred.player, a)
        self.assertEqual(2, len(players))
        self.assertTrue(p1 in players)
        self.assertTrue(p2 in players)

    def test_type(self):
        a = self.create_association(self.create_topic())
        t1 = self.create_topic()
        t2 = self.create_topic()
        r1 = a.create_role(player=self.create_topic(), type=t1)
        r2 = a.create_role(player=self.create_topic(), type=t2)
        self.assertEqual(t1, pred.type_(r1))
        self.assertEqual(t2, pred.type_(r2))
        types = map(pred.type_, a)
        self.assertEqual(2, len(types))
        self.assertTrue(t1 in types)
        self.assertTrue(t2 in types)

    def test_construct_id(self):
        def test_it(tmc):
            self.assertEqual(tmc.id, pred.cid(tmc))
        t = self.create_topic()
        test_it(t)
        a = self.create_association(self.create_topic())
        test_it(a)
        r = a.create_role(self.create_topic(), self.create_topic())
        test_it(r)
        o = t.create_occurrence(self.create_topic(), 'Semagia')
        test_it(o)
        n = t.create_name(self.create_topic(), 'Semagia')
        test_it(n)
        v = n.create_variant('Semagia', [self.create_topic()])
        test_it(v)
        try:
            pred.cid(object())
            self.fail('object() has no id attribute')
        except Exception: # pylint: disable-msg=W0703
            pass

if __name__ == '__main__':
    import nose
    nose.core.runmodule()
