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
This module provides functions to merge topic maps and topics.

.. Warning::

    This module does not belong to the public API.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD License
"""
from mappa import ModelConstraintViolation
from mappa.predicates import parent
from mappa._internal.constraints import check_same_topicmap

def merge_topicmaps(source, target):
    """\
    Merges the `source´ topic map with the `target` topic map.
    
    The `source` stays unmodified, only `target` will be modified.
    
    `source`
        A topic map instance.
    `target`
        A topic map instance.
    """
    def add_merge(source, target):
        """\
        Makes `source` equal with `target`.
        
        If `source` is already equal with some other topic, the other topic
        is merged with the `target` topic.
        """
        existing = mergemap.get(source)
        if existing:
            if existing != target:
                # The source topic is equals to another topic in the target topic map
                # Merge the topics in the target topic map.
                merge_topics(target, existing)
        else:
            # Remember the equality
            mergemap[source] = target
    if source == target:
        return
    # Mapping source.topic -> target.topic
    mergemap = {}
    for topic in source.topics:
        for slo in topic.slos:
            existing = target.topic(slo=slo)
            if existing:
                add_merge(topic, existing)
        for sid in topic.sids:
            existing = target.topic(sid=sid) or target.topic(iid=sid)
            if existing:
                add_merge(topic, existing)
        for iid in topic.iids:
            existing = target.topic(iid=iid) or target.topic(sid=iid)
            if existing:
                add_merge(topic, existing)
    for topic in source.topics:
        if not topic in mergemap:
            _copy_topic(topic, target, mergemap)
    for source_topic, target_topic in mergemap.iteritems():
        _copy_identities(source_topic.sids, source_topic.slos, source_topic.iids, target_topic)
        _copy_characteristics(source_topic, target_topic, mergemap)
    _copy_associations(source, target, mergemap)

def _copy_topic(topic, topicmap, mergemap):
    """\
    Copies the `topic` to the topic map `topicmap` and returns the
    topic in the target `topicmap`.
    """
    sids = tuple(topic.sids)
    slos = tuple(topic.slos)
    iids = tuple(topic.iids)
    target = None
    if sids:
        target = topicmap.create_topic(sid=sids[0])
        sids = sids[1:]
    if not target and slos:
        target = topicmap.create_topic(slo=slos[0])
        slos = slos[1:]
    if not target and iids:
        target = topicmap.create_topic(iid=iids[0])
        iids = iids[1:]
    assert(target)
    _copy_identities(sids, slos, iids, target)
    _copy_characteristics(topic, target, mergemap)
    return target

def _copy_identities(sids, slos, iids, target):
    """\
    Copies the identities of a topic to the `target` topic.
    
    `sids`
        The subject identifiers.
    `slos`
        The subject loctaors.
    `iids`
        The item identifiers.
    `target`
        The target topic.
    """
    add_sid = target.add_sid
    for sid in sids:
        add_sid(sid)
    add_slo = target.add_slo
    for slo in slos:
        add_slo(slo)
    _copy_iids(iids, target)

def _copy_iids(iids, target):
    """\
    Copies the item identifiers to the `target` Topic Maps construct.
    
    `iids`
        The item identifiers.
    `target`
        The target Topic Maps construct.
    """
    add_iid = target.add_iid
    for iid in iids:
        add_iid(iid)

def _copy_characteristics(topic, target, mergemap):
    """\
    Copies the occurrences and names from `topic` to the `target` topic.
    
    `topic`
        A topic instance to take the occurrences and names from.
    `target`
        A topic instance to add the occurrences and names to.
    `mergemap`
        The ``source.topic`` -> ``target.topic`` map.
    """
    def get_topic(topic):
        return mergemap.get(topic) or _copy_topic(topic, tm, mergemap)
    def get_scope(scoped):
        return [get_topic(theme) for theme in scoped.scope]
    tm = target.tm
    # target.occ.sig -> target.occ
    sigs = _signatures(target.occurrences)
    for occ in topic.occurrences:
        target_occ = target.create_occurrence(get_topic(occ.type), occ.literal, get_scope(occ))
        existing = sigs.get(target_occ.__sig__())
        if existing:
            target.remove_occurrence(target_occ)
            target_occ = existing
        target_occ.reifier = _copy_reifier(occ, tm, mergemap)
        _copy_iids(occ.iids, target_occ)
    # target.name.sig -> target.name
    sigs = _signatures(target.names)
    for name in topic.names:
        typ = get_topic(name.type)
        target_name = target.create_name(typ, name.value, get_scope(name))
        existing = sigs.get(target_name.__sig__())
        if existing:
            target.remove_name(target_name)
            target_name = existing
        target_name.reifier = _copy_reifier(name, tm, mergemap)
        _copy_iids(name.iids, target_name)
        vsigs = _signatures(target.variants)
        for var in name.variants:
            target_var = target.create_variant(var.literal, get_scope(var))
            existing = vsigs.get(target_var.__sig__())
            if existing:
                target_name.remove_variant(target_var)
                target_var = existing
            target_var.reifier = _copy_reifier(var, tm, mergemap)
            _copy_iids(var.iids, target_var)

def _copy_associations(source, target, mergemap):
    """\
    Copies all associations from the `source´ topic map to the `target` topic map.
    
    `source`
        A topic map instance (source of the associations).
    `target`
        A topic map instance (target for the associations).
    `mergemap`
        The ``source.topic`` -> ``target.topic`` map.
    """
    def get_topic(topic):
        return mergemap.get(topic) or _copy_topic(topic, target, mergemap)
    sigs = _signatures(target.associations)
    for assoc in source.associations:
        target_assoc = target.create_association(get_topic(assoc.type), [get_topic(theme) for theme in assoc.scope])
        for r_type, player in assoc:
            #TODO: Role iids, role reifier. Arrrg. :(
            target_assoc.create_role(get_topic(r_type), get_topic(player))
        existing = sigs.get(target_assoc.__sig__())
        if existing:
            target.remove_association(target_assoc)
            target_assoc = existing
        target_assoc.reifier = _copy_reifier(assoc, target, mergemap)
        _copy_iids(assoc.iids, target_assoc)

def _copy_reifier(reifiable, tm, mergemap):
    """\
    Copies the reifier of `reifiable` to the topic map `tm` iff it is not ``None``.
    
    If `reifiable` has a reifier, the equivalent topic in the target `tm` is
    returned, otherwise ``None`` is returned.
    """
    reifier = reifiable.reifier
    if reifier:
        return mergemap.get(reifier, None) or _copy_topic(reifier, tm, mergemap)
    return None


def merge_topics(source, target):
    """\
    Merges the `source` topic with the `target` topic.
    The `source` topic will be removed. This function does not create
    duplicate characteristics.
    """
    if source == target:
        return
    check_same_topicmap(source, target)
    if source.reified and target.reified:
        assert source.reified != target.reified # Should be enforced by the model
        raise ModelConstraintViolation('The topics cannot be merged. They reify different Topic Maps constructs')
    move_itemidentifiers(source, target)
    if source.reified:
        reified = source.reified
        reified.reifier = None
        reified.reifier = target
    for loc in tuple(source.sids):
        source.remove_sid(loc)
        target.add_sid(loc)
    for loc in tuple(source.slos):
        source.remove_slo(loc)
        target.add_slo(loc) 
    # Replace the `source` with `target` as type and theme
    _replace_topics(source, target)
    # Collecting occurrence signatures
    sigs = _signatures(target.occurrences)
    for occ in tuple(source.occurrences):
        existing = sigs.get(occ.__sig__())
        if existing:
            handle_existing(occ, existing)
            occ.remove()
            try:
                occ.__dict__ = existing.__dict__
            except AttributeError: 
                pass
        else:
            source.remove_occurrence(occ)
            target.add_occurrence(occ)
    # Collecting name signatures
    sigs = _signatures(target.names)
    for name in tuple(source.names):
        existing = sigs.get(name.__sig__())
        if existing:
            handle_existing(name, existing)
            move_variants(name, existing)
            name.remove()
            try:
                name.__dict__ = existing.__dict__
            except AttributeError:
                pass
        else:
            source.remove_name(name)
            target.add_name(name)
    # Collecting association signatures
    sigs = _signatures(map(parent, target.roles_played))
    # Note: Reifiers and and item identifiers are ignored at roles
    #TODO: Issue a warning that reifiers and iids are ignored?
    for role in tuple(source.roles_played):
        role.player = target
        existing = sigs.get(role.parent.__sig__())
        if existing:
            assoc = role.parent
            handle_existing(assoc, existing)
            assoc.remove()
            try:
                assoc.__dict__ = existing.__dict__
            except AttributeError:
                pass
    source.remove()
    try:
        source.__dict__ = target.__dict__
    except AttributeError:
        pass


def _signatures(iterable):
    """\
    Returns a dict {signature_of_obj_0: obj_0, signature_of_obj_1: obj_1, ...}
    """
    return dict([(e.__sig__(), e) for e in iterable])

def handle_existing(source, target):
    """\
    Called if some construct is equal to another (both have the same signature).
    """
    move_itemidentifiers(source, target)
    reifier = source.reifier
    if not reifier:
        return
    if target.reifier:
        source.reifier = None
        merge_topics(reifier, target.reifier)
    else:
        source.reifier = None
        target.reifier = reifier

def move_roles(source, target):
    """\
    Moves the roles from the `source` association to the `target` association.
    """
    sigs = _signatures(target.roles)
    for role in tuple(source.roles):
        existing = sigs.get(role.__sig__())
        if existing:
            handle_existing(role, existing)
        else:
            source.remove_role(role)
            target.add_role(role)

def move_role_properties(source, target):
    """\
    Moves the role properties from the `source` association to the `target` 
    association. It is assumed that source and target can be considered as 
    duplicate.
    """
    sigs = _signatures(target.roles)
    for role in tuple(source.roles):
        handle_existing(role, sigs[role.__sig__()])
        role.remove()

def move_variants(source, target):
    """\
    Moves the variants from the C{source} name to the C{target} name.
    """
    sigs = _signatures(target.variants)
    for var in tuple(source.variants):
        existing = sigs.get(var.__sig__())
        if existing:
            handle_existing(var, existing)
        else:
            source.remove_variant(var)
            target.add_variant(var)

def _replace_topics(topic, replacement):
    """\
    Replace the usage of `topic` as type or as theme with the 
    `replacement` topic.
    """
    tm = topic.tm
    # Replace every occurrence of `topic` as typing topic with `replacement`
    type_idx = tm.index.type_instance
    _replace_topic_as_type(replacement, type_idx.associations(topic))
    _replace_topic_as_type(replacement, type_idx.roles(topic))
    _replace_topic_as_type(replacement, type_idx.occurrences(topic))
    _replace_topic_as_type(replacement, type_idx.names(topic))
    # Replace every occurence of `topic` as theme with `replacement`
    scoped_idx = tm.index.scoped
    _replace_topic_as_theme(topic, replacement, scoped_idx.associations_by_theme(topic))
    _replace_topic_as_theme(topic, replacement, scoped_idx.occurrences_by_theme(topic))
    _replace_topic_as_theme(topic, replacement, scoped_idx.names_by_theme(topic))
    _replace_topic_as_theme(topic, replacement, scoped_idx.variants_by_theme(topic))

def _replace_topic_as_type(typ, typed_constructs):
    """\
    Sets `typ` as type for all `typed_constructs`.
    """
    for typed in tuple(typed_constructs):
        typed.type = typ

def _replace_topic_as_theme(old_theme, theme, scoped_constructs):
    """\
    Sets `theme` as replacement for `old_theme` for all `scoped_constructs`.
    """
    def new_scope(scope):
        l = list(scope)
        l.remove(old_theme)
        l.append(theme)
        return l
    for scoped in tuple(scoped_constructs):
        scoped.scope = new_scope(scoped.scope)

def move_itemidentifiers(source, target):
    """\
    Moves the item identifiers of `source` to `target`.
    """
    for iid in tuple(source.iids):
        source.remove_iid(iid)
        target.add_iid(iid)
