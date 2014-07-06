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
Tests scoped constructs (association, occurrence, name, variant)

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD License
"""
from . mappa_test import MappaTestCase, len_
from mappa import ModelConstraintViolation

class TestScoped(MappaTestCase):

    def scoped_check(self, scoped):
        self.assertEqual(0, len_(scoped.scope))
        theme = self.create_topic()
        # Assign a singleton theme
        scoped.scope = theme
        self.assertEqual(1, len_(scoped.scope))
        self.assertTrue(theme in scoped.scope)
        # Set to UCS
        scoped.scope = []
        self.assertEqual(0, len_(scoped.scope))
        self.assertFalse(theme in scoped.scope)
        # Assign an iterable
        scoped.scope = [theme]
        self.assertEqual(1, len_(scoped.scope))
        self.assertTrue(theme in scoped.scope)
        # Set back to UCS
        scoped.scope = ()
        self.assertEqual(0, len_(scoped.scope))
        self.assertFalse(theme in scoped.scope)
        try:
            scoped.scope = None
            self.fail('Setting scope to None is not allowed (%r)' % scoped)
        except ValueError:
            pass
        tm2 = self.create_map()
        try:
            scoped.scope = [self.create_topic(tm2)]
            self.fail('Using a theme from another topic map is not allowed. (%r)' % scoped)
        except ModelConstraintViolation:
            pass

    def test_assoc(self):
        a = self.create_association(self.create_topic())
        self.scoped_check(a)

    def test_occurrence(self):
        t = self.create_topic()
        occ = t.create_occurrence(self.create_topic(), 'Semagia')
        self.scoped_check(occ)

    def test_name(self):
        t = self.create_topic()
        n = t.create_name(value='Semagia', type=self.create_topic())
        self.scoped_check(n)

    def test_variant(self):
        t = self.create_topic()
        n = t.create_name(value='Semagia', type=self.create_topic())
        v_theme = self.create_topic()
        v_theme2 = self.create_topic()
        v = n.create_variant(value='semagia', scope=(v_theme, v_theme2))
        self.assertEqual(2, len_(v.scope))
        self.assertTrue(v_theme in v.scope)
        self.assertTrue(v_theme2 in v.scope)
        
        n_theme = self.create_topic()
        n.scope = [n_theme]
        self.assertEqual(1, len_(n.scope))
        self.assertTrue(n_theme in n.scope)
        
        self.assertEqual(3, len_(v.scope))
        self.assertTrue(v_theme in v.scope)
        self.assertTrue(v_theme2 in v.scope)
        self.assertTrue(n_theme in v.scope)
        
        n.scope = []
        self.assertEqual(2, len_(v.scope))
        self.assertTrue(v_theme in v.scope)
        self.assertTrue(v_theme2 in v.scope)
        self.assertFalse(n_theme in v.scope)
        

if __name__ == '__main__':
    import nose
    nose.core.runmodule()
