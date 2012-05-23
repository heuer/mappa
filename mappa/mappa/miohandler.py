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
``tm.mio.handler.MapHandler`` implementation for Mappa.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD License
"""
from tm import mio, UCS, TMDM
import tm.mio.handler as mio_handler
from mappa import utils, ModelConstraintViolation, IdentityViolation
from mappa._internal import mergeutils, kind
from mappa.utils import _kind

__all__ = ['MappaMapHandler']

class MappaMapHandler(mio_handler.HamsterMapHandler):
    """\
    ``MapHandler`` implementation for Mappa.
    """
    __slots__ = ['_tm', '_delayed']

    def __init__(self, tm):
        """
        Initializes the handler with the given topic map.
        
        `tm`
            The topic map to operate upon.
        """
        super(MappaMapHandler, self).__init__()
        self._tm = tm
        self._delayed = {}

    def _create_topic_by_iid(self, iri):
        return self._tm.create_topic_by_iid(iri)

    def _create_topic_by_sid(self, iri):
        return self._tm.create_topic_by_sid(iri)

    def _create_topic_by_slo(self, iri):
        return self._tm.create_topic_by_slo(iri)

    def _handle_type_instance(self, instance, type):
        instance.add_type(type)

    def _handle_item_identifier(self, topic, iri):
        existing = self._tm.topic_by_iid(iri) or self._tm.topic_by_sid(iri)
        if existing and existing != topic:
            self._merge(topic, existing)
            topic = existing
        topic.add_iid(iri)

    def _handle_subject_identifier(self, topic, iri):
        existing = self._tm.topic_by_sid(iri) or self._tm.topic_by_iid(iri)
        if existing and existing != topic:
            self._merge(topic, existing)
            topic = existing
        topic.add_sid(iri)

    def _handle_subject_locator(self, topic, iri):
        existing = self._tm.topic_by_slo(iri)
        if existing and existing != topic:
            self._merge(topic, existing)
            topic = existing
        topic.add_slo(iri)

    def _handle_topicmap_item_identifier(self, iri):
        self._tm.add_iid(iri)

    def _handle_topicmap_reifier(self, reifier):
        self._tm.reifier = reifier

    def _merge(self, source, target):
        """\
        Merges the ``source`` topic into the ``target`` topic.
        """
        super(MappaMapHandler, self).notify_merge(source, target)
        target.merge(source)

    def _create_association(self, type, scope, reifier, iids, roles):
        assoc = self._tm.create_association(type, scope or UCS)
        delayed = self._delayed
        for r in roles:
            role = assoc.create_role(r.type, r.player)
            if r.reifier or r.iids:
                delayed[role.__sig__()] = r.reifier, r.iids
        assoc = _apply_reifier(assoc, reifier)
        _apply_iids(assoc, iids)
        if delayed:
            for role in tuple(assoc.roles):
                reifier, iids = delayed.get(role.__sig__(), (None, None))
                role = _apply_reifier(role, reifier)
                if iids:
                    _apply_iids(role, iids)
            delayed.clear()

    def _create_occurrence(self, parent, type, value, datatype, scope, reifier, iids):
        occ = parent.create_occurrence(type=type, value=(value, datatype), scope=scope or UCS)
        occ = _apply_reifier(occ, reifier)
        _apply_iids(occ, iids)

    def _create_name(self, parent, type, value, scope, reifier, iids, variants):
        name = parent.create_name(type=type or self._tm.create_topic_by_sid(TMDM.topic_name),
                                  value=value, scope=scope or UCS)
        name = _apply_reifier(name, reifier)
        _apply_iids(name, iids)
        delayed = self._delayed
        for v in variants:
            var = name.create_variant(value=(v.value, v.datatype), scope=v.scope)
            if v.reifier or v.iids:
                delayed[var.__sig__()] = v.reifier, v.iids
        if delayed:
            for variant in tuple(name.variants):
                reifier, iids = delayed.get(variant.__sig__(), (None, None))
                variant = _apply_reifier(variant, reifier)
                if iids:
                    _apply_iids(variant, iids)
            delayed.clear()


def _apply_reifier(reifiable, reifier):
    """\
    Sets the [reifier] property of ``reifiable`` to the specified ``reifier``
    iff ``reifier`` is not ```None``.
    """
    if not reifier:
        return reifiable
    try:
        reifiable.reifier = reifier
    except ModelConstraintViolation:
        existing = reifier.reified
        if existing != reifiable:
            if _mergable(reifiable, existing):
                _merge_reifiables(reifiable, existing)
                return existing
            else:
                raise mio.MIOException('The topic "%s" reifies another construct' % reifier)
    return reifiable

def _apply_iids(reifiable, iids):
    """\
    Adds the item identifiers ``iids`` to the specified ``reifiable``.
    """
    for iid in iids:
        try:
            reifiable.add_iid(iid)
        except IdentityViolation, ex:
            existing = ex.existing
            if _mergable(reifiable, existing):
                _merge_reifiables(reifiable, existing)
            else:
                raise mio.MIOException('The item identifier "%s" is already assigned to another construct' % iid)

def _mergable(a, b):
    """\
    Returns if the constructs a and b are mergable.
    """
    kind_a = _kind(a)
    res = _kind(b) == kind_a and a.__sig__() == b.__sig__()
    if kind_a in (kind.ROLE, kind.VARIANT):
        res = res and a.parent.__sig__() == b.parent.__sig__()
    return res

def _merge_reifiables(source, target):
    """\
    Merges the ``source`` into ``target``.
    
    This function is meant to merge statements, not topics! Further, this
    function silently assumes that both statements are mergable but DOES NOT 
    check it; use `_mergable` for that purpose.
    """
    mergeutils.handle_existing(source, target)
    if utils.is_role(source):
        source_parent, target_parent = source.parent, target.parent
        if source_parent != target_parent:
            mergeutils.handle_existing(source_parent, target_parent)
            mergeutils.move_roles(source_parent, target_parent)
            source_parent.remove()
            try:
                source_parent.__dict__ = target_parent.__dict__
            except AttributeError:
                pass
    elif utils.is_variant(source):
        source_parent, target_parent = source.parent, target.parent
        if source_parent != target_parent:
            mergeutils.handle_existing(source_parent, target_parent)
            mergeutils.move_variants(source_parent, target_parent)
            source_parent.remove()
            try:
                source_parent.__dict__ = target_parent.__dict__
            except AttributeError:
                pass
    else:
        if utils.is_association(source):
            mergeutils.move_role_properties(source, target)
        elif utils.is_name(source):
            mergeutils.move_variants(source, target)
        source.remove()
        try:
            source.__dict__ = target.__dict__
        except AttributeError:
            pass
