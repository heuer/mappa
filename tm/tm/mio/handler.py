# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
The PyTM MIO package.

This is more or less a straight port of the Java MIO package to Python.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
import logging
from tm import mio, TMDM, XSD

_DEFAULT_NAME_TYPE = mio.SUBJECT_IDENTIFIER, TMDM.topic_name


class MapHandler(object):
    """\
    Handler which receives notifications about Topic Maps constructs.
    """
    __slots__ = []

    def startTopicMap(self):
        """\
        Notification about the beginning of a topic map.
        
        This method is only called once.

        This method MUST NOT be called if a parser acts as subparser (i.e. if
        another serialized topic map is included into the current topic map via
        a mergemap directive or include directive). 
        """

    def endTopicMap(self):
        """\
        Notification about the end of a topic map.
        
        This method is only called once.
        This method MUST be called by the parser even if it detects an 
        irrevocable error during processing a topic map.
        
        This method MUST NOT be called if a parser acts as subparser (i.e. if
        another serialized topic map is included into the current topic map via
        a mergemap directive or include directive). 
        """

    def startTopic(self, identity):
        """\
        Notification about the start of a topic.
        
        `identity`
            A tuple consisting of an identifier kind constant and an IRI.
        """

    def endTopic(self):
        """\
        Notification about the end of a topic declaration.
        """

    def topicRef(self, identity):
        """\
        Notification about a topic reference.
        
        The interpretation of the topic reference depends on the context (i.e.
        after a `startType`, `startPlayer`, or a `startTheme` event).
        
        `identity`
            A tuple consisting of an identifier kind constant and an IRI.
        """

    def subjectIdentifier(self, iri):
        """\
        Reports a subject identifier.
        
        The subject identifier is an absolute IRI which should be added to the
        currently processed topic.
        
        `iri`
            A string representing an absolute IRI.
        """

    def subjectLocator(self, iri):
        """\
        Reports a subject locator.
        
        The subject locator is an absolute IRI which should be added to the
        currently processed topic.
        
        `iri`
            A string representing an absolute IRI.
        """

    def itemIdentifier(self, iri):
        """\
        Reports an item identifier.
        
        The item identifier is an absolute IRI which should be added to the
        currently processed Topic Maps construct.
        
        `iri`
            A string representing an absolute IRI.
        """

    def startAssociation(self):
        """\
        Notification about the start of an association.
        """

    def endAssociation(self):
        """\
        Notification about the end of an association.
        """

    def startRole(self):
        """\
        Notification about the start of a role.
        """

    def endRole(self):
        """\
        Notification about the end of a role.
        """

    def startOccurrence(self):
        """\
        Notification about the start of an occurrence.
        """

    def endOccurrence(self):
        """\
        Notification about the end of an occurrence.
        """

    def startName(self):
        """\
        Notification about the start of a name.
        """

    def endName(self):
        """\
        Notification about the end of a name.
        
        If there was no ``startType`` .. ``endType`` event, the implementation
        MUST assume that the name has the default name type.
        """

    def startVariant(self):
        """\
        Notification about the start of a variant.
        
        The parser guarantees that the scope of the name has been parsed.
        The scope of the name is not part of the scope of the variant.
        """

    def endVariant(self):
        """\
        Notification about the end of a variant.
        
        If the scope of the variant is not the superset of the name to which
        the variant belongs, this method MUST throw a ``MIOException``.
        """

    def startScope(self):
        """\
        Notification about the start of scope processing.
        
        This method is either called once for a scoped construct or never.
        """

    def endScope(self):
        """\
        Notification about the end of scope processing.
        """

    def startTheme(self):
        """\
        Notification about the start of a theme declaration.
        """

    def endTheme(self):
        """\
        Notification about the end of a theme declaration.
        """

    def startType(self):
        """\
        Notification about the start of a type declaration.
        """

    def endType(self):
        """\
        Notification about the end of a type declaration.
        """

    def startPlayer(self):
        """\
        Notification about the start of a player declaration.
        """

    def endPlayer(self):
        """\
        Notification about the end of a player declaration.
        """

    def startReifier(self):
        """\
        Notification about the start of a reifier declaration.
        """

    def endReifier(self):
        """\
        Notification about the end of a reifier declaration.
        """

    def startIsa(self):
        """\
        Notification about the the start of ``type-instance`` relationships.
        
        After this event there may occurr at minimum one `topicRef` 
        or one `startTopic` (with the correspondending `endTopic`
        event.
        
        The reported topics after a `startIsa` event are meant as
        type of the currently parsed topic.
        
        Outside of a topic context, this notification is illegal.
        """

    def endIsa(self):
        """\
        Notification about the end of the ``type-instance`` relationships.
        """

    def value(self, string, datatype=None):
        """\
        Reports either a value for an occurrence, a name or a variant.
        
        If a value for a name is reported, the `datatype` MUST be ``None``.
        
        `string`
            The value.
        `datatype`
            The datatype IRI or ``None`` if a name value is reported.
        """


class DelegatingMapHandler(MapHandler):
    """\
    A ``MapHandler`` implementation that does nothing but delegates all events 
    to an underlying ``MapHandler`` instance.
    """
    __slots__ = ['_handler']
    
    def __init__(self, handler):
        super(DelegatingMapHandler, self).__init__()
        self._handler = handler

    def startTopicMap(self):
        self._handler.startTopicMap()

    def endTopicMap(self):
        self._handler.endTopicMap()

    def startTopic(self, identity):
        self._handler.startTopic(identity)

    def endTopic(self):
        self._handler.endTopic()

    def topicRef(self, identity):
        self._handler.topicRef(identity)

    def subjectIdentifier(self, iri):
        self._handler.subjectIdentifier(iri)

    def subjectLocator(self, iri):
        self._handler.subjectLocator(iri)

    def itemIdentifier(self, iri):
        self._handler.itemIdentifier(iri)

    def startAssociation(self):
        self._handler.startAssociation()

    def endAssociation(self):
        self._handler.endAssociation()

    def startRole(self):
        self._handler.startRole()

    def endRole(self):
        self._handler.endRole()

    def startOccurrence(self):
        self._handler.startOccurrence()

    def endOccurrence(self):
        self._handler.endOccurrence()

    def startName(self):
        self._handler.startName()

    def endName(self):
        self._handler.endName()

    def startVariant(self):
        self._handler.startVariant()

    def endVariant(self):
        self._handler.endVariant()

    def startScope(self):
        self._handler.startScope()

    def endScope(self):
        self._handler.endScope()

    def startTheme(self):
        self._handler.startTheme()

    def endTheme(self):
        self._handler.endTheme()

    def startType(self):
        self._handler.startType()

    def endType(self):
        self._handler.endType()

    def startPlayer(self):
        self._handler.startPlayer()

    def endPlayer(self):
        self._handler.endPlayer()

    def startReifier(self):
        self._handler.startReifier()

    def endReifier(self):
        self._handler.endReifier()

    def startIsa(self):
        self._handler.startIsa()

    def endIsa(self):
        self._handler.endIsa()

    def value(self, val, datatype=None):
        self._handler.value(val, datatype)


class LoggingMapHandler(MapHandler):
    """\
    A MapHandler which logs all events and delegates the events to
    an underlying MapHandler instance.
    """
    __slots__ = ['level', '_handler', '_logging_function', '_level']

    def __init__(self, handler, level=logging.INFO):
        """\
        `handler`
            The MapHandler instance which should receive the events.
        `level`
            The logging level (default: logging.INFO)
        """
        self._handler = handler
        self._logging_function = None
        self.level = level

    def startTopicMap(self):
        self._logging_function(u'startTopicMap')
        self._handler.startTopicMap()

    def endTopicMap(self):
        self._logging_function(u'endTopicMap')
        self._handler.endTopicMap()

    def startTopic(self, identity):
        self._logging_function(u'startTopic, kind=%r, iri=%r' % identity)
        self._handler.startTopic(identity)

    def endTopic(self):
        self._logging_function(u'endTopic')
        self._handler.endTopic()

    def topicRef(self, identity):
        self._logging_function(u'topicRef, kind=%r, iri=%r' % identity)
        self._handler.topicRef(identity)

    def subjectIdentifier(self, iri):
        self._logging_function(u'subjectIdentifier, iri=%r' % iri)
        self._handler.subjectIdentifier(iri)

    def subjectLocator(self, iri):
        self._logging_function(u'subjectLocator, iri=%r' % iri)
        self._handler.subjectLocator(iri)

    def itemIdentifier(self, iri):
        self._logging_function(u'itemIdentifier, iri=%r' % iri)
        self._handler.itemIdentifier(iri)

    def startAssociation(self):
        self._logging_function(u'startAssociation')
        self._handler.startAssociation()

    def endAssociation(self):
        self._logging_function(u'endAssociation')
        self._handler.endAssociation()

    def startRole(self):
        self._logging_function(u'startRole')
        self._handler.startRole()

    def endRole(self):
        self._logging_function(u'endRole')
        self._handler.endRole()

    def startOccurrence(self):
        self._logging_function(u'startOccurrence')
        self._handler.startOccurrence()

    def endOccurrence(self):
        self._logging_function(u'endOccurrence')
        self._handler.endOccurrence()

    def startName(self):
        self._logging_function(u'startName')
        self._handler.startName()

    def endName(self):
        self._logging_function(u'endName')
        self._handler.endName()

    def startVariant(self):
        self._logging_function(u'startVariant')
        self._handler.startVariant()

    def endVariant(self):
        self._logging_function(u'endVariant')
        self._handler.endVariant()

    def startScope(self):
        self._logging_function(u'startScope')
        self._handler.startScope()

    def endScope(self):
        self._logging_function(u'endScope')
        self._handler.endScope()

    def startTheme(self):
        self._logging_function(u'startTheme')
        self._handler.startTheme()

    def endTheme(self):
        self._logging_function(u'endTheme')
        self._handler.endTheme()

    def startType(self):
        self._logging_function(u'startType')
        self._handler.startType()

    def endType(self):
        self._logging_function(u'endType')
        self._handler.endType()

    def startPlayer(self):
        self._logging_function(u'startPlayer')
        self._handler.startPlayer()

    def endPlayer(self):
        self._logging_function(u'endPlayer')
        self._handler.endPlayer()

    def startReifier(self):
        self._logging_function(u'startReifier')
        self._handler.startReifier()

    def endReifier(self):
        self._logging_function(u'endReifier')
        self._handler.endReifier()

    def startIsa(self):
        self._logging_function(u'startIsa')
        self._handler.startIsa()

    def endIsa(self):
        self._logging_function(u'endIsa')
        self._handler.endIsa()

    def value(self, val, datatype=None):
        self._logging_function(u'value val=%r, datatype=%r' % (val, datatype))
        self._handler.value(val, datatype)

    def _set_level(self, level):
        self._level = level
        self._logging_function = getattr(logging, logging.getLevelName(level).lower())

    level = property(lambda self: self._level, _set_level)


class NoTopicMapEventsMapHandler(DelegatingMapHandler):
    """\
    A ``MapHandler`` implementation where the `startTopicMap` and `endTopicMap`
    events are not delegated to the underlying `MapHandler`. They do nothing by
    default.
    To issue the events, call `start_tm` and `end_tm`.
    """
    __slots__ = ['_handler']
    
    def __init__(self, handler):
        super(NoTopicMapEventsMapHandler, self).__init__(handler)

    def startTopicMap(self):
        pass

    def endTopicMap(self):
        pass

    def start_tm(self):
        """\
        Issues the `startTopicMap` event to the underlying MapHandler.
        """
        self._handler.startTopicMap()

    def end_tm(self):
        """\
        Issues the `endTopicMap` event to the underlying MapHandler.
        """
        self._handler.endTopicMap()


class TeeMapHandler(MapHandler):
    """\
    A ``MapHandler`` implementation that does nothing but delegates all events 
    to two underlying ``MapHandler`` instance.
    """
    __slots__ = ['_first', '_second']
    
    def __init__(self, first, second):
        super(TeeMapHandler, self).__init__()
        self._first = first
        self._second = second

    def startTopicMap(self):
        self._first.startTopicMap()
        self._second.startTopicMap()

    def endTopicMap(self):
        self._first.endTopicMap()
        self._second.endTopicMap()

    def startTopic(self, identity):
        self._first.startTopic(identity)
        self._second.startTopic(identity)

    def endTopic(self):
        self._first.endTopic()
        self._second.endTopic()

    def topicRef(self, identity):
        self._first.topicRef(identity)
        self._second.topicRef(identity)

    def subjectIdentifier(self, iri):
        self._first.subjectIdentifier(iri)
        self._second.subjectIdentifier(iri)

    def subjectLocator(self, iri):
        self._first.subjectLocator(iri)
        self._second.subjectLocator(iri)

    def itemIdentifier(self, iri):
        self._first.itemIdentifier(iri)
        self._second.itemIdentifier(iri)

    def startAssociation(self):
        self._first.startAssociation()
        self._second.startAssociation()

    def endAssociation(self):
        self._first.endAssociation()
        self._second.endAssociation()

    def startRole(self):
        self._first.startRole()
        self._second.startRole()

    def endRole(self):
        self._first.endRole()
        self._second.endRole()
    
    def startOccurrence(self):
        self._first.startOccurrence()
        self._second.startOccurrence()

    def endOccurrence(self):
        self._first.endOccurrence()
        self._second.endOccurrence()

    def startName(self):
        self._first.startName()
        self._second.startName()

    def endName(self):
        self._first.endName()
        self._second.endName()

    def startVariant(self):
        self._first.startVariant()
        self._second.startVariant()

    def endVariant(self):
        self._first.endVariant()
        self._second.endVariant()

    def startScope(self):
        self._first.startScope()
        self._second.startScope()

    def endScope(self):
        self._first.endScope()
        self._second.endScope()

    def startTheme(self):
        self._first.startTheme()
        self._second.startTheme()

    def endTheme(self):
        self._first.endTheme()
        self._second.endTheme()

    def startType(self):
        self._first.startType()
        self._second.startType()

    def endType(self):
        self._first.endType()
        self._second.endType()

    def startPlayer(self):
        self._first.startPlayer()
        self._second.startPlayer()

    def endPlayer(self):
        self._first.endPlayer()
        self._second.endPlayer()

    def startReifier(self):
        self._first.startReifier()
        self._second.startReifier()

    def endReifier(self):
        self._first.endReifier()
        self._second.endReifier()

    def startIsa(self):
        self._first.startIsa()
        self._second.startIsa()

    def endIsa(self):
        self._first.endIsa()
        self._second.endIsa()

    def value(self, val, datatype=None):
        self._first.value(val, datatype)
        self._second.value(val, datatype)


#pylint: disable-msg=W0622,W0221
class SimpleMapHandler(DelegatingMapHandler):
    """\
    A ``MapHandler`` implementation that adds some methods which cover common
    use cases.
    
    This class may be used to wrap an ordinary ``MapHandler`` implementation.
    """
    __slots__ = []
    _SUPERTYPE_SUBTYPE = mio.SUBJECT_IDENTIFIER, TMDM.supertype_subtype
    _SUPERTYPE = mio.SUBJECT_IDENTIFIER, TMDM.supertype
    _SUBTYPE = mio.SUBJECT_IDENTIFIER, TMDM.subtype
    
    def __init__(self, handler):
        super(SimpleMapHandler, self).__init__(handler)

    def topic(self, identity):
        """\
        Generates a `startTopic` and a `endTopic` event.
        """
        self.startTopic(identity)
        self.endTopic()

    def isa(self, identity):
        """\
        Generates a `startIsa`, `topicRef` and a `endIsa` event.
        """
        self.startIsa()
        self.topicRef(identity)
        self.endIsa()

    def ako(self, subtype, supertype):
        """\
        Generates a supertype-subtype association.
        """
        self.startAssociation(SimpleMapHandler._SUPERTYPE_SUBTYPE)
        self.startRole(SimpleMapHandler._SUBTYPE)
        self.player(subtype)
        self.endRole()
        self.startRole(SimpleMapHandler._SUPERTYPE)
        self.player(supertype)
        self.endRole()
        self.endAssociation()

    def type(self, identity):
        """\
        Generates a `startType`, `topicRef` and `endType` event.
        """
        self.startType()
        self.topicRef(identity)
        self.endType()

    def theme(self, identity):
        """\
        Generates a `startTheme`, `topicRef` and `endTheme` event.
        """
        self.startTheme()
        self.topicRef(identity)
        self.endTheme()

    def player(self, identity):
        """\
        Generates a `startPlayer`, `topicRef` and `endPlayer` event.
        """
        self.startPlayer()
        self.topicRef(identity)
        self.endPlayer()

    def role(self, type, player):
        """\
        Generates a `startRole`, `player` and `endRole` event.
        """
        self.startRole(type)
        self.player(player)
        self.endRole()

    def reifier(self, identity):
        """\
        Generates a `startReifier`, `topicRef` and `endReifier` event 
        iff `identity` is provided.
        """
        if identity:
            self.startReifier()
            self.topicRef(identity)
            self.endReifier()

    def startAssociation(self, type=None):
        """\
        Generates a `startAssociation` and iff the `type` is specified, a `startType`,
        `topicRef`, and `endType` event.
        """
        super(SimpleMapHandler, self).startAssociation()
        if type is not None:
            self.type(type)

    def startRole(self, type=None):
        """\
        Generates a `startRole` and iff the `type` is specified, a `startType`,
        `topicRef`, and `endType` event.
        """
        super(SimpleMapHandler, self).startRole()
        if type is not None:
            self.type(type)

    def startOccurrence(self, type=None):
        """\
        Generates a `startOccurrence` and iff the `type` is specified, a `startType`,
        `topicRef`, and `endType` event.
        """
        super(SimpleMapHandler, self).startOccurrence()
        if type is not None:
            self.type(type)

    def occurrence(self, type, value, datatype=None):
        """\
        Issues a `startOccurrence`, `type` and `value` event.
        """
        self.startOccurrence(type)
        self.value(value, datatype or XSD.string)
        self.endOccurrence()

    def startName(self, type=None):
        """\
        Generates a `startName` and iff the `type` is specified, a `startType`,
        `topicRef`, and `endType` event.
        """
        super(SimpleMapHandler, self).startName()
        if type is not None:
            self.type(type)

    def name(self, value, type=None):
        """\
        Generates a `startName`, a `type`, `value`, and `endName` event.
        """
        self.startName(type if type else _DEFAULT_NAME_TYPE)
        self.value(value)
        self.endName()


# Hamster handler states
_STATE_INITIAL = 1
_STATE_TOPIC = 2
_STATE_ASSOCIATION = 3
_STATE_ROLE = 4
_STATE_OCCURRENCE = 5
_STATE_NAME = 6
_STATE_VARIANT = 7
_STATE_TYPE = 8
_STATE_SCOPE = 9
_STATE_THEME = 10
_STATE_PLAYER = 11
_STATE_REIFIER = 12
_STATE_ISA = 13


class _Association(object):
    __slots__ = ['reifier', 'type', 'scope', 'iids', 'roles']
    def __init__(self):
        self.reifier = None
        self.type = None
        self.scope = []
        self.iids = []
        self.roles = []
    def add_iid(self, iri):
        self.iids.append(iri)
    def add_role(self, role):
        self.roles.append(role)
    def add_theme(self, theme):
        self.scope.append(theme)


class _Role(object):
    __slots__ = ['reifier', 'type', 'player', 'iids']
    def __init__(self):
        self.reifier = None
        self.type = None
        self.player = None
        self.iids = []
    def add_iid(self, iri):
        self.iids.append(iri)


class _Occurrence(object):
    __slots__ = ['reifier', 'type', 'scope', 'iids', 'value', 'datatype']
    def __init__(self):
        self.reifier = None
        self.type = None
        self.scope = []
        self.iids = []
        self.value = None
        self.datatype = None
    def add_iid(self, iri):
        self.iids.append(iri)
    def add_theme(self, theme):
        self.scope.append(theme)


class _Name(object):
    __slots__ = ['reifier', 'value', 'type', 'scope', 'iids', 'variants']
    def __init__(self):
        self.reifier = None
        self.value = None
        self.type = None
        self.scope = []
        self.iids = []
        self.variants = []
    def add_iid(self, iri):
        self.iids.append(iri)
    def add_variant(self, variant):
        self.variants.append(variant)
    def add_theme(self, theme):
        self.scope.append(theme)


class _Variant(object):
    __slots__ = ['reifier', 'scope', 'iids', 'value', 'datatype']
    def __init__(self):
        self.reifier = None
        self.scope = []
        self.iids = []
        self.value = None
        self.datatype = None
    def add_iid(self, iri):
        self.iids.append(iri)
    def add_theme(self, theme):
        self.scope.append(theme)


def _create_association():
    return _Association()


def _create_role():
    return _Role()


def _create_occurrence():
    return _Occurrence()


def _create_name():
    return _Name()


def _create_variant():
    return _Variant()


class HamsterMapHandler(MapHandler):
    """\
    Simplification of the ``MapHandler``.
    
    This (abstract) class collects information about Topic Maps constructs
    and reports them once an ``endX`` occurs.

    Additionally, this class checks for errors, so classes derived from this
    class are very simple to implement since all error checking / state keeping
    is done by this class.
    """
    __slots__ = ['_states', '_constructs']

    def __init__(self):
        super(HamsterMapHandler, self).__init__()
        self._states = None
        self._constructs = None

    ## Methods which must be implemented by classes derived from the HamsterHandler
    def _create_topic_by_iid(self, iri):
        """\
        Returns either an existing topic with the specified item identifier
        or creates a topic with the specified item identifier.
        """
        raise NotImplementedError()

    def _create_topic_by_sid(self, iri):
        """\
        Returns either an existing topic with the specified subject identifier
        or creates a topic with the specified subject identifier.
        """
        raise NotImplementedError()

    def _create_topic_by_slo(self, iri):
        """\
        Returns either an existing topic with the specified subject locator
        or creates a topic with the specified subject locator.
        """
        raise NotImplementedError()

    def _handle_type_instance(self, instance, type):
        """\
        Creates a tmdm:type-instance relationship between `instance` and
        `type`.
        """
        raise NotImplementedError()

    def _handle_item_identifier(self, topic, iri):
        """\
        Adds the item identifier `iri` to the topic.
        
        Adding the item identifier to the topic may cause a merge operation 
        that must be handled transparently.
        """
        raise NotImplementedError()

    def _handle_subject_identifier(self, topic, iri):
        """\
        Adds the subject identifier `iri` to the topic.
        
        Adding the subject identifier to the topic may cause a merge operation 
        that must be handled transparently.
        """
        raise NotImplementedError()

    def _handle_subject_locator(self, topic, iri):
        """\
        Adds the subject locator `iri` to the topic.
        
        Adding the subject locator to the topic may cause a merge operation 
        that must be handled transparently.
        """
        raise NotImplementedError()

    def _handle_topicmap_item_identifier(self, iri):
        """\
        Adds the item identifier ``iid`` to the topic map.
        """
        raise NotImplementedError()

    def _handle_topicmap_reifier(self, reifier):
        """\
        Sets the [reifier] property of the topic map.
        """
        raise NotImplementedError()

    def _create_association(self, type, scope, reifier, iids, roles):
        """\
        Creates an association with the provided properties.
        
        `type`
            The type of the association.
        `scope`
            The scope of the association or ``None`` to indicate the 
            unconstrained scope.
        `reifier`
            The reifier of the association or ``None``
        `iids`
            The item identifiers of the association. 
            This collection is never ``None`` but may be empty.
        `roles`
            The roles of the association (never empty)
            The collection contains objects like this::

                class Role:
                    type = A topic
                    player = A topic
                    reifier = A topic
                    iids = An iterable of strings which are the
                           item identifiers of the role
        """
        raise NotImplementedError()

    def _create_occurrence(self, parent, type, value, datatype, scope, reifier, iids):
        """\
        Creates an occurrence with the provided properties.
        
        `parent`
            The parent topic.
        `type`
            The occurrence type.
        `value`
            The value of the occurrence.
        `datatype`
            The datatype IRI.
        `scope`
            The scope of the occurrence or ``None`` to indicate the 
            unconstrained scope.
        `reifier`
            The reifier of the occurrence or ``None``.
        `iids`
            The item identifiers of the occurrence. 
            This collection is never ``None`` but may be empty.
        """
        raise NotImplementedError()

    def _create_name(self, parent, type, value, scope, reifier, iids, variants):
        """\
        Creates a topic name with the provided properties.
        
        `parent`
            The parent topic.
        `type`
            The name type or ``None`` to indicate the default name type.
        `value`
            The value of the name.
        `scope`
            The scope of the name  or ``None`` to indicate the 
            unconstrained scope.
        `reifier`
            The reifier of the name or ``None``.
        `iids`
            The item identifiers of the name. 
            This collection is never ``None`` but may be empty.
        `variants`
            The variants of the name. 
            This collection is never ``None`` but may be emtpy.
            The collection contains objects like this::

                class Variant:
                    reifier = A topic
                    value = A string
                    datatype = A string
                    scope = An iterable of topics (never empty)
                    iids = An iterable of strings which are the
                           item identifiers of the variant
        """
        raise NotImplementedError()
    ## End of methods which must be implemented by derived classes
    
    def notify_merge(self, source, target):
        """\
        This method MUST be invoked by a derived class if the `source` topic
        is merged into the `target` topic.
        """
        for i, c in enumerate(self._constructs):
            if c == source:
                self._constructs[i] = target

    ## Internal methods
    def __create_topic(self, identity):
        kind, iri = identity
        if kind is mio.ITEM_IDENTIFIER:
            return self._create_topic_by_iid(iri)
        elif kind is mio.SUBJECT_IDENTIFIER:
            return self._create_topic_by_sid(iri)
        elif kind is mio.SUBJECT_LOCATOR:
            return self._create_topic_by_slo(iri)
        else:
            raise mio.MIOException('Unknown reference type: "%s"' % kind)

    def __handle_topic(self, topic):
        # The topic may be used within a context
        state = self._states[-1]
        if _STATE_TYPE is state:
            self._constructs[-1].type = topic
        elif _STATE_PLAYER is state:
            self._constructs[-1].player = topic
        elif _STATE_ISA is state:
            self._handle_type_instance(self._constructs[-1], topic)
        elif _STATE_THEME is state:
            self._constructs[-1].add_theme(topic)
        elif _STATE_REIFIER is state:
            if _STATE_INITIAL is self._states[-2]:
                self._handle_topicmap_reifier(topic)
            else:
                self._constructs[-1].reifier = topic
 
    ## MapHandler methods.
    def startTopicMap(self):
        self._states = [_STATE_INITIAL]
        self._constructs = []

    def endTopicMap(self):
        self._states = None
        self._constructs = None

    def itemIdentifier(self, iri):
        state = self._states[-1]
        if _STATE_TOPIC is state:
            self._handle_item_identifier(self._constructs[-1], iri)
        elif _STATE_INITIAL is state:
            self._handle_topicmap_item_identifier(iri)
        else:
            self._constructs[-1].add_iid(iri)

    def subjectIdentifier(self, iri):
        if not _STATE_TOPIC is self._states[-1]:
            raise mio.MIOException('Unexpected "subjectIdentifier" event')
        self._handle_subject_identifier(self._constructs[-1], iri)

    def subjectLocator(self, iri):
        if not _STATE_TOPIC is self._states[-1]:
            raise mio.MIOException('Unexpected "subjectLocator" event')
        self._handle_subject_locator(self._constructs[-1], iri)

    def topicRef(self, identity):
        self.__handle_topic(self.__create_topic(identity))

    def startTopic(self, identity):
        self._constructs.append(self.__create_topic(identity))
        self._states.append(_STATE_TOPIC)

    def endTopic(self):
        if _STATE_TOPIC is not self._states.pop():
            raise mio.MIOException('Unexpected "endTopic" event')
        self.__handle_topic(self._constructs.pop())

    def startAssociation(self):
        self._states.append(_STATE_ASSOCIATION)
        self._constructs.append(_create_association())

    def endAssociation(self):
        if _STATE_ASSOCIATION is not self._states.pop():
            raise mio.MIOException('Unexpected "endAssociation" event')
        assoc = self._constructs.pop()
        if not assoc.type:
            raise mio.MIOException('The association has no type')
        if not assoc.roles:
            raise mio.MIOException('The association has no roles')
        self._create_association(assoc.type, assoc.scope,
                                 assoc.reifier, assoc.iids, assoc.roles)

    def startRole(self):
        if _STATE_ASSOCIATION is not self._states[-1]:
            raise mio.MIOException('Unexpected "startRole" event, not in an association')
        self._states.append(_STATE_ROLE)
        self._constructs.append(_create_role())

    def endRole(self):
        if _STATE_ROLE is not self._states.pop():
            raise mio.MIOException('Unexpected "endRole" event')
        role = self._constructs.pop()
        if not role.type:
            raise mio.MIOException('The role has no type')
        if not role.player:
            raise mio.MIOException('The role has no player')
        self._constructs[-1].add_role(role)

    def startOccurrence(self):
        if _STATE_TOPIC is not self._states[-1]:
            raise mio.MIOException('Unexpected "startOccurrence" event, not in a topic')
        self._states.append(_STATE_OCCURRENCE)
        self._constructs.append(_create_occurrence())

    def endOccurrence(self):
        if _STATE_OCCURRENCE is not self._states.pop():
            raise mio.MIOException('Unexpected "endOccurrence" event')
        occ = self._constructs.pop()
        if not occ.type:
            raise mio.MIOException('The occurrence has no type')
        if occ.value is None: # Important: Check for None, not 'not value' since an empty string is allowed
            raise mio.MIOException('The occurrence has no value')
        self._create_occurrence(self._constructs[-1],
                                occ.type, occ.value, occ.datatype,
                                occ.scope, occ.reifier, occ.iids)

    def startName(self):
        if _STATE_TOPIC is not self._states[-1]:
            raise mio.MIOException('Unexpected "startName" event, not in a topic')
        self._states.append(_STATE_NAME)
        self._constructs.append(_create_name())

    def endName(self):
        if _STATE_NAME is not self._states.pop():
            raise mio.MIOException('Unexpected "endName" event')
        name = self._constructs.pop()
        if name.value is None: # Important: Check for None, not 'not value' since an empty string is allowed
            raise mio.MIOException('The name has no value')
        self._create_name(self._constructs[-1],
                          name.type, name.value, name.scope,
                          name.reifier, name.iids, name.variants)

    def startVariant(self):
        if _STATE_NAME is not self._states[-1]:
            raise mio.MIOException('Unexpected "startVariant" event, not in a name')
        self._states.append(_STATE_VARIANT)
        self._constructs.append(_create_variant())

    def endVariant(self):
        if _STATE_VARIANT is not self._states.pop():
            raise mio.MIOException('Unexpected "endVariant" event')
        var = self._constructs.pop()
        if not var.scope:
            raise mio.MIOException('The variant has no scope')
        if var.value is None:  # Important: Check for None, not 'not value' since an empty string is allowed
            raise mio.MIOException('The variant has no value')
        name = self._constructs[-1]
        name.add_variant(var)

    def startIsa(self):
        if _STATE_TOPIC is not self._states[-1]:
            raise mio.MIOException('Unexpected "startIsa" event, not in a topic')
        self._states.append(_STATE_ISA)

    def endIsa(self):
        if _STATE_ISA is not self._states.pop():
            raise mio.MIOException('Unexpected "endIsa" event')

    def startType(self):
        if self._states[-1] not in (_STATE_ASSOCIATION, _STATE_ROLE, _STATE_OCCURRENCE, _STATE_NAME):
            raise mio.MIOException('Unexpected "startType" event; not in an association, role, occurrence, or name')
        self._states.append(_STATE_TYPE)

    def endType(self):
        if _STATE_TYPE is not self._states.pop():
            raise mio.MIOException('Unexpected "endType" event')

    def startPlayer(self):
        if _STATE_ROLE is not self._states[-1]:
            raise mio.MIOException('Unexpected "startPlayer" event, not in a role')
        self._states.append(_STATE_PLAYER)

    def endPlayer(self):
        if _STATE_PLAYER is not self._states.pop():
            raise mio.MIOException('Unexpected "endPlayer" event')

    def startScope(self):
        if self._states[-1] not in (_STATE_ASSOCIATION, _STATE_OCCURRENCE, _STATE_NAME, _STATE_VARIANT):
            raise mio.MIOException('Unexpected "startScope" event; not in an association, occurrence, name, or variant')
        self._states.append(_STATE_SCOPE)

    def endScope(self):
        if _STATE_SCOPE is not self._states.pop():
            raise mio.MIOException('Unexpected "endScope" event')

    def startTheme(self):
        if _STATE_SCOPE is not self._states[-1]:
            raise mio.MIOException('Unexpected "startTheme" event, not in scope')
        self._states.append(_STATE_THEME)

    def endTheme(self):
        if _STATE_THEME is not self._states.pop():
            raise mio.MIOException('Unexpected "endTheme" event')

    def startReifier(self):
        if _STATE_TOPIC is self._states[-1]:
            raise mio.MIOException('Unexpected "startReifier" event within a topic')
        self._states.append(_STATE_REIFIER)

    def endReifier(self):
        if _STATE_REIFIER is not self._states.pop():
            raise mio.MIOException('Unexpected "endReifier" event')

    def value(self, value, datatype=None):
        if value is None:
            raise mio.MIOException('The value must not be None')
        state, tmc = self._states[-1], self._constructs[-1]
        if _STATE_NAME is state:
            if datatype:
                raise mio.MIOException('The datatype must be None for names')
            tmc.value = value            
        elif state in (_STATE_OCCURRENCE, _STATE_VARIANT):
            if not datatype:
                raise mio.MIOException('The datatype must be provided')
            tmc.value, tmc.datatype = value, datatype
        else:
            raise mio.MIOException('Unexpected value event in state "%s"' % state)

del TMDM

def simplify(handler):
    """\
    Returns a `SimpleMapHandler` which wraps the specified `handler` iff
    it is not already a `SimpleMapHandler`
    """
    if isinstance(handler, SimpleMapHandler):
        return handler
    return SimpleMapHandler(handler)

_java_compatible = False

import sys
if sys.platform[:4] == 'java':
    _java_compatible = True
    try:
        from com.semagia.mio import IRef, MIOException as JavaMIOException, IMapHandler as JavaIMapHandler
        from com.semagia.mio.helpers import Ref
    except ImportError:
        _java_compatible = False
del sys

if _java_compatible:
    class MIOHandlerToJava(SimpleMapHandler):
        """\
        A ``MapHandler`` implementation that delegates all Python MIO events to
        a Java implementation of ``com.semagia.mio.IMapHandler``.
        
        All ``SimpleMapHandler`` methods are available as well.
        """
        __slots__ = []
        def __init__(self, handler):
            super(MIOHandlerToJava, self).__init__(handler)

        def startTopic(self, identity):
            super(MIOHandlerToJava, self).startTopic(_create_ref(identity))

        def topicRef(self, identity):
            super(MIOHandlerToJava, self).topicRef(_create_ref(identity))

        def value(self, value, datatype=None):
            # Necessary to let Jython decide which method should be called.
            if datatype is None:
                self._handler.value(value)
            else:
                self._handler.value(value, datatype)

    def _create_ref((kind, iri)):
        """\
        Returns a IRef implementation from the specified ``(kind, iri)`` tuple.
        """
        if mio.ITEM_IDENTIFIER is kind:
            return Ref.createItemIdentifier(iri)
        elif mio.SUBJECT_IDENTIFIER is kind:
            return Ref.createSubjectIdentifier(iri)
        elif mio.SUBJECT_LOCATOR is kind:
            return Ref.createSubjectLocator(iri)
        raise JavaMIOException('Unknown identity kind "%s"' % kind)


    class MIOHandlerFromJava(JavaIMapHandler, DelegatingMapHandler):
        """\
        Implements the ``com.semagia.mio.IMapHandler`` interface and 
        translates the events to the Python equivalent. 
        """
        def startTopic(self, ref):
            self._handler.startTopic(_create_identity(ref))

        def topicRef(self, ref):
            self._handler.topicRef(_create_identity(ref))

    def _create_identity(ref):
        """\
        Returns a identity tuple ``(kind, iri)`` from the specified Java mio.IRef.
        """
        kind, iri = ref.getType(), ref.getIRI()
        if IRef.ITEM_IDENTIFIER == kind:
            return mio.ITEM_IDENTIFIER, iri
        elif IRef.SUBJECT_IDENTIFIER == kind:
            return mio.SUBJECT_IDENTIFIER, iri
        elif IRef.SUBJECT_LOCATOR == kind:
            return mio.SUBJECT_LOCATOR, iri
        raise JavaMIOException('Unknown reference type "%s"' % kind)
