# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
Tests against associations and roles

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD License
"""
from . mappa_test import MappaTestCase, len_
from mappa import ANY, ModelConstraintViolation

class TestAssociation(MappaTestCase):

    def test_assoc_creation(self):
        self.assertEqual(0, len_(self._tm.associations))
        try:
            self._tm.create_association(None)
            self.fail('Assoc type == None is illegal')
        except Exception: # pylint: disable-msg=W0703
            pass
        self.assertEqual(0, len_(self._tm.associations))
        atype = self.create_topic()
        a = self.create_association(atype)
        self.assertEqual(1, len_(self._tm.associations))
        self.assertEqual(self._tm, a.parent)
        self.assert_(a.type == atype)
        self.assert_(a.parent == self._tm)
        self.assert_(a in self._tm.associations)
        try:
            a.type = None
            self.fail('Assoc type == None is illegal')
        except ValueError:
            pass
        
    def test_assoc_iid(self):
        a = self.create_association(self.create_topic())
        loc = 'http://www.semagia.com'
        a.add_iid(loc)
        self.assertEqual(a, self._tm.construct(iid=loc))
        
    def test_role_creation(self):
        atype = self.create_topic()
        a = self.create_association(atype)
        self.assertEqual(0, len(a))
        rtype, player = self.create_topic(), self.create_topic()
        self.assertEqual(0, len_(player.roles_played))
        r = a.create_role(rtype, player)
        self.assertEqual(1, len(a))
        self.assertEqual(a, r.parent)
        self.assertTrue(r in player.roles_played)
        self.assertTrue(r in player.roles_by(rtype))
        self.assertTrue(r in a)
        self.assert_(r not in player.roles_by(self.create_topic()))
        try:
            a.create_role(None, player)
            self.fail('Role with type == None is not allowed')
        except:
            pass
        try:
            a.create_role(rtype, None)
            self.fail('Role with player == None is not allowed')
        except:
            pass
        
    def test_assoc_add_role(self):
        a = self.create_association(self.create_topic())
        r = a.create_role(self.create_topic(), self.create_topic())
        self.assertEqual(1, len(a))
        a.add_role(r)
        self.assertEqual(1, len(a))

        tm2 = self.create_map()
        a2 = tm2.create_association(self.create_topic(tm2))
        r2 = a2.create_role(self.create_topic(tm2), self.create_topic(tm2))
        try:
            a.add_role(r2)
            self.fail('Moving constructs is not allowed')
        except:
            pass

        try:
            a.add_role(None)
            self.fail('Adding role which is None is not allowed')
        except:
            pass
        
    def test_assoc_removeRole(self):
        a = self.create_association(self.create_topic())
        r = a.create_role(self.create_topic(), self.create_topic())
        self.assertEqual(1, len(a))
        self.assertTrue(r in a)
        a.remove_role(r)
        self.assertEqual(0, len(a))
        self.assertTrue(r not in a)

        try:
            a.remove_role(None)
            self.fail('Removing a role which is None is not allowed')
        except:
            pass
        
    def test_player(self):
        a = self.create_association(self.create_topic())
        r = a.create_role(self.create_topic(), self.create_topic())
        t = self.create_topic()
        r.player = t
        self.assert_(r.player == t)

        tm2 = self.create_map()
        t2 = self.create_topic(tm2)
        try:
            r.player = t2
            self.fail('Moving constructs is not allowed')
        except ModelConstraintViolation, ex:
            pass
        self.assert_(r.player == t)
        try:
            r.player = None
            self.fail('Role player == None is not allowed')
        except ValueError, ex:
            pass

    def test_role_creation_magic(self):
        atype = self.create_topic()
        a = self.create_association(atype)
        self.assertEqual(0, len(a))
        rtype, player = self.create_topic(), self.create_topic()
        self.assertEqual(0, len_(player.roles_played))
        a[rtype] = player
        self.assertEqual(1, len(a))
        self.assertEqual(1, len_(player.roles_played))
        self.assert_(player in a[rtype])
        
        a['type'] = 'player'
        self.assertEqual(2, len_(a.roles))
        t = self._tm.topic(iid='%s#%s' % (self._tm.iri, 'type'))
        p = self._tm.topic(iid='%s#%s' % (self._tm.iri, 'player'))
        self.assertFalse(None is t)
        self.assertFalse(None is p)
        self.assertTrue(p in a['type'])

    def test_assoc_roles_by_type(self):
        t = self.create_topic()
        a = self.create_association(self.create_topic())
        r = a.create_role(self.create_topic(), t)
        self.assert_(r in a.roles_by(r.type))
        self.assert_(r not in a.roles_by(self.create_topic()))
        self.assert_(r in a.roles_by(ANY))
    
    def test_assoc_players_by_type(self):
        t = self.create_topic()
        a = self.create_association()
        r = a.create_role(self.create_topic(), t)
        self.assert_(t in a.players_by(r.type))
        self.assert_(t not in a.players_by(self.create_topic()))
        self.assert_(t in a.players_by(ANY))
        self.assert_(t in a[r.type])
        self.assert_(t in a[ANY])
        
    def test_player_roles_by_type(self):
        a = self.create_association(self.create_topic())
        type, player = self.create_topic(), self.create_topic()
        r = a.create_role(type, player)
        self.assert_(r in player.roles_played)
        self.assert_(r in player.roles_by(type))
        self.assert_(r in player.roles_by(ANY))
        self.assert_(r not in player.roles_by(self.create_topic()))
        
        a2 = self.create_association(self.create_topic())
        r2 = a2.create_role(self.create_topic(), self.create_topic())
        self.assert_(r2 not in player.roles_by(type))
        r2.player = player
        self.assert_(r2 not in player.roles_by(type))
        r2.type = type
        self.assert_(r in player.roles_by(type))
        self.assert_(r2 in player.roles_by(type))
        assoc_type = self.create_topic()
        a2.type = assoc_type
        self.assert_(r not in player.roles_by(type, assoc_type))
        self.assert_(r2 in player.roles_by(type, assoc_type))
        
    def test_assoc_role_unpacking(self):
        a = self.create_association(self.create_topic())
        l = []
        for i in xrange(1, 10):
            type, player = self.create_topic(), self.create_topic()
            a.create_role(type, player)
            l.append((type, player))
        for type, player in a.roles:
            self.assertTrue((type, player) in l)

        
if __name__ == '__main__':
    import nose
    nose.core.runmodule()
