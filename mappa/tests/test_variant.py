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
from mappa import UCS, ModelConstraintViolation

class TestVariant(MappaTestCase):

    def test_variant_illegal(self):
        name = self.create_name()
        self.assertEqual(0, len_(name.scope))
        try:
            variant = name.create_variant('value', [])
            self.fail('Creating a variant with no scope is illegal')
        except ModelConstraintViolation:
            pass
        theme = self.create_topic()
        name = self.create_topic().create_name(type=self.create_topic(),
                                               value='Semagia',
                                               scope=[theme])
        self.assert_(theme in name.scope)
        try:
            variant = name.create_variant('value', [theme])
            self.fail('The scope of the variant is equal to the name scope')
        except ModelConstraintViolation:
            pass
        
        theme2 = self.create_topic()
        # Create a legal variant
        variant = name.create_variant('value', [theme, theme2])
        self.assert_(variant)
        try:
            variant.scope = []
            self.fail('Setting the scope of the variant to UCS is illegal')
        except ModelConstraintViolation:
            self.assert_(theme in variant.scope)
            self.assert_(theme2 in variant.scope)
        try:
            variant.scope = [theme]
            self.fail("Setting the scope of the variant to the parent's scope is illegal")
        except ModelConstraintViolation:
            self.assert_(theme in variant.scope)
            self.assert_(theme2 in variant.scope)

    def test_variant_legal(self):
        theme = self.create_topic()
        name = self.create_topic().create_name(type=self.create_topic(),
                                               value='Semagia',
                                               scope=[theme])
        self.assert_(theme in name.scope)
        theme2 = self.create_topic()
        variant = name.create_variant('value', [theme2])
        self.assert_(theme in variant.scope)
        self.assert_(theme2 in variant.scope)
        self.assertEqual(2, len_(variant.scope))
        variant = name.create_variant('value', [theme, theme2])
        self.assert_(theme in variant.scope)
        self.assert_(theme2 in variant.scope)
        self.assertEqual(2, len_(variant.scope))
        theme3 = self.create_topic()
        name.scope = [theme, theme3]
        self.assert_(theme in variant.scope)
        self.assert_(theme2 in variant.scope)
        self.assert_(theme3 in variant.scope)
        self.assertEqual(3, len_(variant.scope))
        name.scope = UCS
        self.assertEqual(0, len_(name.scope))
        self.assertEqual(2, len_(variant.scope))
        
        variant2 = name.create_variant('value2', [theme2])
        self.assertEqual(1, len_(variant2.scope))
        self.assert_(theme2 in variant.scope)

if __name__ == '__main__':
    import nose
    nose.core.runmodule()
