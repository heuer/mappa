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
Tests against names.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD License
"""
from . mappa_test import MappaTestCase, len_
from mappa import TMDM, XSD

class TestName(MappaTestCase):

    def test_variant_creation(self):
        t = self.create_topic()
        self.assertEqual(0, len_(t.names))
        t['- name'] = 'Semagia'
        self.assertEqual(1, len_(t.names))
        name = tuple(t.names)[0]
        name_type = self._tm.topic(iid=self._tm.iri + '#' + 'name')
        
        self.assertEqual(0, len_(name.variants))
        v_theme, v_theme2 = self.create_topic(), self.create_topic()
        v = name.create_variant(2, (v_theme, v_theme2))
        self.assertEqual('2', v.value)
        self.assertEqual(XSD.integer, v.datatype)
        self.assertEqual(1, len_(name.variants))
        self.assertEqual(name, v.parent)
        self.assertEqual(2, len_(v.scope))
        self.assert_(v_theme in v.scope)
        self.assert_(v_theme2 in v.scope)
        n_theme = self.create_topic()
        name.scope = [n_theme]
        self.assert_(n_theme in name.scope)
        # name_theme must be part of the variants scope
        self.assert_(n_theme in v.scope)

    def test_name_creation_with_scope(self):
        t = self.create_topic()
        self.assertEqual(0, len_(t.names))
        t['- name @de'] = 'Semagia'
        self.assertEqual(1, len_(t.names))
        name = tuple(t.names)[0]
        name_type = self._tm.topic(iid=self._tm.iri + '#' + 'name')
        self.assertTrue(name_type is not None)
        self.assertEqual('Semagia', name.value)
        self.assertEqual(name_type, name.type)
        
        self.assertEqual(name, tuple(t['- name'])[0])
        self.assertEqual(name, tuple(t['* name'])[0])
        self.assertEqual(name, tuple(t / 'name')[0])
        self.assertEqual(name, tuple(t / name_type)[0])
        self.assertEqual(1, len_(t['- name @de']))
        self.assertEqual(1, len_(t['* name @de']))
        self.assertEqual(name, tuple(t['- name @de'])[0])
        self.assertEqual(name, tuple(t['* name @de'])[0])
        self.assertEqual(0, len_(t['- name @en']))
        self.assertEqual(0, len_(t['* name @en']))
        self.assertEqual(0, len_(t['- xxx']))
        self.assertEqual(0, len_(t['* xxx']))
        
        t['-name @de en'] = 'Semagia'
        self.assertEqual(1, len_(t['- name @de']))
        self.assertEqual(1, len_(t['* name @de']))
        self.assertEqual(1, len_(t['- name @de en']))
        self.assertEqual(1, len_(t['* name @de en']))
        self.assertEqual(0, len_(t['- name @de en es']))
        self.assertEqual(0, len_(t['* name @de en es']))
        

    def test_name_creation_default_type(self):
        t = self.create_topic()
        self.assertEqual(0, len_(t.names))
        t['-'] = 'Semagia'
        self.assertEqual(1, len_(t.names))
        name = tuple(t.names)[0]
        self.assertEqual('Semagia', name.value)        
        self.assertTrue(TMDM.topic_name in name.type.sids)


if __name__ == '__main__':
    import nose
    nose.core.runmodule()
