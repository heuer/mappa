# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\


:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
from tm import mio, XSD, TMDM

__all__ = ['MappingHandler']

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
        super(AbstractScopeTypeAwareMapper, self).__init__(name)
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

    @staticmethod
    def _handle_type(handler, type):
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
        super(AssociationMapper, self).__init__(u'rtm:association', scope=scope, type=type)
        if not subject_role:
            raise mio.MIOException('The subject role must be provided')
        if not object_role:
            raise mio.MIOException('The object role must be provided')
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
        super(OccurrenceMapper, self).__init__(u'rtm:occurrence', scope=scope, type=type)
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
        super(NameMapper, self).__init__(u'rtm:basename', scope=scope, type=type)
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
        super(TypeInstanceMapper, self).__init__(u'rtm:instance-of')

    def handle_object(self, handler, error_handler, subject, predicate_iri, obj, is_blank_node):
        handler.startIsa()
        handler.topicRef(_reference_from_object_iri(obj, is_blank_node))
        handler.endIsa()


class TypeInstanceScopedMapper(AbstractScopeTypeAwareMapper):
    """\
    rtm:instance-of implementation with an associated scope.
    """
    def __init__(self, scope):
        super(TypeInstanceScopedMapper, self).__init__(u'rtm:instance-of', scope=scope, type=_TYPE_INSTANCE)

    def handle_object(self, handler, error_handler, subject, predicate_iri, obj, is_blank_node):
        handler.startAssociation()
        self.type(handler)
        self.role(handler, _TYPE_INSTANCE_INSTANCE, subject)
        self.role(handler, _TYPE_INSTANCE_TYPE, _reference_from_object_iri(obj, is_blank_node))
        self.process_scope(handler)
        handler.endAssociation()


class SupertypeSubtypeMapper(AbstractScopeTypeAwareMapper):
    """\
    rtm:subtype-of implementation with an optional scope.
    """
    def __init__(self, scope):
        super(SupertypeSubtypeMapper, self).__init__(u'rtm:subtype-of', scope=scope, type=_SUPERTYPE_SUBTYPE)

    def handle_object(self, handler, error_handler, subject, predicate_iri, obj, is_blank_node):
        handler.startAssociation()
        self.type(handler)
        self.role(handler, _SUPERTYPE_SUBTYPE_SUBTYPE, subject)
        self.role(handler, _SUPERTYPE_SUBTYPE_SUPERTYPE, _reference_from_object_iri(obj, is_blank_node))
        self.process_scope(handler)
        handler.endAssociation()


class IdentityMapper(AbstractMapper):
    """\
    rtm:subject-identifier, rtm:subject-locator, and rtm:source-locator mapping
    implementation.
    """
    def __new__(cls, kind):
        attr = '_the_instance_%s' % kind
        if not attr in cls.__dict__:
            setattr(cls, attr, object.__new__(cls))
        return getattr(cls, attr)

    def __init__(self, kind):
        super(IdentityMapper, self).__init__(kind == mio.SUBJECT_IDENTIFIER and u'rtm:subject-identifier' \
                                             or kind == mio.SUBJECT_LOCATOR and u'rtm:subject-locator' \
                                             or kind == mio.ITEM_IDENTIFIER and u'rtm:item-identifier')
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

    def handleAssociation(self, predicate, subject_role, object_role, scope=None, type=None):
        self.mapping[predicate] = AssociationMapper(subject_role=_sid(subject_role),
                                                    object_role=_sid(object_role),
                                                    scope=_sids(scope), type=_sid(type))

    def handleOccurrence(self, predicate, scope=None, type=None, lang2scope=False):
        self.mapping[predicate] = OccurrenceMapper(scope=_sids(scope), type=_sid(type), lang2scope=lang2scope)

    def handleName(self, predicate, scope=None, type=None, lang2scope=False):
        self.mapping[predicate] = NameMapper(scope=_sids(scope), type=_sid(type), lang2scope=lang2scope)

    def handleInstanceOf(self, predicate, scope=None):
        if not scope:
            self.mapping[predicate] = TypeInstanceMapper()
        else:
            self.mapping[predicate] = TypeInstanceScopedMapper(scope=_sids(scope))

    def handleSubtypeOf(self, predicate, scope=None):
        self.mapping[predicate] = SupertypeSubtypeMapper(scope=_sids(scope))

    def handleSubjectIdentifier(self, predicate):
        self.mapping[predicate] = IdentityMapper(mio.SUBJECT_IDENTIFIER)

    def handleSubjectLocator(self, predicate):
        self.mapping[predicate] = IdentityMapper(mio.SUBJECT_LOCATOR)

    def handleItemIdentifier(self, predicate):
        self.mapping[predicate] = IdentityMapper(mio.ITEM_IDENTIFIER)


def _sids(iris):
    if not iris:
        return None
    return [(mio.SUBJECT_IDENTIFIER, iri) for iri in iris]


def _sid(iri):
    if not iri:
        return None
    return mio.SUBJECT_IDENTIFIER, iri

