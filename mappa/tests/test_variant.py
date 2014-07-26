# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
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
