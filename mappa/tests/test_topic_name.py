# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
Tests against topic name creation / fetching.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD License
"""
from . mappa_test import MappaTestCase, len_
from mappa import TMDM

class TestTopicName(MappaTestCase):

    def test_name_creation(self):
        t = self.create_topic()
        self.assertEqual(0, len_(t.names))
        t['- name'] = 'Semagia'
        self.assertEqual(1, len_(t.names))
        name = tuple(t.names)[0]
        name_type = self._tm.topic(iid=self._tm.iri + '#' + 'name')
        self.assertTrue(name_type is not None)
        self.assertEqual('Semagia', name.value)
        self.assertEqual(name_type, name.type)
        
        self.assertEqual(name, tuple(t['- name'])[0])
        self.assertEqual(0, len_(t['- xxx']))

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
        self.assertEqual(1, len_(t['- name @de']))
        self.assertEqual(name, tuple(t['- name @de'])[0])
        self.assertEqual(0, len_(t['- name @en']))
        self.assertEqual(0, len_(t['- xxx']))
        
        t['-name @de en'] = 'Semagia'
        self.assertEqual(1, len_(t['- name @de']))
        self.assertEqual(1, len_(t['- name @de en']))
        self.assertEqual(0, len_(t['- name @de en es']))
        

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
