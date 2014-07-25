# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
Tests against topic occurrence creation / fetching.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD License
"""
from . mappa_test import MappaTestCase, len_

class TestTopicOccurrence(MappaTestCase):

    def test_occurrence_creation(self):
        t = self.create_topic()
        self.assertEqual(0, len_(t.occurrences))
        t['homepage'] = 'http://www.semagia.com'
        self.assertEqual(1, len_(t.occurrences))
        occ = tuple(t.occurrences)[0]
        occ_type = self._tm.topic(iid=self._tm.iri + '#' + 'homepage')
        self.assertTrue(occ_type is not None)
        self.assertEqual('http://www.semagia.com', occ.value)
        self.assertEqual(occ_type, occ.type)
        
        self.assertEqual(occ, tuple(t['homepage'])[0])
        self.assertEqual(0, len_(t['xxx']))
        
        t2 = self.create_topic()
        datatype = 'http://www.some.datatype'
        t2['something'] = 34, datatype
        occ = tuple(t2.occurrences)[0]
        self.assertEqual('34', occ.value)
        self.assertEqual(datatype, occ.datatype)

    def test_occurrence_creation_with_scope(self):
        t = self.create_topic()
        self.assertEqual(0, len_(t.occurrences))
        t['homepage @de'] = 'http://www.semagia.com'
        self.assertEqual(1, len_(t.occurrences))
        occ = tuple(t.occurrences)[0]
        occ_type = self._tm.topic(iid=self._tm.iri + '#' + 'homepage')
        self.assertTrue(occ_type is not None)
        self.assertEqual('http://www.semagia.com', occ.value)
        self.assertEqual(occ_type, occ.type)
        
        self.assertEqual(occ, tuple(t['homepage'])[0])
        self.assertEqual(1, len_(t['homepage @de']))
        self.assertEqual(occ, tuple(t['homepage @de'])[0])
        self.assertEqual(0, len_(t['homepage @en']))
        self.assertEqual(0, len_(t['xxx']))
        
        t['homepage @de en'] = 'Semagia'
        self.assertEqual(1, len_(t['homepage @de']))
        self.assertEqual(1, len_(t['homepage @de en']))
        self.assertEqual(0, len_(t['homepage @de en es']))


if __name__ == '__main__':
    import nose
    nose.core.runmodule()
