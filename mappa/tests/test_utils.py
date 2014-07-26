# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
Tests the utility module.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD License
"""
from . mappa_test import MappaTestCase, len_
from mappa.utils import * # pylint: disable-msg=W0401, W0614
from mappa import ANY, UCS, TMDM

# Remove warning about redefintion of 'type'
# pylint: disable-msg=W0622

class TestUtils(MappaTestCase):
    
    def _test_is_(self, func, obj):
        # Tests is_* DOES NOT work with Topic Map instances!
        self.assertTrue(is_construct(obj))
        self.assertTrue(func(obj))
        self.assertFalse(func(object()))
        self.assertFalse(func(None))
        self.assertFalse(func(self._tm)) # Something which is a construct
        
    def test_is_topicmap(self):
        self.assertTrue(is_topicmap(self._tm))
        self.assertFalse(is_topicmap(object()))
        self.assertFalse(is_topicmap(self.create_topic()))
        
    def test_is_topic(self):
        self._test_is_(is_topic, self.create_topic())
        
    def test_is_association(self):
        self._test_is_(is_association, self.create_association())
        
    def test_is_role(self):
        assoc = self.create_association(self.create_topic())
        role = assoc.create_role(self.create_topic(), self.create_topic())
        self._test_is_(is_role, role)
        
    def test_is_occurrence(self):
        occ = self.create_topic().create_occurrence(type=self.create_topic(),
                                                    value='Semagia')
        self._test_is_(is_occurrence, occ)
        
    def test_is_name(self):
        name = self.create_topic().create_name(type=self.create_topic(),
                                                    value='Semagia')
        self._test_is_(is_name, name)
        
    def test_is_variant(self):
        name = self.create_topic().create_name(type=self.create_topic(),
                                                    value='Semagia')
        var = name.create_variant(value='Semagia', scope=(self.create_topic(),))
        self._test_is_(is_variant, var)
        
    def test_is_dataobject(self):
        occ = self.create_topic().create_occurrence(type=self.create_topic(),
                                                    value='Semagia')
        name = self.create_topic().create_name(type=self.create_topic(),
                                                    value='Semagia')
        var = name.create_variant(value='Semagia', scope=(self.create_topic(),))
        
        self.assertTrue(is_datatyped(occ))
        self.assertFalse(is_datatyped(self.create_topic()))
        self.assertFalse(is_datatyped(name))
        self.assertTrue(is_datatyped(var))

    def test_is_literal(self):
        from mappa import Literal
        self.assert_(not is_literal(object()))
        self.assert_(is_literal(Literal('test')))
        
    def test_has_type(self):
        type = self.create_topic()
        
        assoc = self.create_association(type)
        self.assertTrue(has_type(assoc, type))
        self.assertTrue(has_type(assoc, ANY))
        self.assertFalse(has_type(assoc, self.create_topic()))
        
        role = assoc.create_role(type=type, player=self.create_topic())
        self.assertTrue(has_type(role, type))
        self.assertTrue(has_type(role, ANY))
        self.assertFalse(has_type(role, self.create_topic()))

        occ = self.create_topic().create_occurrence(type=type, value='Semagia')
        self.assertTrue(has_type(occ, type))
        self.assertTrue(has_type(occ, ANY))
        self.assertFalse(has_type(occ, self.create_topic()))
        
        name = self.create_topic().create_name(type=type, value='Semagia')
        self.assertTrue(has_type(name, type))
        self.assertTrue(has_type(name, ANY))
        self.assertFalse(has_type(name, self.create_topic()))

        try:
            has_type(self.create_topic(), type)
            self.fail('Topics are not typed')
        except AttributeError:
            pass

    def test_has_scope(self):
        type = self.create_topic()
        
        theme1 = self.create_topic()
        theme2 = self.create_topic()
        scope = (theme1, theme2)
        
        assoc = self.create_association(type, scope=scope)
        self.assertTrue(has_scope(assoc, scope))
        self.assertTrue(has_scope(assoc, scope, False))
        self.assertTrue(has_scope(assoc, ANY))
        self.assertFalse(has_scope(assoc, UCS))
        self.assertFalse(has_scope(assoc, [self.create_topic()]))
        self.assertFalse(has_scope(assoc, [theme1]))
        self.assertFalse(has_scope(assoc, [theme2]))
        self.assertTrue(has_scope(assoc, [theme1], False))
        self.assertTrue(has_scope(assoc, [theme2], False))
        
        assoc.scope = [theme2]
        self.assertFalse(has_scope(assoc, [theme1], False))
        self.assertTrue(has_scope(assoc, [theme2], False))
        self.assertTrue(has_scope(assoc, ANY))
        self.assertFalse(has_scope(assoc, UCS))
        
        assoc.scope = []
        self.assertFalse(has_scope(assoc, [theme2], False))
        self.assertTrue(has_scope(assoc, ANY))
        self.assertTrue(has_scope(assoc, UCS))
        
    def test_valid_in_scope(self):
        type = self.create_topic()
        
        theme1 = self.create_topic()
        theme2 = self.create_topic()
        scope = (theme1, theme2)
        
        assoc = self.create_association(type, scope=scope)
        self.assertTrue(valid_in_scope(assoc, scope))
        self.assertTrue(valid_in_scope(assoc, scope, False))
        self.assertTrue(valid_in_scope(assoc, ANY))
        self.assertFalse(valid_in_scope(assoc, UCS))
        self.assertFalse(valid_in_scope(assoc, [self.create_topic()]))
        self.assertFalse(valid_in_scope(assoc, [theme1]))
        self.assertFalse(valid_in_scope(assoc, [theme2]))
        self.assertTrue(valid_in_scope(assoc, [theme1], False))
        self.assertTrue(valid_in_scope(assoc, [theme2], False))
    
        assoc.scope = [theme2]
        self.assertFalse(valid_in_scope(assoc, theme1, False))
        self.assertTrue(valid_in_scope(assoc, [theme2], False))
        self.assertTrue(valid_in_scope(assoc, ANY))
        self.assertFalse(valid_in_scope(assoc, UCS))

        # Assoc is in UCS, any scope is valid now
        assoc.scope = []
        
        self.assertTrue(valid_in_scope(assoc, [theme1]))
        self.assertTrue(valid_in_scope(assoc, [theme2]))
        self.assertTrue(valid_in_scope(assoc, scope))
        self.assertTrue(valid_in_scope(assoc, ANY))
        self.assertTrue(valid_in_scope(assoc, UCS))
        self.assertTrue(valid_in_scope(assoc, (self.create_topic(), self.create_topic(), self.create_topic())))
        

    def test_is_default_name(self):
        default_name = self.create_topic().create_name(type=None, value='Semagia')
        name = self.create_topic().create_name(type=self.create_topic(), value='Semagia')
        
        self.assertTrue(is_default_name(default_name))
        self.assertFalse(is_default_name(name))

        default_name.type.remove_sid(TMDM.topic_name)
        self.assertFalse(is_default_name(default_name))
        
        name.type.add_sid(TMDM.topic_name)
        self.assertTrue(is_default_name(name))
        
    def test_in_ucs(self):
        assoc = self.create_association(self.create_topic())
        self.assertTrue(in_ucs(assoc))
        theme = self.create_topic()
        assoc.scope = [theme]
        self.assertFalse(in_ucs(assoc))
        assoc.scope = []
        self.assertTrue(in_ucs(assoc))
        
    def test_assoc_arity(self):
        assoc = self.create_association()
        assoc.create_role(self.create_topic(), self.create_topic())
        self.assertEqual(1, arity(assoc))
        self.assertTrue(is_unary(assoc))
        assoc.create_role(self.create_topic(), self.create_topic())
        self.assertEqual(2, arity(assoc))
        self.assertTrue(is_binary(assoc))
        assoc.create_role(self.create_topic(), self.create_topic())
        self.assertEqual(3, arity(assoc))
        self.assertTrue(is_ternary(assoc))
        
    def test_is_associated(self):
        topic1 = self.create_topic()
        topic2 = self.create_topic()
        type = self.create_topic()

        self.assertFalse(is_associated(topic1, topic2))
        self.assertFalse(is_associated(topic1, topic2, type))
        
        assoc = self.create_association(self.create_topic())
        assoc.create_role(self.create_topic(), topic1)
        assoc.create_role(self.create_topic(), topic2)
        
        self.assertTrue(is_associated(topic1, topic2))
        self.assertTrue(is_associated(topic1, topic2, assoc.type))
        self.assertFalse(is_associated(topic1, topic2, type))
        
        assoc.type = type
        self.assertTrue(is_associated(topic1, topic2))
        self.assertTrue(is_associated(topic1, topic2, type))
        
        role = tuple(topic1.roles_played)[0]
        role.remove()
        
        self.assertFalse(is_associated(topic1, topic2))
        self.assertFalse(is_associated(topic1, topic2, type))

    def test_find_associated(self):
        t1 = self.create_topic()
        t2 = self.create_topic()
        self.assertEqual(0, len_(find_associated(t1)))
        t1.add_type(t2)
        self.assertEqual(1, len_(find_associated(t1)))
        self.assert_(t2 in find_associated(t1))
        self.assert_(t2 in find_associated(t1, type=self._tm.topic(sid=TMDM.instance)))
        self.assert_(t2 in find_associated(t1, type=self._tm.topic(sid=TMDM.instance),
                                           other_type=self._tm.topic(sid=TMDM.type)))
        self.assert_(t2 in find_associated(t1, type=self._tm.topic(sid=TMDM.instance),
                                           other_type=self._tm.topic(sid=TMDM.type),
                                           assoc_type=self._tm.topic(sid=TMDM.type_instance)))
        self.assert_(t2 in find_associated(t1, type=self._tm.topic(sid=TMDM.instance),
                                           other_type=self._tm.topic(sid=TMDM.type),
                                           assoc_type=self._tm.topic(sid=TMDM.type_instance),
                                           scope=UCS))
        self.assert_(t2 in find_associated(t1, type=self._tm.topic(sid=TMDM.instance),
                                           other_type=self._tm.topic(sid=TMDM.type),
                                           assoc_type=self._tm.topic(sid=TMDM.type_instance),
                                           scope=ANY))
        assoc = tuple(self._tm.associations)[0]
        self.assertEqual(self._tm.topic(sid=TMDM.type_instance), assoc.type)
        theme = self.create_topic()
        assoc.scope = theme
        self.assert_(t2 not in find_associated(t1, type=self._tm.topic(sid=TMDM.instance),
                                           other_type=self._tm.topic(sid=TMDM.type),
                                           assoc_type=self._tm.topic(sid=TMDM.type_instance),
                                           scope=UCS))
        self.assert_(t2 in find_associated(t1, type=self._tm.topic(sid=TMDM.instance),
                                           other_type=self._tm.topic(sid=TMDM.type),
                                           assoc_type=self._tm.topic(sid=TMDM.type_instance),
                                           scope=ANY))
        self.assert_(t2 in find_associated(t1, type=self._tm.topic(sid=TMDM.instance),
                                           other_type=self._tm.topic(sid=TMDM.type),
                                           assoc_type=self._tm.topic(sid=TMDM.type_instance),
                                           scope=[theme]))
        self.assertEqual(0, len_(find_associated(t1, scope=[self.create_topic()])))
        self.assertEqual(0, len_(find_associated(t1, type=self.create_topic())))
        self.assertEqual(0, len_(find_associated(t1, assoc_type=self.create_topic())))

    def test_is_removable(self):
        topic = self.create_topic()
        self.assert_(is_removable(topic))
        type = self.create_topic()
        topic.add_type(type)
        self.assert_(not is_removable(topic))
        topic.remove_type(type)
        self.assert_(is_removable(topic))
        assoc = self.create_association()
        assoc.scope = topic
        self.assert_(not is_removable(topic))
        assoc.scope = []
        self.assert_(is_removable(topic))
        assoc.type = topic
        self.assert_(not is_removable(topic))
        assoc.type = self.create_topic()
        self.assert_(is_removable(topic))

    
    def make_iko(self, sub, super):
        # Creates a type-instance relationship between ``sub`` and ``super``
        subtype = self.create_topic(sid=TMDM.subtype)
        supertype = self.create_topic(sid=TMDM.supertype)
        assoc = self.create_association(self.create_topic(sid=TMDM.supertype_subtype))
        assoc[supertype] = super
        assoc[subtype] = sub
        
    def test_isa_simple_topic(self):
        t = self.create_topic()
        type = self.create_topic()
        self.assertFalse(isa(t, type))
        t.add_type(type)
        self.assertTrue(isa(t, type))
        t.remove_type(type)
        self.assertFalse(isa(t, type))
        
    def test_isa_simple_topic2(self):
        t = self.create_topic()
        type = self.create_topic()
        self.assertFalse(isa(t, type))
        t.add_type(type)
        self.assertTrue(isa(t, type))
        
        type2 = self.create_topic()
        self.assertFalse(isa(t, type2))
        type.add_type(type2)
        self.assertTrue(isa(type, type2))
        self.assertFalse(isa(t, type2))
        
    def test_isa_topic(self):
        super = self.create_topic()
        t = self.create_topic()
        type = self.create_topic()
        self.make_iko(type, super)
        self.assertFalse(isa(t, super))
        t.add_type(type)
        self.assertTrue(isa(t, super))
        t.remove_type(type)
        self.assertFalse(isa(t, super))
        
        # t isa type
        # type iko super
        # super iko supersuper
        # isa(t, supersuper) -> True
        supersuper = self.create_topic()
        self.make_iko(super, supersuper)
        self.assertFalse(isa(t, supersuper))
        t.add_type(type)
        self.assertTrue(isa(t, supersuper))
        t.remove_type(type)
        self.assertFalse(isa(t, supersuper))
    
    def test_isa_simple_typed(self):
        occ_type = self.create_topic()
        occ = self.create_topic().create_occurrence(occ_type, 'Semagia')
        type = self.create_topic()
        self.assertFalse(isa(occ, type))
        occ.type = type
        self.assertTrue(isa(occ, type))
        occ.type = occ_type
        self.assertFalse(isa(occ, type))
        
    def test_isa_simple_typed2(self):
        occ_type = self.create_topic()
        occ = self.create_topic().create_occurrence(occ_type, 'Semagia')
        type = self.create_topic()
        self.assertFalse(isa(occ, type))
        occ.type = type
        self.assertTrue(isa(occ, type))
     
        type2 = self.create_topic()
        self.assertFalse(isa(occ, type2))
        type.add_type(type2)
        self.assertTrue(isa(type, type2))
        self.assertFalse(isa(occ, type2))
        
    def test_isa_typed(self):
        super = self.create_topic()
        type = self.create_topic()
        deftype = self.create_topic()
        assoc = self.create_association(deftype)
        self.make_iko(type, super)
        self.assertFalse(isa(assoc, super))
        assoc.type = type
        self.assertTrue(isa(assoc, super))
        assoc.type = deftype
        self.assertFalse(isa(assoc, super))
        
        # assoc isa type
        # type iko super
        # super iko supersuper
        # isa(t, supersuper) -> True
        supersuper = self.create_topic()
        self.make_iko(super, supersuper)
        self.assertFalse(isa(assoc, supersuper))
        assoc.type = type
        self.assertTrue(isa(assoc, supersuper))
        assoc.type = deftype
        self.assertFalse(isa(assoc, supersuper))
        
    def test_supertypes_of(self):
        pass
    
    def test_subtypes_of(self):
        pass
        
if __name__ == '__main__':
    import nose
    nose.core.runmodule()
