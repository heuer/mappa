# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
Tests datatyped constructs (occurrence, variant)

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD License
"""
from . mappa_test import MappaTestCase
from mappa import XSD

class TestDatatyped(MappaTestCase):

    def check(self, do):
        do.value = 1
        self.assertEqual(u'1', do.value)
        self.assertEqual(XSD.integer, do.datatype)
        self.assertEqual(1, int(do))
        self.assertEqual(1.0, float(do))
        self.assertEqual(1L, long(do))
        self.assertEqual('1', str(do))
        try:
            do.value = None
            self.fail('Setting value to None is not allowed (%r)' % do)
        except ValueError:
            pass
        do.value = '1', 'http://non.existing.datatype'
        self.assertEqual(u'1', do.value)
        self.assertEqual('http://non.existing.datatype', do.datatype)

    def test_occurrence(self):
        t = self.create_topic()
        occ = t.create_occurrence(type=self.create_topic(), value='Semagia')
        self.check(occ)

    def test_variant(self):
        n = self.create_name('Semagia')
        v = n.create_variant('semagia', (self.create_topic(), self.create_topic()))
        self.check(v)


if __name__ == '__main__':
    import nose
    nose.core.runmodule()
