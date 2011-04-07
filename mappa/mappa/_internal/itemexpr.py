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
This module provides utility functions to enable access to Topic Maps properties
by using a dict-alike notation like topic['-'] = 'My Topic'.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD License
"""
from itertools import chain
from mappa import ANY, UCS, TMDM
from mappa.utils import is_topic
from mappa._internal.utils import is_slo, is_uri, make_locator

_AXIS_CHILD = 1
_AXIS_NAME = 2
_AXIS_TYPE = 3

class ItemExpr(object):
    """\
    Represents an expression.
    """
    __slots__ = ['_axis', '_type', '_scope']
    
    def __init__(self, expr):
        """\
        
        """
        axis = _axis(expr)
        if axis in (_AXIS_NAME, _AXIS_CHILD):
            expr = _strip_prefix(expr)
        self._axis = axis
        self._type, self._scope = _parse_type_scope(expr)

    def add_topic_child(self, topic, value):
        """\
        
        """
        def make_scope(scope):
            if scope in (ANY, UCS):
                return ()
            return _resolve_topics(topic.tm, scope, create=True)
        axis, typ, scope = self._axis, self._type, self._scope
        if axis is _AXIS_CHILD:
            raise ValueError()
        if axis is _AXIS_NAME:
            if typ is ANY:
                typ = TMDM.topic_name
            topic.create_name(type=_resolve_topic(topic.tm, typ, create=True),
                              value=value,
                              scope=make_scope(scope))
        elif axis is _AXIS_TYPE:
            if typ is ANY:
                raise ValueError('The type of the occurrence must be specified')
            topic.create_occurrence(type=_resolve_topic(topic.tm, typ, create=True),
                                    value=value,
                                    scope=make_scope(scope))

    def add_role(self, assoc, player):
        """\
        
        """
        axis, typ, scope = self._axis, self._type, self._scope
        assert scope is ANY
        if axis is not _AXIS_TYPE:
            raise ValueError()
        if typ is ANY:
            raise ValueError('The type of the role must be specified')
        tm = assoc.tm
        assoc.create_role(type=_resolve_topic(tm, typ, create=True), 
                          player=_resolve_topic(tm, player, create=True))

    def filter_topic_children(self, topic, child_axis=None):
        """\
        
        """
        axis, typ, scope = child_axis and _AXIS_CHILD or self._axis, self._type, self._scope
        if typ is not ANY:
            try:
                typ = _resolve_topic(topic.tm, typ)
            except ValueError:
                return ()
        if scope not in (ANY, UCS):
            try:
                scope = _resolve_topics(topic.tm, scope)
            except ValueError:
                return ()
        if axis is _AXIS_TYPE:
            return topic.occurrences_by(type=typ, scope=scope)
        elif axis is _AXIS_NAME:
            return topic.names_by(type=typ, scope=scope)
        else:
            assert axis is _AXIS_CHILD
            return chain(topic.occurrences_by(type=typ, scope=scope), topic.names_by(type=typ, scope=scope))

    def filter_players(self, assoc):
        """\
        
        """
        assert self._axis is _AXIS_TYPE and self._scope is ANY
        typ = self._type
        if typ is not ANY:
            try:
                typ = _resolve_topic(assoc.tm, typ)
            except ValueError:
                return ()
        return assoc.players_by(type=typ)

_cache = {}

def _compile(expr):
    """\
    
    """
    if not expr:
        raise ValueError('No expression provided')
    item_expr = _cache.get(expr)
    if item_expr:
        return item_expr
    item_expr = ItemExpr(expr)
    if len(_cache) >= 100:
        _cache.clear()
    _cache[expr] = item_expr
    return item_expr

def filter_topic_children(topic, expr, all_children=False):
    """\
    
    """
    return _compile(expr).filter_topic_children(topic, child_axis=all_children)

def add_topic_child(topic, value, expr):
    """\
    
    """
    return _compile(expr).add_topic_child(topic, value)

def filter_players(assoc, expr):
    """\
    
    """
    return _compile(expr).filter_players(assoc)

def add_role(assoc, player, expr):
    """\
    
    """
    return _compile(expr).add_role(assoc, player)

def _axis(expr):
    """\
    Returns an axis constant from the ``expr``.
    """
    if _is_name_axis(expr):
        return _AXIS_NAME
    if _is_child_axis(expr):
        return _AXIS_CHILD
    return _AXIS_TYPE

def _resolve_topic(tm, ident, create=False):
    """\
    Returns a topic from the topic map with the identity ``ident``.
    If no topic with the identity exists, a ``ValueError`` is raised unless
    ``create`` is ``True``.
    """
    if is_topic(ident):
        return ident
    t = None
    if is_slo(ident):
        slo = _strip_prefix(ident)
        if create:
            t = tm.create_topic_by_slo(slo)
        else:
            t = tm.topic_by_slo(slo)
    elif is_uri(ident):
        if create:
            t = tm.create_topic_by_sid(ident)
        else:
            t = tm.topic(ident)
    else:
        loc = make_locator(tm.iri, ident)
        if create:
            t = tm.create_topic_by_iid(loc)
        else:
            t = tm.topic(loc)
    if t is None:
        raise ValueError()
    return t

def _resolve_topics(tm, ids, create=False):
    """\
    Returns topics from the topic map with the identities ``ids``.
    If one of the identities cannot be resolved, a ``ValueError`` is raised 
    unless ``create`` is ``True``.
    """
    def resolve_topic(ident):
        return _resolve_topic(tm, ident, create)
    return [resolve_topic(ident) for ident in ids]

def _strip_prefix(string):
    """\
    Strips away any prefix like ``=``, ``*``, ``-`` from the provided string.
    """
    return string[1:].strip()

def _is_child_axis(string):
    """\
    Returns if the string starts with ``*``.
    """
    return isinstance(string, basestring) and string[0] == '*'

def _is_name_axis(string):
    """\
    Returns if the `string` starts with ``-``.
    """
    return isinstance(string, basestring) and string[0] == '-'

def _parse_type_scope(expr):
    """\
    Returns the type and scope from a string.
    
    >>> type, scope = _parse_type_scope('a')
    >>> type == 'a' and scope is ANY
    True
    >>> type, scope = _parse_type_scope('a ')
    >>> type == 'a' and scope is ANY
    True
    >>> _parse_type_scope('a @b')
    ('a', ['b'])
    >>> _parse_type_scope('a @b c')
    ('a', ['b', 'c'])
    >>> _parse_type_scope('a   @  b c  ')
    ('a', ['b', 'c'])
    >>> type, scope = _parse_type_scope('')
    >>> type is ANY and scope is ANY
    True
    >>> type, scope = _parse_type_scope('@b')
    >>> type is ANY and scope == ['b']
    True
    >>> type, scope = _parse_type_scope('  @b')
    >>> type is ANY and scope == ['b']
    True
    >>> type, scope = _parse_type_scope('@b c ')
    >>> type is ANY and scope == ['b', 'c']
    True
    >>> type, scope = _parse_type_scope('a @')
    >>> type == 'a' and scope is UCS
    True
    >>> type, scope = _parse_type_scope('= http://www.google.com/@')
    >>> type == '= http://www.google.com/' and scope is UCS
    True
    >>> type, scope = _parse_type_scope('@')
    >>> type is ANY and scope is UCS
    True
    """
    if is_topic(expr):
        return expr, ANY
    try:
        typ, scope = expr.split('@')
        scope = scope.split() or UCS
    except ValueError:
        typ = expr
        scope = ANY
    except AttributeError:
        return ANY, ANY
    return typ.strip() or ANY, scope


if __name__ == '__main__':
    import doctest
    doctest.testmod()

