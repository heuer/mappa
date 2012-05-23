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
Tests against topics.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD License
"""
from . mappa_test import MappaTestCase, len_
from mappa import ModelConstraintViolation

# Remove warning about redefintion of 'type'
# pylint: disable-msg=W0622

class TestTopic(MappaTestCase):

    def test_type(self):
        t = self.create_topic()
        type = self.create_topic()
        self.assertEqual(0, len_(self._tm.associations))
        self.assertEqual(0, len_(t.types))
        self.assertEqual(0, len_(type.instances))
        t.add_type(type)
        self.assertEqual(1, len_(t.types))
        self.assertEqual(1, len_(type.instances))
        # May fail with 3rd party backends
        try:
            self.assertEqual(1, len_(self._tm.associations))
        except AssertionError:
            pass #TODO: Warning
        self.assertTrue(type in t.types)
        self.assertTrue(t in type.instances)
        another_type = self.create_topic()
        t.add_type(another_type)
        self.assertEqual(2, len_(t.types))
        self.assertTrue(another_type in t.types)
        t.remove_type(type)
        self.assertEqual(1, len_(t.types))
        t.remove_type(another_type)
        self.assertEqual(0, len_(t.types))
        

    def test_supertype(self):
        t = self.create_topic()
        supertype = self.create_topic()
        self.assertEqual(0, len_(self._tm.associations))
        self.assertEqual(0, len_(t.types))
        t.add_supertype(supertype)
        self.assertEqual(1, len_(t.supertypes))
        # May fail with 3rd party backends
        try:
            self.assertEqual(1, len_(self._tm.associations))
        except AssertionError:
            pass #TODO: Warning
        self.assertTrue(supertype in t.supertypes)
        another_supertype = self.create_topic()
        t.add_supertype(another_supertype)
        self.assertEqual(2, len_(t.supertypes))
        self.assertTrue(another_supertype in t.supertypes)
        t.remove_supertype(supertype)
        self.assertEqual(1, len_(t.supertypes))
        t.remove_supertype(another_supertype)
        self.assertEqual(0, len_(t.supertypes))

    def test_contains_sid(self):
        sid = 'http://psi.semagia.com/test'
        t = self._tm.create_topic(sid=sid)
        self.assertTrue(sid in t.sids)

    def test_contains_slo(self):
        iri = 'http://www.semagia.com/test'
        t = self._tm.create_topic(slo=iri)
        self.assertTrue(iri in t.slos)

    def test_not_contains_(self):
        iri = 'http://www.semagia.com/test'
        t = self._tm.create_topic(slo=iri)
        slo = '= %s' % iri
        self.assert_(iri in t.slos)
        try:
            slo in t
            self.fail('Remove the __contains__ magic!')
        except TypeError:
            pass
        t2 = self._tm.create_topic(sid=iri)
        self.assert_(iri in t2.sids)
        try:
            iri in t2
            self.fail('Remove the __contains__ magic!')
        except TypeError:
            pass

    def test_not_iadd(self):
        # Removed the iadd magic from Mappa
        # This test tests if this is really gone
        t = self.create_topic()
        try:
            t+= 'http://www.semagia.com/'
            self.fail('Remove the __iadd__ magic')
        except:
            self.assert_('http://www.semagia.com/' not in t.sids)

    def test_not_isub(self):
        # Removed the isub magic from Mappa
        # This test tests if this is really gone
        t = self._tm.create_topic('http://www.semagia.com/')
        self.assert_('http://www.semagia.com/' in t.sids)
        try:
            t-= 'http://www.semagia.com/'
            self.fail('Remove the __isub__ magic')
        except:
            self.assert_('http://www.semagia.com/' in t.sids)

    def test_removal(self):
        ref = 'http://test.semagia.com/'
        topic = self._tm.create_topic(sid=ref)
        self.assert_(topic)
        topic.remove()
        topic = self._tm.topic(sid=ref)
        self.assert_(not topic)

    def test_removal_characteristics(self):
        ref = 'http://test.semagia.com/'
        topic = self._tm.create_topic(sid=ref)
        self.assert_(topic)
        name = topic.create_name(self.create_topic(), value='Semagia')
        self.assert_(name)
        name_id = name.id
        self.assert_(self._tm.construct(id=name_id))
        topic.remove()
        topic = self._tm.topic(sid=ref)
        self.assert_(not topic)
        self.assert_(None is self._tm.construct(id=name_id))

    def test_removal_type(self):
        ref1 = 'http://test.semagia.com/1'
        ref2 = 'http://test.semagia.com/2'
        instance = self._tm.create_topic(sid=ref1)
        type = self._tm.create_topic(sid=ref2)
        self.assert_(instance)
        self.assert_(type)
        instance.add_type(type)
        self.assert_(type in instance.types)
        self.assert_(instance in type.instances)
        self.assert_(1 == len_(self._tm.associations))
        try:
            instance.remove()
            self.fail('The topic plays roles (type-instance) and is not removable')
        except ModelConstraintViolation:
            pass
        instance.remove_type(type)
        self.assert_(0 == len_(self._tm.associations))
        instance.remove()
        self.assert_(None is self._tm.topic(sid=ref1))
        self.assert_(self._tm.topic(sid=ref2))

if __name__ == '__main__':
    import nose
    nose.core.runmodule()
