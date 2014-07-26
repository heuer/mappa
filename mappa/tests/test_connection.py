# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
Tests against the topic map connection.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD License
"""
from . mappa_test import MappaTestCase, len_

class TestTopicMapConnection(MappaTestCase):

    def test_contains(self):
        loc = self.random_locator()
        self.assertFalse(loc in self._conn)
        # 1, because self._tm is in the sys
        self.assertEqual(1, len_(self._conn.iris))
        self._conn.create(loc)
        self.commit()
        self.assertTrue(loc in self._conn)
        self.assertEqual(2, len_(self._conn.iris))
        self.assertTrue(loc in self._conn.iris)

    def test_dict(self):
        loc = self.random_locator()
        try:
            tm = self._conn[loc]
            self.fail('KeyError for non-existent topic map expected')
        except KeyError:
            pass
        self.assertTrue(None is self._conn.get(loc))
        tm = self._conn.create(loc)
        self.commit()
        self.assertTrue(tm == self._conn[loc])

    def test_creation(self):
        loc = self.random_locator()
        self.assertTrue(None is self._conn.get(loc))
        self._conn.create(loc)
        try:
            self._conn.create(loc)
            self.fail('ValueError expected, the IRI is already bound')
        except ValueError:
            pass

if __name__ == '__main__':
    import nose
    nose.core.runmodule()
