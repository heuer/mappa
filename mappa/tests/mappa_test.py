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
Base class for Mappa tests which provides some utility methods.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD License
"""
from unittest import TestCase
import mappa
from mappa import XSD


class MappaTestCase(TestCase):
    """\
    
    """
    base = 'http://mappa.semagia.com/test/'
    config = {'backend':'mem'}
    
    def setUp(self):
        self._conn = mappa.connect(**self.config)
        self._tm = self._conn.create(self.base)
        
    def tearDown(self):
        for loc in tuple(self._conn.iris):
            del self._conn[loc]
        self._conn.close(True)

    def topic_by_sid(self, sid):
        return self._tm.topic(sid=sid)

    def topic_by_slo(self, slo):
        return self._tm.topic(slo=slo)

    def topic_by_iid(self, iid):
        return self._tm.topic(iid=iid)

    def topic_by_id(self, ident, base=None):
        base = base or self.base
        return self.topic_by_iid(base + "#" + ident)

    def random_locator(self):
        return self.base + str(randid())
        
    def create_map(self, iri=None):
        if not iri:
            iri = self.random_locator()
        return self._conn.create(iri)
    
    def create_topic(self, tm=None, **kw):
        if tm is None:
            tm = self._tm
        return tm.create_topic(**kw)
    
    def create_association(self, type=None, scope=()): # pylint: disable-msg=W0622
        return self._tm.create_association(type=(type or self.create_topic()), 
                                           #roles=[(self.create_topic(), self.create_topic())], 
                                           scope=scope)

    def create_role(self, type=None, player=None): # pylint: disable-msg=W0622
        assoc = self.create_association()
        return assoc.create_role(type=(type or self.create_topic()),
                                 player=(player or self.create_topic()))

    def create_occurrence(self, value=None, datatype=None):
        t = self.create_topic()
        return t.create_occurrence(type=self.create_topic(), 
                             value=((value or 'a value'), (datatype or XSD.string)))

    def create_name(self, value=None):
        t = self.create_topic()
        return t.create_name(type=self.create_topic(), 
                             value=(value or 'a value'))

    def create_variant(self, value=None, datatype=None, scope=None):
        n = self.create_name()
        return n.create_variant( 
                             value=((value or 'a value'), (datatype or XSD.string)),
                             scope=(scope or [self.create_topic()]))

    def commit(self):
        self._conn.commit()

if not hasattr(MappaTestCase, 'assertTrue'):
    MappaTestCase.assertTrue = lambda self, expr: self.assert_(expr)
    MappaTestCase.assertFalse = lambda self, expr: self.assert_(not expr)

def len_(coll):
    """\
    Returns the length / size of a collection / generator / iterator.
    """
    return len(tuple(coll))

import random

def randid(randint=random.randint, choice=random.choice, signs=(-1,1)):
    return choice(signs)*randint(1,2000000000)

del random
