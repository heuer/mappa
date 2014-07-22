# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
Utilities.

.. Note::

   In an application use the ``is_*`` functions (i.e. `is_topic`) instead of 
   ``isinstance(obj, SomeType)``

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD License
"""
import sys
from functools import partial
from operator import eq
from itertools import chain, imap
from mappa import ANY, TMDM, XSD, predicates as pred
from mappa._internal import it, kind

def atomify(tmc, ctx=ANY):
    """\
    Atomifies a Topic Maps construct. 
    For topic instances, an optional scope may be provided.
    """
    if is_topic(tmc):
        return tmc.__atomify__(ctx)
    return tmc.__atomify__()

def pyvalue(tmc):
    """\
    Returns the Python representation of the Topic Maps construct.
    
    .. Note:: 
       This method should work for occurrences, names and variants, 
       for all other Topic Maps constructs the behaviour is not specified.
    
    Raises a `TypeError` if the the object has no natural Python representant.
    """
    try:
        return tmc.__pyvalue__()
    except AttributeError:
        raise TypeError(sys.exc_info()[1])

def is_construct(obj):
    """\
    Returns if the object is a Topic Maps construct.
    """
    return _kind(obj) not in (None, kind.LITERAL)

def is_topicmap(tmc):
    """\
    Returns if the object is a topic map.
    """
    return _kind(tmc) is kind.TOPIC_MAP

def is_topic(tmc):
    """\
    Returns if the object is a topic.
    """
    return _kind(tmc) is kind.TOPIC

def is_association(tmc):
    """\
    Returns if the object is an association.
    """
    return _kind(tmc) is kind.ASSOCIATION

def is_role(tmc):
    """\
    Returns if the object is an association role.
    """
    return _kind(tmc) is kind.ROLE

def is_occurrence(tmc):
    """\
    Returns if the object is an occurrence.
    """
    return _kind(tmc) is kind.OCCURRENCE

def is_name(tmc):
    """\
    Returns if the object is a topic name.
    """
    return _kind(tmc) is kind.NAME

def is_variant(tmc):
    """\
    Returns if the object is a variant.
    """
    return _kind(tmc) is kind.VARIANT

def is_datatyped(tmc):
    """\
    Returns if the Topic Maps construct is an occurrence or a variant.
    """
    return _kind(tmc) in (kind.OCCURRENCE, kind.VARIANT)

def is_reifiable(tmc):
    """\
    Returns if the object is reifiable.
    
    Every Topic Maps construct that is not a topic, is reifiable.
    """
    return _kind(tmc) not in (kind.TOPIC, None) 

def is_typed(tmc):
    """\
    Returns if the object has a type (associations, roles, occurrences, 
    and names)
    """
    return _kind(tmc) in (kind.ASSOCIATION, kind.ROLE, kind.OCCURRENCE, kind.NAME)

def is_scoped(tmc):
    """\
    Returns if the object is scoped (associations, occurrences, names, 
    and variants)
    """
    return _kind(tmc) in (kind.ASSOCIATION, kind.OCCURRENCE, kind.NAME, kind.VARIANT)

def is_string(literal):
    """\
    Returns if the given `literal` has the datatype ``xsd:string``.
    """
    return literal.datatype == XSD.anyURI

def is_locator(literal):
    """\
    Returns if the given `literal` has the datatype ``xsd:anyURI``.
    """
    return literal.datatype == XSD.anyURI

def is_literal(obj):
    """\
    Returns if the object represents a literal.
    """
    return _kind(obj) is kind.LITERAL

def is_unary(assoc):
    """\
    Returns if the association is unary (contains 1 role).
    """
    return len(assoc) == 1

def is_binary(assoc):
    """\
    Returns if the association is binary (contains 2 roles).
    """
    return len(assoc) == 2

def is_ternary(assoc):
    """\
    Returns if the association is terary (contains 3 roles).
    """
    return len(assoc) == 3

def arity(assoc):
    """\
    Returns the arity (number of roles) of the association.
    """
    return len(assoc)

def is_associated(topic1, topic2, type=ANY): # pylint: disable-msg=W0622
    """\
    Returns if the specified topics play a role in the same association.
    If the `type` is not ``ANY``, the association type is also considered.
    """
    for assoc in imap(pred.parent, topic1.roles_played):
        if not has_type(assoc, type):
            continue
        for _, player in assoc:
            if player == topic2:
                return True
    return False

def involved_associations(topic, type=ANY, assoc_type=ANY, scope=ANY):
    """\
    Returns those association where the `topic` plays a role.
    
    `topic`
        The topic.
    `type`
        The type of the role the `topic` must play or ``ANY`` (default).
    `assoc_type`
        The association type or ``ANY`` (default).
    `scope`
        The scope of the association or ``ANY`` (default).
    """
    return imap(pred.parent, topic.roles_by(type=type, assoc_type=assoc_type, scope=scope))

def find_associated(topic, type=ANY, assoc_type=ANY, other_type=ANY, scope=ANY):
    """\
    Returns topics which play a role in the same association as ``topic``.
    
    `topic`
        The topic to find the associated topics for.
    `type`
        The optional role type indicates the role type the ``topic`` must play.
    `assoc_type`
        Indicates the association type.
    `other_type`
        Indicates the role type the "other" topics must play.
    `scope`
        Indicates the scope of the association.
    """
    for assoc in involved_associations(topic, type, assoc_type, scope):
        for player in assoc.players_by(type=other_type):
            if player != topic:
                yield player

def in_ucs(scoped):
    """\
    Returns if the scoped Topic Maps construct is in the unconstrained scope.
    """
    return it.no(scoped.scope)

def has_theme(scoped, theme):
    """\
    Returns if the scoped Topic Maps construct has the provided `theme` in its scope.
    
    `scoped`
        The scoped Topic Maps construct
    `theme`
        A topic
    """
    return theme in scoped.scope

def valid_in_scope(scoped, scope, exact=True):
    """\
    Returns if the scoped Topic Maps construct is valid in the provided scope.
    
    If the the scope is ``ANY`` this function returns ``True``. If the scoped
    Topic Maps construct is in the unconstrained scope, it returns ``True``.
    
    If `exact` is set to ``False`` (set to ``True`` by default), this function
    returns ``True`` if the provided `scope` is a subset of the construct's scope.
    """
    return in_ucs(scoped) or has_scope(scoped, scope, exact)

def has_scope(scoped, scope, exact=True):
    """\
    Returns if the scoped Topic Maps construct has the provided scope.
    
    If the scope is `ANY`, this function returns ``True``.
    
    .. Note:: 
       This function returns ``False`` for constructs in the 
       unconstrained scope, if the specified scope is not `UCS`.
    
    `scope`
        Either a topic or an iterable.
    `exact`
        Indicates if the `scoped` Topic Maps construct must have exactly
        the provided `scope`. If `exact` is set to ``False`` (default value: 
        ``True``), the `scoped` Topic Maps construct may have a subset of the 
        provided `scope`.
    """
    if scope is ANY:
        return True
    if is_topic(scope):
        scope = (scope,)
    if exact:
        return frozenset(scope) == frozenset(scoped.scope)
    return frozenset(scope).issubset(frozenset(scoped.scope))

def has_type(typed, type): # pylint: disable-msg=W0622
    """\
    Returns if the typed Topic Maps construct has the specified type.
    
    If ``type`` is ``ANY``, this function returns ``True`` regardless of the
    actual ``[type]`` property of ``typed``.
    """
    return type is ANY or typed.type == type

def ako(subtype, supertype):
    """\
    Creates a ``supertype-subtype`` relationship between `subtype` and `supertype`.
    """
    assert subtype.tm == supertype.tm
    subtype.add_supertype(supertype)

def isa(instance, type): # pylint: disable-msg=W0622
    """\
    Returns if `instance` is an instance of `type`.
    
    `instance`
        A topic, an association, a role, an occurrence or a name.
    `type`
        A topic.
    """
    if not is_topic(instance):
        return _typed_isa(instance, type)
    # 'instance' is a topic
    if type in instance.types:
        return True
    return iko(instance, type)

def _typed_isa(instance, type): # pylint: disable-msg=W0622
    return instance.type == type or _typed_iko(instance, type)

def iko(subtype, supertype):
    """\
    Returns if `subtype` is a subtype of `supertype`.
    
    `subtype`
        A topic, an association, a role, an occurrence or a name.
    `supertype`
        A topic.
    """
    if not is_topic(subtype):
        return _typed_iko(subtype, supertype)
    return it.exists(supertypes(subtype), partial(eq, supertype))

def _typed_iko(subtype, supertype):
    tm = subtype.tm
    return it.exists(_supertypes_of(subtype.type, 
                                 tm.topic(sid=TMDM.supertype_subtype), 
                                 tm.topic(sid=TMDM.supertype), 
                                 tm.topic(sid=TMDM.subtype)),
                              partial(eq, supertype))

def supertypes(subtype):
    """\
    Returns all supertypes of the specified `subtype`.
    
    `subtype`
        A topic.
    """
    tm = subtype.tm
    for typ in subtype.types:
        yield typ
        for supertype in _supertypes_of(typ, 
                                        tm.topic(sid=TMDM.supertype_subtype), 
                                        tm.topic(sid=TMDM.supertype), 
                                        tm.topic(sid=TMDM.subtype)):
            yield supertype

def subtypes(supertype):
    """\
    Returns all subtypes of the specified `supertype`.
    
    `supertype`
        A topic, an association, role, occurrence or name.
    """
    tm = supertype.tm
    return chain(tm.index.type_instance.topics(supertype), 
                 _subtypes_of(supertype, 
                              tm.topic(sid=TMDM.supertype_subtype), 
                              tm.topic(sid=TMDM.supertype), 
                              tm.topic(sid=TMDM.subtype)))

def _supertypes_of(topic, supertype_subtype, supertype, subtype):
    for assoc in imap(pred.parent, topic.roles_by(type=subtype, assoc_type=supertype_subtype)):
        for supertyp in assoc[supertype]:
            yield supertyp
            # The recursive call may violate the Python rec.limit?
            for super_super in _supertypes_of(supertyp, supertype_subtype, supertype, subtype):
                yield super_super

def _subtypes_of(topic, supertype_subtype, supertype, subtype):
    type_idx = topic.tm.index.type_instance
    for assoc in imap(pred.parent, topic.roles_by(type=supertype, assoc_type=supertype_subtype)):
        for subtyp in assoc[subtype]:
            yield subtyp
            for instance in type_idx.topics(subtyp):
                yield instance
            for subsub in _subtypes_of(subtyp, supertype_subtype, supertype, subtype):
                yield subsub

def is_default_name(name):
    """\
    Returns if the name has the type 
    ``http://psi.topicmaps.org/iso13250/model/topic-name``
    """
    return is_default_name_type(name.type)

def is_default_name_type(topic):
    """\
    Returns if the `topic` represents the default name type ``tmdm:topic-name``
    """
    return TMDM.topic_name in topic.sids

def topic_for(tmc):
    """\
    If the specified Topic Maps construct `tmc` is reified, the reifier is
    returned, if the Topic Maps construct is typed, the type is returned.
    
    If the Topic Maps construct is neither reified nor typed, `None` is returned.
    """
    return getattr(tmc, 'reified') or getattr(tmc, 'type')

def is_removable(topic):
    """\
    Returns if the specified ``topic`` is removable.
    """
    if not is_topic(topic):
        raise TypeError('Expected a topic')
    ti_idx = topic.tm.index.type_instance
    scope_idx = topic.tm.index.scoped
    return topic.reified is None \
            and it.no(topic.roles_played) \
            and it.no(ti_idx.associations(topic)) \
                    and it.no(ti_idx.roles(topic)) \
                    and it.no(ti_idx.occurrences(topic)) \
                    and it.no(ti_idx.names(topic)) \
            and it.no(scope_idx.associations_by_theme(topic)) \
                    and it.no(scope_idx.occurrences_by_theme(topic)) \
                    and it.no(scope_idx.names_by_theme(topic)) \
                    and it.no(scope_idx.variants_by_theme(topic))


import re
# Something that looks like an identifier which was invented by an human
_NICE_CHARS = re.compile(r'[a-zA-Z]+[\-\._\w]*')
del re

def nice_identifier(topic):
    """\
    Returns an identifier (part of an item identifier or subject identifier)
    from the topic which starts with the storage address of the parent topic map
    and looks like an human entered identifier.
    
    Returns either a string or ``None`` if no nice identifier was found.
    """
    base = topic.tm.iri
    locs = []
    for loc in chain(topic.iids, topic.sids):
        if loc.startswith(base):
            loc = loc.split(base)[1]
            if loc.startswith('#'):
                loc = loc.split('#')[1]
            if _NICE_CHARS.match(loc, 1):
                return loc
            else:
                locs.append(loc)
    return it.one_of(locs)

def remove_duplicates(topicmap):
    """\
    Removes duplicate Topic Maps constructs from the specified `topicmap`.
    
    `topicmap`
        The topic map to remove duplicates from.
    """
    try:
        topicmap._remove_duplicates() #pylint: disable-msg=W0212
    except AttributeError:
        from mappa._internal.dupremoval import remove_duplicates as remove_dups 
        remove_dups(topicmap)

def _kind(tmc):
    return getattr(tmc, '_kind', None)
