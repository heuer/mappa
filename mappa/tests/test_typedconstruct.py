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
