# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\


:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD License
"""
from .mappa_test import MappaTestCase
from mappa.utils import atomify
from mappa import TMDM, XSD

class TestAtomification(MappaTestCase):

    def test_simple_topic_atomification(self):
        t = self.create_topic()
        t['-'] = 'Semagia'
        t['- name'] = 'Another name'
        self.assertEqual('Semagia', atomify(t))

    def test_name_atomification(self):
        n = self.create_name('Semagia')
        self.assertEqual('Semagia', atomify(n))

    def test_occurrence_atomification(self):
        t = self.create_topic()
        o = t.create_occurrence(type=self.create_topic(), value=('Semagia', XSD.string))
        self.assertEqual('Semagia', atomify(o))

    def test_variant_atomification(self):
        n = self.create_name('Semagia')
        v = n.create_variant(value=('Semagia', XSD.string), scope=[self.create_topic()])
        self.assertEqual('Semagia', atomify(v))

    def test_contextaware_topic_atomification(self):
        t = self.create_topic()
        default_type = self.create_topic(sid=TMDM.topic_name)
        scope = (self.create_topic(), self.create_topic())
        n = t.create_name(type=self.create_topic(), value='scoped-random-type', scope=scope)
        n2 = t.create_name(type=default_type, value='scoped-default-type', scope=scope)
        t['-'] = 'Semagia'
        self.assertEqual('scoped-default-type', atomify(t, scope))
        n2.scope = [scope[0]]
        self.assertEqual('scoped-random-type', atomify(t, scope))
        n.scope = [scope[0]]
        self.assertEqual('Semagia', atomify(t, scope))
        
    def test_nice_iid(self):
        iid = '%s#%s' % (self._tm.iri, 'nice-iid')
        t = self.create_topic(iid=iid)
        self.assertEqual('nice-iid', atomify(t))
        
    def test_nice_iid2(self):
        iid = '%s#%s' % (self._tm.iri, '238923')
        t = self.create_topic(iid=iid)
        t.add_iid('%s#%s' % (self._tm.iri, 'nice-iid'))
        self.assertEqual('nice-iid', atomify(t))
        
    def test_nice_iid_slash(self):
        iid = '%s%s' % (self._tm.iri, '238923')
        t = self.create_topic(iid=iid)
        t.add_iid('%s%s' % (self._tm.iri, 'nice-iid'))
        self.assertEqual('nice-iid', atomify(t))
        
    def test_nice_sid(self):
        sid = '%s#%s' % (self._tm.iri, 'nice-sid')
        t = self.create_topic(sid=sid)
        self.assertEqual('nice-sid', atomify(t))
        
    def test_nice_sid2(self):
        sid = '%s#%s' % (self._tm.iri, '238923')
        t = self.create_topic(sid=sid)
        t.add_sid('%s#%s' % (self._tm.iri, 'nice-sid'))
        self.assertEqual('nice-sid', atomify(t))
        
    def test_nice_sid_slash(self):
        sid = '%s%s' % (self._tm.iri, '238923')
        t = self.create_topic(sid=sid)
        t.add_sid('%s%s' % (self._tm.iri, 'nice-sid'))
        self.assertEqual('nice-sid', atomify(t))

if __name__ == '__main__':
    import nose
    nose.core.runmodule()
