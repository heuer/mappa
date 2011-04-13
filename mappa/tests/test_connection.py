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
