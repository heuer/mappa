# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
Tests typed constructs (association, role, occurrence, name)

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD License
"""
from . mappa_test import MappaTestCase
from mappa import ModelConstraintViolation

# Remove warning about redefintion of 'type'
# pylint: disable-msg=W0622

class TestTyped(MappaTestCase):

    def typed_check(self, typed):
        type = self.create_topic()
        typed.type = type
        self.assertEqual(type, typed.type)
        try:
            typed.type = None
            self.fail('Setting type to None is not allowed (%r)' % typed)
        except ValueError:
            pass
        
        tm2 = self.create_map()
        try:
            typed.type = self.create_topic(tm2)
            self.fail('Using a type from another topic map is not allowed. (%r)' % typed)
        except ModelConstraintViolation:
            pass

    def test_assoc(self):
        a = self.create_association(self.create_topic())
        self.typed_check(a)

    def test_role(self):
        a = self.create_association(self.create_topic())
        r = a.create_role(self.create_topic(), self.create_topic())
        self.typed_check(r)

    def test_occurrence(self):
        t = self.create_topic()
        occ = t.create_occurrence(self.create_topic(), 'Semagia')
        self.typed_check(occ)

    def test_name(self):
        t = self.create_topic()
        n = t.create_name(value='Semagia', type=self.create_topic())
        self.typed_check(n)


if __name__ == '__main__':
    import nose
    nose.core.runmodule()
