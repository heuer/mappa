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
