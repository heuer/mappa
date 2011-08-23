# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2011 -- Lars Heuer - Semagia <http://www.semagia.com/>.
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
#     * Neither the name of the project nor the names of the contributors 
#       may be used to endorse or promote products derived from this 
#       software without specific prior written permission.
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
This module provides implementation stubs for backends.

These stubs are useful for an `OO`_ view on the `TMDM`_.

.. _OO: http://en.wikipedia.org/wiki/Object-oriented_programming
.. _TMDM: http://www.isotopicmaps.org/sam/sam-model/

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD License
"""
from operator import attrgetter
from mappa import irilib, ModelConstraintViolation, Literal, ANY, UCS, TMDM, XSD
from mappa.utils import is_construct, is_topic
from mappa._internal import kind, it
from mappa._internal.constraints import check_not_none, check_same_topicmap
from mappa.backend.events import *


__all__ = ('TopicMapStub',
           'TopicStub', 'AssociationStub', 'RoleStub',
           'OccurrenceStub', 'NameStub', 'VariantStub')

class ReifiableConstructStub(object):
    def __init__(self, reifier):
        self._reifier = reifier

    def _set_reifier(self, reifier):
        if self._reifier == reifier:
            return
        self._fire_event(SetReifier(self, self._reifier, reifier))
        if self._reifier:
            self._reifier._reified = None
        self._reifier = reifier
        if reifier:
            reifier._reified = self

    reifier = property(attrgetter('_reifier'), _set_reifier)


class TypedConstructStub(object):
    def __init__(self, type):
        self._type = type

    def _set_type(self, type):
        check_not_none(type)
        assert is_topic(type)
        if self._type == type:
            return
        self._fire_event(SetType(self, self._type, type))
        self._type = type

    type = property(attrgetter('_type'), _set_type)


class DatatypeAwareConstructStub(object):

    def __init__(self, literal):
        self._literal = literal

    def _set_literal(self, lit):
        check_not_none(lit)
        lit = Literal(lit)
        if self._literal == lit:
            return
        self._fire_event(SetValue(self, self._literal, lit))
        self._literal = lit

    def __pyvalue__(self):
        return self._literal.__pyvalue__()

    def __int__(self):
        return int(self._literal)

    def __float__(self):
        return float(self._literal)

    def __long__(self):
        return long(self._literal)

    def __str__(self):
        return str(self._literal)

    literal = property(attrgetter('_literal'))
    value = property(lambda self: self._literal.value, _set_literal)
    datatype = property(lambda self: self._literal.datatype)

class TopicMapsConstructStub(object):
    """\
    Derived classes must provide the following mutable attributes:
    - `iids` (a set)
    """
    def __init__(self, tm):
        self._tm = tm
        self._parent = None
        self.iids = self._create_iids()

    def _is_attached(self):
        # Take care, may lead into infinitive loop, must be overridden by
        # topic, assoc, topic map
        return self._parent is not None and self._parent._is_attached()

    def add_iid(self, iid):
        check_not_none(iid)
        _check_attached(self)
        iid = irilib.normalize(iid)
        if iid in self.iids:
            return
        self._fire_event(AddItemIdentifier(self, iid))
        self.iids.add(iid)

    def remove_iid(self, iid):
        check_not_none(iid)
        _check_attached(self)
        iid = irilib.normalize(iid)
        if iid not in self.iids:
            return
        self._fire_event(RemoveItemIdentifier(self, iid))
        self.iids.remove(iid)

    def __hash__(self):
        return hash(self.id)

    def __eq__(self, other):
        return self.id == getattr(other, 'id', None)

    def _fire_event(self, evt):
        if not self._is_attached():
            return
        self._tm.dispatch(evt)

    tm = property(attrgetter('_tm'))
    parent = property(attrgetter('_parent'))


class ScopedConstructStub(TopicMapsConstructStub):
    """\
    Derived classes must provide the following mutable attributes:
    - `_scope` (a set)
    """
    def __init__(self, tm, scope=()):
        TopicMapsConstructStub.__init__(self, tm)
        self._scope = self._create_scope(scope)

    def _set_scope(self, scope):
        check_not_none(scope)
        if is_topic(scope):
            scope = (scope,)
        for theme in scope:
            check_same_topicmap(self.tm, theme)
        new_scope = self._create_scope(scope)
        self._fire_event(SetScope(self, self._scope, new_scope))
        self._scope = new_scope

    scope = property(attrgetter('_scope'), _set_scope)

class TopicMapStub(TopicMapsConstructStub, ReifiableConstructStub,
                  EventDispatcher):
    """\
    Derived classes must provide the following mutable attributes:
    - `builder` (a builder for Topic Maps constructs)
    - `topics` (a set)
    - `associations` (a set)
    """
    _kind = kind.TOPIC_MAP
    def __init__(self, iri):
        TopicMapsConstructStub.__init__(self, None)
        ReifiableConstructStub.__init__(self, None)
        EventDispatcher.__init__(self)
        self._event_multiplier = EventMultiplier(self)
        self._iri = iri

        self.topics = self._create_topics()
        self.associations = self._create_associations()

    def dispatch(self, evt):
        if is_construct(evt.new):
            check_same_topicmap(self, evt.new)
        EventDispatcher.dispatch(self, evt)

    def _is_attached(self):
        return True

    def _create_topic(self):
        topic = self.builder.create_topic()
        self.add_topic(topic)
        return topic

    def create_topic_by_iid(self, iid):
        topic = self.topic_by_iid(iid)
        if topic:
            return topic
        topic = self.topic_by_sid(iid)
        if not topic:
            topic = self._create_topic()
        topic.add_iid(iid)
        return topic

    def create_topic_by_sid(self, sid):
        topic = self.topic_by_sid(sid)
        if topic:
            return topic
        topic = self.topic_by_iid(sid)
        if not topic:
            topic = self._create_topic()
        topic.add_sid(sid)
        return topic

    def create_topic_by_slo(self, slo):
        topic = self.topic_by_slo(slo)
        if topic:
            return topic
        topic = self._create_topic()
        topic.add_slo(slo)
        return topic

    def create_association(self, type, scope=()):
        assert type is not None
        assoc = self.builder.create_association(type, scope)
        self.add_association(assoc)
        return assoc

    def add_topic(self, child):
        assert child is not None
        if not _accept_child(self, child):
            return
        self._fire_event(AddTopic(self, child))
        child._parent = self
        self.topics.add(child)

    def remove_topic(self, child):
        if child._parent != self:
            return
        self._fire_event(RemoveTopic(self, child))
        self.topics.remove(child)
        child._parent = None

    def add_association(self, child):
        assert child is not None
        if not _accept_child(self, child):
            return
        self._fire_event(AddAssociation(self, child))
        child._parent = self
        self.associations.add(child)

    def remove_association(self, child):
        if child._parent != self:
            return
        self._fire_event(RemoveAssociation(self, child))
        self.associations.remove(child)
        child._parent = None

    def _fire_event(self, evt):
        self.dispatch(evt)

    parent = property(lambda self: self)
    tm = property(lambda self: self)
    iri = property(attrgetter('_iri'))


class TopicStub(TopicMapsConstructStub):
    """\
    Derived classes must provide the following mutable attributes:
    - `sids` (a set)
    - `slos` (a set)
    - `roles_played` (a set)
    - `occurrences` (a set)
    - `names` (a set)
    """
    _kind = kind.TOPIC
    def __init__(self, tm):
        TopicMapsConstructStub.__init__(self, tm)
        self._reified = None
        self.sids = self._create_sids()
        self.slos = self._create_slos()
        self.roles_played = self._create_roles_played()
        self.occurrences = self._create_occurrences()
        self.names = self._create_names()

    def _is_attached(self):
        return self._parent is not None

    def add_sid(self, sid):
        check_not_none(sid)
        _check_attached(self)
        sid = irilib.normalize(sid)
        if sid in self.sids:
            return
        self._fire_event(AddSubjectIdentifier(self, sid))
        self.sids.add(sid)

    def remove_sid(self, sid):
        check_not_none(sid)
        _check_attached(self)
        sid = irilib.normalize(sid)
        if sid not in self.sids:
            return
        self._fire_event(RemoveSubjectIdentifier(self, sid))
        self.sids.remove(sid)

    def add_slo(self, slo):
        check_not_none(slo)
        _check_attached(self)
        slo = irilib.normalize(slo)
        if slo in self.slos:
            return
        self._fire_event(AddSubjectLocator(self, slo))
        self.slos.add(slo)

    def remove_slo(self, slo):
        check_not_none(slo)
        _check_attached(self)
        slo = irilib.normalize(slo)
        if slo not in self.slos:
            return
        self._fire_event(RemoveSubjectLocator(self, slo))
        self.slos.remove(slo)

    def create_occurrence(self, type, value, scope=()):
        assert type is not None
        assert value is not None
        occ = self._tm.builder.create_occurrence(type, Literal(value), scope)
        self.add_occurrence(occ)
        return occ

    def add_occurrence(self, child):
        assert child is not None
        if not _accept_child(self, child):
            return
        self._fire_event(AddOccurrence(self, child))
        child._parent = self
        self.occurrences.add(child)

    def remove_occurrence(self, child):
        if child._parent != self:
            return
        self._fire_event(RemoveOccurrence(self, child))
        self.occurrences.remove(child)
        child._parent = None

    def create_name(self, type, value, scope=()):
        if not type:
            type = self._tm.create_topic(sid=TMDM.topic_name)
        assert value is not None
        name = self._tm.builder.create_name(type, Literal(value), scope)
        self.add_name(name)
        return name

    def add_name(self, child):
        assert child is not None
        if not _accept_child(self, child):
            return
        self._fire_event(AddName(self, child))
        child._parent = self
        self.names.add(child)

    def remove_name(self, child):
        assert child is not None
        if child._parent != self:
            return
        self._fire_event(RemoveName(self, child))
        self.names.remove(child)
        child._parent = None

    def remove(self):
        from mappa.utils import is_removable
        if not is_removable(self):
            raise ModelConstraintViolation('The topic is not removable since it plays roles or it is used as type, player, reifier, or theme')
        self._tm.remove_topic(self)
        for occ in tuple(self.occurrences):
            occ.remove()
        for name in tuple(self.names):
            name.remove()

    parent = property(attrgetter('_tm'))
    reified = property(attrgetter('_reified'))


class AssociationStub(ScopedConstructStub, TypedConstructStub, ReifiableConstructStub):
    """\
    Derived classes must provide the following mutable attributes:
    - `roles` (a set)
    """
    _kind = kind.ASSOCIATION
    def __init__(self, tm, type, scope=()):
        ScopedConstructStub.__init__(self, tm, scope)
        TypedConstructStub.__init__(self, type)
        ReifiableConstructStub.__init__(self, None)
        self.roles = self._create_roles()

    def create_role(self, type, player):
        role = self._tm.builder.create_role(type, player)
        self.add_role(role)
        return role

    def _is_attached(self):
        return self._parent is not None

    def add_role(self, child):
        assert child is not None
        if not _accept_child(self, child):
            return
        self._fire_event(AddRole(self, child))
        child._parent = self
        child.player.roles_played.add(child)
        self.roles.add(child)

    def remove_role(self, child):
        assert child is not None
        if child._parent != self:
            return
        self._fire_event(RemoveRole(self, child))
        self.roles.remove(child)
        child.player.roles_played.remove(child)
        child._parent = None

    def remove(self):
        self.reifier = None
        self._tm.remove_association(self)
        for role in tuple(self.roles):
            role.remove()

    parent = property(attrgetter('_tm'))


class RoleStub(TopicMapsConstructStub, TypedConstructStub, ReifiableConstructStub):

    _kind = kind.ROLE

    def __init__(self, tm, type, player):
        TopicMapsConstructStub.__init__(self, tm)
        TypedConstructStub.__init__(self, type)
        ReifiableConstructStub.__init__(self, None)
        self._player = player

    def _set_player(self, player):
        check_not_none(player)
        check_same_topicmap(self, player)
        if self._player:
            self._player.roles_played.remove(self)
        self._player = player
        player.roles_played.add(self)

    def remove(self):
        self.reifier = None
        self._parent.remove_role(self)

    player = property(attrgetter('_player'), _set_player)


class OccurrenceStub(ScopedConstructStub, TypedConstructStub, ReifiableConstructStub, DatatypeAwareConstructStub):

    _kind = kind.OCCURRENCE

    def __init__(self, tm, type, value, scope=UCS):
        ScopedConstructStub.__init__(self, tm, scope)
        TypedConstructStub.__init__(self, type)
        ReifiableConstructStub.__init__(self, None)
        DatatypeAwareConstructStub.__init__(self, value)

    def remove(self):
        self.reifier = None
        self._parent.remove_occurrence(self)


class NameStub(ScopedConstructStub, TypedConstructStub, ReifiableConstructStub):
    """\

    Derived classes must provide the following mutable attributes:
    - `variants` (a set)
    """
    _kind = kind.NAME
    
    def __init__(self, tm, type, value, scope=()):
        ScopedConstructStub.__init__(self, tm, scope)
        TypedConstructStub.__init__(self, type)
        ReifiableConstructStub.__init__(self, None)
        self._literal = value
        self.variants = self._create_variants()

    def _set_value(self, value):
        check_not_none(value)
        lit = Literal(value, XSD.string)
        if self._literal == lit:
            return
        self._fire_event(SetValue(self, self._literal, lit))
        self._literal = lit

    def create_variant(self, value, scope):
        def in_name_scope(theme):
            return theme in self.scope
        if not scope:
            raise ModelConstraintViolation('The variant must have a scope')
        if it.all(scope, in_name_scope):
            raise ModelConstraintViolation("The variant's scope is equal to the parent's scope")
        var = self._tm.builder.create_variant(Literal(value), scope)
        self.add_variant(var)
        return var

    def add_variant(self, child):
        assert child is not None
        if not _accept_child(self, child):
            return
        self._fire_event(AddVariant(self, child))
        child._parent = self
        self.variants.add(child)

    def remove_variant(self, child):
        assert child is not None
        if child._parent != self:
            return
        self._fire_event(RemoveVariant(self, child))
        self.variants.remove(child)
        child._parent = None

    def remove(self):
        self.reifier = None
        self._parent.remove_name(self)
        for var in tuple(self.variants):
            var.remove()

    literal = property(lambda self: self._literal)
    value = property(lambda self: self._literal.value, _set_value)


class VariantStub(ScopedConstructStub, ReifiableConstructStub, DatatypeAwareConstructStub):

    _kind = kind.VARIANT

    def __init__(self, tm, value, scope):
        ScopedConstructStub.__init__(self, tm, scope)
        ReifiableConstructStub.__init__(self, None)
        DatatypeAwareConstructStub.__init__(self, value)

    def _get_scope(self):
        scope = set(self._scope)
        if self._parent:
            scope = scope.union(self._parent.scope)
        return scope

    def _set_scope(self, scope):
        def in_name_scope(theme):
            return theme in self._parent.scope
        if is_topic(scope):
            scope = (scope,)
        if not scope:
            raise ModelConstraintViolation('The variant must have a scope')
        if it.all(scope, in_name_scope):
            raise ModelConstraintViolation("The variant's scope is equal to the parent's scope")
        new_scope = self._create_scope(scope)
        self._fire_event(SetScope(self, self._scope, new_scope))
        self._scope = new_scope

    def remove(self):
        self.reifier = None
        self._parent.remove_variant(self)

    scope = property(_get_scope, _set_scope)


def _check_attached(tmc):
    if not tmc._is_attached():
        raise ModelConstraintViolation('This Topic Maps construct is not attached to a topic map. Modification of the identity is not allowed')

def _accept_child(parent, child):
    if child._parent == parent:
        return False
    if child._parent is not None:
        raise ModelConstraintViolation('The Topic Maps construct "%r" has a parent' % child)
    return True

from mappa._internal.enhancer import enhance
enhance(TopicMapStub)
enhance(TopicStub)
enhance(AssociationStub)
enhance(RoleStub)
enhance(OccurrenceStub)
enhance(NameStub)
enhance(VariantStub)
