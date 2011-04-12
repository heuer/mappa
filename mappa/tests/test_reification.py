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
Tests reification of Topic Maps constructs.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD License
"""
from . mappa_test import MappaTestCase
from mappa import ModelConstraintViolation

class TestReification(MappaTestCase):

    def reification_check(self, reifiable):
        self.assert_(reifiable.reifier is None)
        t = self.create_topic()
        reifiable.reifier = t
        self.assert_(reifiable.reifier == t and t.reified == reifiable)
        reifiable.reifier = t
        t2 = self.create_topic()
        reifiable.reifier = t2
        self.assert_(reifiable.reifier == t2)
        reifiable.reifier = None
        self.assert_(reifiable.reifier is None)
        self.assert_(t.reified is None)
        reifiable.reifier = t
        self.assert_(reifiable.reifier == t and t.reified == reifiable)

    def reification_collision_check(self, reifiable):
        def _make_reifiable():
            return self._tm.create_association(self.create_topic())
        reifier = self.create_topic()
        reifiable2 = _make_reifiable()
        reifiable2.reifier = reifier
        self.assertEqual(reifier, reifiable2.reifier)
        self.assert_(None is reifiable.reifier)
        try:
            reifiable.reifier = reifier
            self.fail('The reifier reifies another construct')
        except ModelConstraintViolation:
            pass

    def test_topicmap(self):
        self.reification_check(self._tm)

    def test_topicmap_collision(self):
        self.reification_collision_check(self._tm)

    def test_assoc(self):
        a = self.create_association()
        self.reification_check(a)

    def test_assoc_collision(self):
        a = self.create_association()
        self.reification_collision_check(a)

    def test_role(self):
        a = self.create_association(self.create_topic())
        r = a.create_role(self.create_topic(), self.create_topic())
        self.reification_check(r)

    def test_role_collision(self):
        a = self.create_association(self.create_topic())
        r = a.create_role(self.create_topic(), self.create_topic())
        self.reification_collision_check(r)

    def test_occurrence(self):
        t = self.create_topic()
        occ = t.create_occurrence(value='Semagia', type=self.create_topic())
        self.reification_check(occ)

    def test_occurrence_collision(self):
        t = self.create_topic()
        occ = t.create_occurrence(value='Semagia', type=self.create_topic())
        self.reification_collision_check(occ)

    def test_name(self):
        t = self.create_topic()
        n = t.create_name(value='Semagia', type=self.create_topic())
        self.reification_check(n)

    def test_name_collision(self):
        t = self.create_topic()
        n = t.create_name(value='Semagia', type=self.create_topic())
        self.reification_collision_check(n)

    def test_variant(self):
        t = self.create_topic()
        n = t.create_name(value='Semagia', type=self.create_topic())
        v = n.create_variant(value='Semagia', scope=(self.create_topic(), self.create_topic()))
        self.reification_check(v)

    def test_variant_collision(self):
        t = self.create_topic()
        n = t.create_name(value='Semagia', type=self.create_topic())
        v = n.create_variant(value='Semagia', scope=(self.create_topic(), self.create_topic()))
        self.reification_collision_check(v)

if __name__ == '__main__':
    import nose
    nose.core.runmodule()
