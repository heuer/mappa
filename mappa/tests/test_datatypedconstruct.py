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
