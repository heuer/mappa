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
