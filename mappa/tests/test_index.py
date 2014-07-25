# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
Tests against indices.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD License
"""
import unittest
from . mappa_test import MappaTestCase, len_

class TestTypeInstanceIndex(MappaTestCase):

    def test_type_instance(self):
        idx = self._tm.index.type_instance
        self.assert_(idx)
        a_type = self.create_topic()
        self.assertEqual(0, len_(idx.associations(a_type)))
        a = self.create_association(a_type)
        self.assertEqual(1, len_(idx.associations(a_type)))
        self.assert_(a in idx.associations(a_type))

    def test_type_instance_add_remove(self):
        idx = self._tm.index.type_instance
        t = self.create_topic()
        o_type = self.create_topic()
        n_type = self.create_topic()
        self.assertEqual(0, len_(idx.occurrences(o_type)))
        self.assertEqual(0, len_(idx.names(n_type)))
        o = t.create_occurrence(o_type, 'Semagia')
        n = t.create_name(n_type, 'Semagia')
        self.assertEqual(1, len_(idx.occurrences(o_type)))
        self.assertTrue(o in idx.occurrences(o_type))
        self.assertEqual(1, len_(idx.names(n_type)))
        self.assertTrue(n in idx.names(n_type))
        
        # Detach t
        self._tm.remove_topic(t)
        self.assertEqual(0, len_(idx.occurrences(o_type)))
        self.assertEqual(0, len_(idx.names(n_type)))

        # Attach t
        self._tm.add_topic(t)
        self.assertEqual(1, len_(idx.occurrences(o_type)))
        self.assertTrue(o in idx.occurrences(o_type))
        self.assertEqual(1, len_(idx.names(n_type)))
        self.assertTrue(n in idx.names(n_type))
        
        a_type = self.create_topic()
        r_type = self.create_topic()
        self.assertEqual(0, len_(idx.associations(a_type)))
        self.assertEqual(0, len_(idx.roles(r_type)))
        a = self.create_association(a_type)
        self.assertEqual(1, len_(idx.associations(a_type)))
        self.assertTrue(a in idx.associations(a_type))
        self.assertEqual(0, len_(idx.roles(r_type)))
        
        r = a.create_role(r_type, self.create_topic())
        self.assertEqual(1, len_(idx.roles(r_type)))
        self.assertTrue(r in idx.roles(r_type))
        
        # Detach a
        self._tm.remove_association(a)
        self.assertEqual(0, len_(idx.associations(a_type)))
        self.assertEqual(0, len_(idx.roles(r_type)))
        
        # Attach a
        self._tm.add_association(a)
        self.assertEqual(1, len_(idx.associations(a_type)))
        self.assertTrue(a in idx.associations(a_type))
        self.assertEqual(1, len_(idx.roles(r_type)))
        self.assertTrue(r in idx.roles(r_type))


class TestLiteralIndex(MappaTestCase):
    """\
    Tests against the literal index.
    """
    def test_occurrence(self):
        idx = self._tm.index.literal
        self.assert_(idx)
        self.assert_(not idx.occurrences('Semagia'))
        occ = self.create_occurrence('Semagia')
        self.assert_(occ in idx.occurrences('Semagia'))
        occ.value = 'Mappa'
        self.assert_(occ not in idx.occurrences('Semagia'))
        self.assert_(occ in idx.occurrences('Mappa'))

    def test_name(self):
        idx = self._tm.index.literal
        self.assert_(idx)
        self.assert_(not idx.names('Semagia'))
        name = self.create_name('Semagia')
        self.assert_(name in idx.names('Semagia'))
        name.value = 'Mappa'
        self.assert_(name not in idx.names('Semagia'))
        self.assert_(name in idx.names('Mappa'))

    def test_variant(self):
        idx = self._tm.index.literal
        self.assert_(idx)
        self.assert_(not idx.variants('Semagia'))
        var = self.create_variant('Semagia')
        self.assert_(var in idx.variants('Semagia'))
        var.value = 'Mappa'
        self.assert_(var not in idx.variants('Semagia'))
        self.assert_(var in idx.variants('Mappa'))

class TestScopedIndex(MappaTestCase):
    """\
    Tests against the scoped index.
    """
    def test_association(self):
        idx = self._tm.index.scoped
        assoc = self.create_association()
        theme = self.create_topic()
        self.assert_(assoc)
        self.assert_(theme)
        self.assert_(0 == len_(assoc.scope))
        self.assert_(assoc not in idx.associations_by_theme(theme))
        assoc.scope = theme
        self.assert_(assoc in idx.associations_by_theme(theme))
        assoc.scope = []
        self.assert_(assoc not in idx.associations_by_theme(theme))
        assoc.scope = [theme]
        self.assert_(assoc in idx.associations_by_theme(theme))
        assoc.remove()
        self.assert_(assoc not in idx.associations_by_theme(theme))

    def test_occurrence(self):
        idx = self._tm.index.scoped
        occ = self.create_occurrence()
        theme = self.create_topic()
        self.assert_(occ)
        self.assert_(theme)
        self.assert_(0 == len_(occ.scope))
        self.assert_(occ not in idx.occurrences_by_theme(theme))
        occ.scope = theme
        self.assert_(occ in idx.occurrences_by_theme(theme))
        occ.scope = []
        self.assert_(occ not in idx.occurrences_by_theme(theme))
        occ.scope = [theme]
        self.assert_(occ in idx.occurrences_by_theme(theme))
        occ.remove()
        self.assert_(occ not in idx.occurrences_by_theme(theme))

    def test_name(self):
        idx = self._tm.index.scoped
        name = self.create_name()
        theme = self.create_topic()
        self.assert_(name)
        self.assert_(theme)
        self.assert_(0 == len_(name.scope))
        self.assert_(name not in idx.names_by_theme(theme))
        name.scope = theme
        self.assert_(name in idx.names_by_theme(theme))
        name.scope = []
        self.assert_(name not in idx.names_by_theme(theme))
        name.scope = [theme]
        self.assert_(name in idx.names_by_theme(theme))
        name.remove()
        self.assert_(name not in idx.names_by_theme(theme))

    def test_variant(self):
        idx = self._tm.index.scoped
        var = self.create_variant()
        theme = self.create_topic()
        self.assert_(var)
        self.assert_(theme)
        self.assert_(1 == len_(var.scope))
        self.assert_(var not in idx.variants_by_theme(theme))
        var.scope = theme
        self.assert_(var in idx.variants_by_theme(theme))
        var.scope = [self.create_topic()]
        self.assert_(var not in idx.variants_by_theme(theme))
        var.scope = [theme]
        self.assert_(var in idx.variants_by_theme(theme))
        var.remove()
        self.assert_(var not in idx.variants_by_theme(theme))

if __name__ == '__main__':
    import nose
    nose.core.runmodule()
