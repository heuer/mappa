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
#     * Neither the project name nor the names of the contributors may be 
#       used to endorse or promote products derived from this software 
#       without specific prior written permission.
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


:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
from tm import mio, XSD, TMDM

_TYPE_INSTANCE = mio.SUBJECT_IDENTIFIER, TMDM.type_instance
_TYPE_INSTANCE_TYPE = mio.SUBJECT_IDENTIFIER, TMDM.type
_TYPE_INSTANCE_INSTANCE = mio.SUBJECT_IDENTIFIER, TMDM.instance
_SUPERTYPE_SUBTYPE = mio.SUBJECT_IDENTIFIER, TMDM.supertype_subtype
_SUPERTYPE_SUBTYPE_SUPERTYPE = mio.SUBJECT_IDENTIFIER, TMDM.supertype
_SUPERTYPE_SUBTYPE_SUBTYPE = mio.SUBJECT_IDENTIFIER, TMDM.subtype

def _reference_from_object_iri(iri, is_blank_node):
    """\
    Returns either an item identifier (iff the IRI is a blank node)
    or subject identifier.
    """
    return mio.ITEM_IDENTIFIER, iri if is_blank_node else mio.SUBJECT_IDENTIFIER, iri 

class AbstractMapper(object):
    """\
    Common superclass for IMappers
    """
    def __init__(self, name):
        """\

        `name`
            The name of the mapper
        """
        self.name = name

    def handle_literal(self, handler, error_handler, subject, predicate_iri, value, datatype, language):
        """\
        Rejects the literal.
        """
        error_handler.reject_literal(self.name, value, datatype)

    def handle_object(self, handler, error_handler, subject, predicate_iri, obj, is_blank_node):
        """\
        Rejects an object
        """
        error_handler.reject_nonliteral(self.name, obj)

class AbstractScopeTypeAwareMapper(AbstractMapper):
    """\

    """
    def __init__(self, name, scope=None, type=None):
        """\

        `name`
            Name of the mapper
        `scope`
            The scope.
        `type`
            The type.
        """
        super(name)
        self._scope = scope if scope else None
        self._type = type

    def type(self, handler, pred=None):
        """
        Issues a ``IMapHandler#startType()``, ``IMapHandler#topicRef()``,
        ``IMapHandler#endType()`` event sequence.

        This method uses either a subject identifier reference from the provided
        `pred` or the overridden type (in case of a
        ``rdf-predicate rtm:type subject-identifier`` statment).

        `handler`
            The IMapHandler instance.
        `pred`
            A subject identifier reference or ``None``.
        """
        type_ = self._type if self._type else mio.SUBJECT_IDENTIFIER, pred
        self._handle_type(handler, type_)

    def _handle_type(self, handler, type):
        handler.startType()
        handler.topicRef(type)
        handler.endType()

    def role(self, handler, type, player):
        """\
        Issues events to the `handler` which create a role with the provided
        `type` and `player`.

        `handler`
            The handler which receives the events.
        `type`
            The role type
         `player`
             The role player
        """
        handler.startRole()
        self._handle_type(handler, type)
        handler.startPlayer()
        handler.topicRef(player)
        handler.endPlayer()
        handler.endRole()

    def process_scope(self, handler, additional_theme=None):
        """\
        Processes the scope, if any.

        This method must be called from the derived classes to process the scope.
        """
        scope = self._scope
        if not scope and not additional_theme:
            return
        handler.startScope()
        if additional_theme:
            handler.startTheme()
            handler.topicRef(additional_theme)
            handler.endTheme()
        if scope:
            for theme in scope:
                handler.startTheme()
                handler.topicRef(theme)
                handler.endTheme()
        handler.endScope()
        

class AssociationMapper(AbstractScopeTypeAwareMapper):
    """\
    rtm:association implementation.
    """
    def __init__(self, subject_role, object_role, scope=None, type=None):
        """\
        
        """
        super(AssociationMapper, self).__init__('rtm:association', scope=scope, type=type)
        if not subject_role:
            raise ValueError('The subject role must be provided')
        if not object_role:
            raise ValueError('The object role must be provided')
        self._subject_role = subject_role
        self._object_role = object_role

    def handle_object(self, handler, error_handler, subject, predicate_iri, obj, is_blank_node):
        handler.startAssociation()
        self.type(handler, predicate_iri)
        self.role(handler, self._subject_role, subject)
        self.role(handler, self._object_role, _reference_from_object_iri(obj, is_blank_node))
        self.process_scope(handler)
        handler.endAssociation()


class OccurrenceMapper(AbstractScopeTypeAwareMapper):
    """\
    rtm:occurrence implementation.
    """
    def __init__(self, scope=None, type=None, lang2scope=False):
        """\

        """
        super(OccurrenceMapper, self).__init__('rtm:occurrence', scope=scope, type=type)
        self._lang2scope = lang2scope

    def handle_literal(self, handler, error_handler, subject, predicate_iri, value, datatype, language):
        handler.startOccurrence()
        self.type(handler, predicate_iri)
        handler.value(value, datatype)
        self.process_scope(handler, language if self._lang2scope else None)
        handler.endOccurrence()

    def handle_object(self, handler, error_handler, subject, predicate_iri, obj, is_blank_node):
        if is_blank_node:
            error_handler.reject_blank_node(self.name)
        else:
            self.handle_literal(handler, error_handler, subject, predicate_iri, obj, XSD.anyURI, None)       


class NameMapper(AbstractScopeTypeAwareMapper):
    """\
    rtm:basename implementation.
    """
    def __init__(self, scope=None, type=None, lang2scope=False):
        """\

        """
        super(NameMapper, self).__init__('rtm:basename', scope=scope, type=type)
        self._lang2scope = lang2scope

    def handle_literal(self, handler, error_handler, subject, predicate_iri, value, datatype, language):
        handler.startName()
        self.type(handler, predicate_iri)
        handler.value(value)
        self.process_scope(handler, language if self._lang2scope else None)
        handler.endName()


class TypeInstanceMapper(AbstractMapper):
    """\
    rtm:instance-of implementation (unconstrained scope)
    """
    def __new__(cls):
        if not '_the_instance' in cls.__dict__:
            cls._the_instance = object.__new__(cls)
        return cls._the_instance

    def __init__(self):
        super(TypeInstanceMapper, self).__init__('rtm:instance-of')

    def handle_object(self, handler, error_handler, subject, predicate_iri, obj, is_blank_node):
        handler.startIsa()
        handler.topicRef(_reference_from_object_iri(obj, is_blank_node));
        handler.endIsa()


class TypeInstanceScopedMapper(AbstractScopeTypeAwareMapper):
    """\
    rtm:instance-of implementation with an associated scope.
    """
    def __init__(self, scope):
        super(TypeInstanceScopedMapper, self).__init__('rtm:instance-of', scope=scope, type=_TYPE_INSTANCE)

    def handle_object(self, handler, error_handler, subject, predicate_iri, obj, is_blank_node):
        handler.startAssociation()
        self.type(handler)
        self.role(handler, _TYPE_INSTANCE_INSTANCE, subject);
        self.role(handler, _TYPE_INSTANCE_TYPE, _reference_from_object_iri(obj, is_blank_node))
        self.process_scope(handler)
        handler.endAssociation()


class SupertypeSubtypeMapper(AbstractScopeTypeAwareMapper):
    """\
    rtm:subtype-of implementation with an optional scope.
    """
    def __init__(self, scope):
        super(SupertypeSubtypeMapper, self).__init__('rtm:subtype-of', scope=scope, type=_SUPERTYPE_SUBTYPE)

    def handle_object(self, handler, error_handler, subject, predicate_iri, obj, is_blank_node):
        handler.startAssociation()
        self.type(handler)
        self.role(handler, _SUPERTYPE_SUBTYPE_SUBTYPE, subject);
        self.role(handler, _SUPERTYPE_SUBTYPE_SUPERTYPE, _reference_from_object_iri(obj, is_blank_node))
        self.process_scope(handler)
        handler.endAssociation()


class IdentityMapper(AbstractMapper):
    """\
    rtm:subject-identifier, rtm:subject-locator, and rtm:source-locator mapping implementation.
    """
    def __new__(cls, kind):
        attr = '_the_instance_%s' % kind
        if not attr in cls.__dict__:
            setattr(cls, attr, object.__new__(cls))
        return getattr(cls, attr)

    def __init__(self, kind):
        super(IdentityMapper, self).__init__(kind == mio.SUBJECT_IDENTIFIER and 'rtm:subject-identifier' \
                                             or kind == mio.SUBJECT_LOCATOR and 'rtm:subject-locator' \
                                             or kind == mio.ITEM_IDENTIFIER and 'rtm:item-identifier')
        self._kind = kind

    def handle_object(self, handler, error_handler, subject, predicate_iri, obj, is_blank_node):
        if is_blank_node:
            error_handler.reject_blank_node(self.name)
        else:
            if mio.SUBJECT_IDENTIFIER == self._kind:
                handler.subjectIdentifier(obj)
            elif mio.SUBJECT_LOCATOR == self._kind:
                handler.subjectLocator(obj)
            else:
                handler.itemIdentifier(obj)

class MappingHandler(object):
    """\
    Default IMappingHandler implementation that keeps the mapping in-memory.
    """
    def __init__(self):
        self.mapping = {}

    def start(self):
        pass

    def end(self):
        pass

    def handleComment(self, comment):
        pass
    
    def handlePrefix(self, prefix, iri):
        pass

    def handleAssociation(self, predicate, subject_role, object_role, scope, type):
        if not subject_role:
            raise mio.MIOException('The subject role must be provided')
        if not object_role:
            raise mio.MIOException('The object role must be provided')
        self.mapping[predicate] = AssociationMapper(_sid(subject_role), _sid(object_role), scope=_sids(scope), type=_sid(type))

    def handleOccurrence(self, predicate, scope, type, lang2scope=False):
        self.mapping[predicate] = OccurreneMapper(scope=_sids(scope), type=_sid(type), lang2scope=lang2scope)

    def handleName(self, predicate, scope, type, lang2scope=False):
        self.mapping[predicate] = NameMapper(scope=_sids(scope), type=_sid(type), lang2scope=lang2scope)

    def handleInstanceOf(self, predicate, scope):
        self.mapping[predicate] = TypeInstanceMapper() if not scope else TypeInstanceScopedMapper(scope=_sids(scope))

    def handleSubtypeOf(self, predicate, scope):
        self.mapping[predicate] = SupertypeSubtypeMapper(scope=_sids(scope))

    def handleSubjectIdentifier(self, predicate):
        self.mapping[predicate] = IdentityMapper(mio.SUBJECT_IDENTIFIER)

    def handleSubjectLocator(self, predicate):
        self.mapping[predicate] = IdentityMapper(mio.SUBJECT_LOCATOR)

    def handleItemIdentifier(self, predicate):
        self.mapping[predicate] = IdentityMapper(mio.ITEM_IDENTIFIER)

def _sids(iris):
    return None if not iris else [(mio.SUBJECT_IDENTIFIER, iri) for iri in coll]

def _sid(iri):
    return mio.SUBJECT_IDENTIFIER, iri if iri else None

