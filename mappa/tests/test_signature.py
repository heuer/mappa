# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
Signature tests.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD License
"""
from . mappa_test import MappaTestCase

class TestSignature(MappaTestCase):

    def test_association_signature(self):
        typ = self.create_topic()
        a = self.create_association(typ)
        a2 = self.create_association(typ)
        self.assertEqual(a.__sig__(), a2.__sig__())
        role_type = self.create_topic()
        role_player = self.create_topic()
        a.create_role(role_type, role_player)
        self.assertNotEqual(a.__sig__(), a2.__sig__())
        a2.create_role(role_type, role_player)
        self.assertEqual(a.__sig__(), a2.__sig__())

    def test_occurrence_signature(self):
        t = self.create_topic()
        t2 = self.create_topic()
        typ = self.create_topic()
        o = t.create_occurrence(value='Semagia', type=typ)
        o2 = t2.create_occurrence(value='Semagia', type=typ)
        self.assertEqual(o.__sig__(), o2.__sig__())
        theme = self.create_topic()
        o.scope = [theme]
        self.assertNotEqual(o.__sig__(), o2.__sig__())
        o2.scope = [theme]
        self.assertEqual(o.__sig__(), o2.__sig__())
        o.scope = ()
        self.assertNotEqual(o.__sig__(), o2.__sig__())
        o2.scope = []
        self.assertEqual(o.__sig__(), o2.__sig__())
        o.value = 'Another value'
        self.assertNotEqual(o.__sig__(), o2.__sig__())

    def test_name_signature(self):
        t = self.create_topic()
        t2 = self.create_topic()
        typ = self.create_topic()
        n = t.create_name(value='Semagia', type=typ)
        n2 = t2.create_name(value='Semagia', type=typ)
        self.assertEqual(n.__sig__(), n2.__sig__())
        theme = self.create_topic()
        n.scope = [theme]
        self.assertNotEqual(n.__sig__(), n2.__sig__())
        n2.scope = [theme]
        self.assertEqual(n.__sig__(), n2.__sig__())
        # Duplicate theme
        n2.scope = [theme, theme]
        self.assertEqual(n.__sig__(), n2.__sig__())
        n.scope = ()
        self.assertNotEqual(n.__sig__(), n2.__sig__())
        n2.scope = ()
        self.assertEqual(n.__sig__(), n2.__sig__())
        n.value = 'Another value'
        self.assertNotEqual(n.__sig__(), n2.__sig__())
        n = t.create_name(value='Semagia_', type=typ, scope=[theme])
        n2 = t.create_name(value='Semagia_', type=typ, scope=[theme, theme])
        self.assertEqual(n.__sig__(), n2.__sig__())

    def test_variant_signature(self):
        t = self.create_topic()
        t2 = self.create_topic()
        n = t.create_name(value='Semagia Name', type=self.create_topic())
        n2 = t2.create_name(value='Semagia', type=self.create_topic())
        scope = [self.create_topic()]
        v = n.create_variant(value='Semagia', scope=scope)
        v2 = n2.create_variant(value='Semagia', scope=scope)
        self.assertEqual(v.__sig__(), v2.__sig__())
        theme = self.create_topic()
        v.scope = [theme]
        self.assertNotEqual(v.__sig__(), v2.__sig__())
        v2.scope = [theme]
        self.assertEqual(v.__sig__(), v2.__sig__())
        theme2 = self.create_topic()
        v.scope = [theme, theme2]
        self.assertNotEqual(v.__sig__(), v2.__sig__())
        v2.scope = (theme, theme2)
        self.assertEqual(v.__sig__(), v2.__sig__())
        v.value = 'Another value'
        self.assertNotEqual(v.__sig__(), v2.__sig__())


if __name__ == '__main__':
    import nose
    nose.core.runmodule()
