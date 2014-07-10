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


:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD License
"""
from .mappa_test import MappaTestCase
from mappa.utils import atomify
from mappa import TMDM, XSD

class TestAtomification(MappaTestCase):

    def test_simple_topic_atomification(self):
        t = self.create_topic()
        t['-'] = 'Semagia'
        t['- name'] = 'Another name'
        self.assertEqual('Semagia', atomify(t))

    def test_name_atomification(self):
        n = self.create_name('Semagia')
        self.assertEqual('Semagia', atomify(n))

    def test_occurrence_atomification(self):
        t = self.create_topic()
        o = t.create_occurrence(type=self.create_topic(), value=('Semagia', XSD.string))
        self.assertEqual('Semagia', atomify(o))

    def test_variant_atomification(self):
        n = self.create_name('Semagia')
        v = n.create_variant(value=('Semagia', XSD.string), scope=[self.create_topic()])
        self.assertEqual('Semagia', atomify(v))

    def test_contextaware_topic_atomification(self):
        t = self.create_topic()
        default_type = self.create_topic(sid=TMDM.topic_name)
        scope = (self.create_topic(), self.create_topic())
        n = t.create_name(type=self.create_topic(), value='scoped-random-type', scope=scope)
        n2 = t.create_name(type=default_type, value='scoped-default-type', scope=scope)
        t['-'] = 'Semagia'
        self.assertEqual('scoped-default-type', atomify(t, scope))
        n2.scope = [scope[0]]
        self.assertEqual('scoped-random-type', atomify(t, scope))
        n.scope = [scope[0]]
        self.assertEqual('Semagia', atomify(t, scope))
        
    def test_nice_iid(self):
        iid = '%s#%s' % (self._tm.iri, 'nice-iid')
        t = self.create_topic(iid=iid)
        self.assertEqual('nice-iid', atomify(t))
        
    def test_nice_iid2(self):
        iid = '%s#%s' % (self._tm.iri, '238923')
        t = self.create_topic(iid=iid)
        t.add_iid('%s#%s' % (self._tm.iri, 'nice-iid'))
        self.assertEqual('nice-iid', atomify(t))
        
    def test_nice_iid_slash(self):
        iid = '%s%s' % (self._tm.iri, '238923')
        t = self.create_topic(iid=iid)
        t.add_iid('%s%s' % (self._tm.iri, 'nice-iid'))
        self.assertEqual('nice-iid', atomify(t))
        
    def test_nice_sid(self):
        sid = '%s#%s' % (self._tm.iri, 'nice-sid')
        t = self.create_topic(sid=sid)
        self.assertEqual('nice-sid', atomify(t))
        
    def test_nice_sid2(self):
        sid = '%s#%s' % (self._tm.iri, '238923')
        t = self.create_topic(sid=sid)
        t.add_sid('%s#%s' % (self._tm.iri, 'nice-sid'))
        self.assertEqual('nice-sid', atomify(t))
        
    def test_nice_sid_slash(self):
        sid = '%s%s' % (self._tm.iri, '238923')
        t = self.create_topic(sid=sid)
        t.add_sid('%s%s' % (self._tm.iri, 'nice-sid'))
        self.assertEqual('nice-sid', atomify(t))

if __name__ == '__main__':
    import nose
    nose.core.runmodule()
