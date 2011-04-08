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
Provides some helper functions to ease the implementation of a backend.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD License
"""
from itertools import ifilter, imap
from mappa import TMDM, UCS
from mappa.utils import is_binary, involved_associations
from mappa.predicates import parent
from .utils import is_slo, is_uri, make_locator, strip_slo_prefix, random_id

def get_topic(tm, key):
    """\
    
    """
    if is_uri(key):
        return tm.topic(key)
    else:
        return tm.topic(make_locator(tm.iri, key))

def topic_by_identity(tm, *identity, **kw):
    """\

    """
    if identity:
        if len(identity) != 1:
            raise ValueError('Max. one identity argument expected.')
        identity = identity[0]
        if is_slo(identity):
            return tm.topic_by_slo(strip_slo_prefix(identity))
        return tm.topic_by_sid(identity) or tm.topic_by_iid(identity)
    if len(kw) == 1:
        for key, iri in kw.items():
            try:
                return getattr(tm, 'topic_by_%s' % key)(iri)
            except AttributeError:
                raise ValueError('Expected either one "sid", "slo", or "iid" keyword argument, got %r' % kw)
    else:
        raise ValueError('Expected either one "sid", "slo", or "iid" keyword argument, got %r' % kw)

def create_topic_by_identity(tm, *identity, **kw):
    """\

    """
    def random_iid():
        return make_locator(tm.iri, str(random_id()))
    if not identity and not kw: # Automatically assigned topic iid
        iid = random_iid()
        while tm.topic_by_iid(iid) or tm.topic_by_sid(iid):
            iid = random_iid()
        return tm.create_topic_by_iid(iid)
    topic = topic_by_identity(tm, *identity, **kw)
    if topic:
        return topic
    if identity:
        identity = identity[0]
        if is_slo(identity):
            return tm.create_topic_by_slo(strip_slo_prefix(identity))
        else:
            return tm.create_topic_by_sid(identity)
    if len(kw) == 1:
        for key, iri in kw.items():
            try:
                return getattr(tm, 'create_topic_by_%s' % key)(iri)
            except AttributeError:
                raise ValueError('Expected either one "sid", "slo", or "iid" keyword argument, got %r' % kw)
    else:
        raise ValueError('Expected either one "sid", "slo", or "iid" keyword argument, got %r' % kw)

def construct_by_identity(tm, *identity, **kw):
    """\
    Returns a construct by its item identifier or internal id.
    """
    if identity:
        identity = identity[0]
    if identity or kw.get('iid'):
        return tm.construct_by_iid(identity or kw.get('iid'))
    return tm.construct_by_id(kw.get('id'))

def _type_instance_topics(tm):
    """\
    Returns a tuple of topics: ``(tmdm:type-instance, tmdm:type, tmdm:instance)``.
    
    If one of the topics is not available in the topic map, this function
    raises a ``ValueError``
    """
    type_instance = tm.topic_by_sid(TMDM.type_instance)
    if not type_instance:
        raise ValueError()
    typ = tm.topic_by_sid(TMDM.type)
    if not typ:
        raise ValueError()
    instance = tm.topic_by_sid(TMDM.instance)
    if not instance:
        raise ValueError()
    return type_instance, typ, instance

def _supertype_subtype_topics(tm):
    """\
    Returns a tuple of topics: ``(tmdm:supertype-subtype, tmdm:supertype, tmdm:subtype)``.
    
    If one of the topics is not available in the topic map, this function
    raises a ``ValueError``
    """
    supertype_subtype = tm.topic_by_sid(TMDM.supertype_subtype)
    if not supertype_subtype:
        raise ValueError()
    supertype = tm.topic_by_sid(TMDM.supertype)
    if not supertype:
        raise ValueError()
    subtype = tm.topic_by_sid(TMDM.subtype)
    if not subtype:
        raise ValueError()
    return supertype_subtype, supertype, subtype

def topic_types(topic):
    """\
    Returns the topics which are the types of the specified ``topic``.
    
    This functions returns only those topics which play the ``tmdm:type``
    role in a ``tmdm:type-instance`` association where the ``topic`` plays 
    the ``tmdm:instance`` role. ``tmdm:supertype-subtype`` relationships are ignored.
    """
    try:
        type_instance, typ, instance = _type_instance_topics(topic.tm)
    except ValueError:
        return ()
    return _complementary_role_players(topic, type_instance, instance, typ)

def topic_instances(topic):
    """\
    Returns the topics which are instances of the specified ``topic``.
    
    This functions returns only those topics which play the ``tmdm:instance``
    role in a ``tmdm:type-instance`` association where the ``topic`` plays 
    the ``tmdm:type`` role. ``tmdm:supertype-subtype`` relationships are ignored.
    """
    try:
        type_instance, typ, instance = _type_instance_topics(topic.tm)
    except ValueError:
        return ()
    return _complementary_role_players(topic, type_instance, typ, instance)

def topic_supertypes(topic):
    try:
        supertype_subtype, supertype, subtype = _supertype_subtype_topics(topic.tm)
    except ValueError:
        return ()
    return _complementary_role_players(topic, supertype_subtype, subtype, supertype)

def topic_subtypes(topic):
    try:
        supertype_subtype, supertype, subtype = _supertype_subtype_topics(topic.tm)
    except ValueError:
        return ()
    return _complementary_role_players(topic, supertype_subtype, supertype, subtype)

def _complementary_role_players(topic, assoc_type, role_type, other_role_type, scope=UCS):
    """\
    Returns those role players which play the `other_role_type` in a *binary* 
    association of type `assoc_type`.
    """
    for assoc in ifilter(is_binary, involved_associations(topic, type=role_type, assoc_type=assoc_type, scope=scope)):
        for player in assoc.players_by(type=other_role_type):
            yield player

