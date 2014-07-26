# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
Provides deserialization of TM/XML topic maps.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
from xml.sax import handler as sax_handler
from tm import TMDM, XSD
from tm import mio
from tm.irilib import resolve_iri

__all__ = ['TMXMLContentHandler']

_NS_TMXML = u'http://psi.ontopia.net/xml/tm-xml/'
_NS_TMDM = u'http://psi.topicmaps.org/iso13250/model/'
_TOPIC_NAME = mio.SUBJECT_IDENTIFIER, TMDM.topic_name   # Default name type

# States
_INITIAL = 0
_TOPICMAP = 1
_TOPIC = 2
_IDENTITY = 3
_ASSOCIATION = 4
_AFTER_ROLE = 5
_BASENAME = 6
_NAME = 7
_VARIANT = 8
_PROPERTY = 9

_ATTR_ID = None, u'id'
_ATTR_ROLE = None, u'role'
_ATTR_SCOPE = None, u'scope'
_ATTR_REIFIER = None, u'reifier'
_ATTR_DATATYPE = None, u'datatype'
_ATTR_TOPIC_REF = None, u'topicref'
_ATTR_OTHER_ROLE = None, u'otherrole'


class TMXMLContentHandler(sax_handler.ContentHandler):
    """\
    Content handler for TM/XML topic maps.
    """
    def __init__(self):
        sax_handler.ContentHandler.__init__(self)
        self.map_handler = None
        self._prefixes = {}
        self._content = []
        self._state = _INITIAL
        self.doc_iri = None
        self._current_topic = None
        self._type = None
        self._scope = None
        self._reifier = None
        self._datatype = None
        self._seen_identity = False

    def startDocument(self):
        self._prefixes = {}
        self._content = []
        self._state = _INITIAL
        self._current_topic = None
        self._type = None
        self._scope = None
        self._reifier = None
        self._datatype = None

    def startPrefixMapping(self, prefix, uri):
        self._prefixes[prefix] = uri

    def endPrefixMapping(self, prefix):
        del self._prefixes[prefix]

    def startElementNS(self, (uri, name), qname, attrs):
        state = self._state
        handler = self.map_handler
        topic_ref = self._topic_by_reference
        if _INITIAL is state:
            self._handle_reifier(attrs)
            state = _TOPICMAP
        elif _TOPICMAP is state:
            tid = attrs.get(_ATTR_ID, None)
            # The topic id is optional iff the topic has at least one sid / slo
            if tid:
                self._current_topic = self._resolve_iid(tid)
                handler.startTopic(self._current_topic)
                self._seen_identity = True
            else:
                self._seen_identity = False
            type_ = self._resolve_type(uri, name)
            if type_:
                if self._seen_identity:
                    handler.isa(type_)
                else:
                    # No startTopic event, delay the type-instance assoc.
                    self._type = type_
            state = _TOPIC
        elif _TOPIC is state:
            if uri == _NS_TMXML and name in (u'identifier', u'locator'):
                state = _IDENTITY
            elif attrs.get(_ATTR_ROLE, None):
                handler.startAssociation(self._resolve_type(uri, name))
                self._handle_scope(attrs)
                self._handle_reifier(attrs)
                # 1 .. n-ary
                handler.startRole(topic_ref(attrs.getValue(_ATTR_ROLE)))
                handler.player(self._current_topic)
                handler.endRole()
                if attrs.get(_ATTR_TOPIC_REF, None):
                    # 2-ary
                    handler.startRole(topic_ref(attrs.getValue(_ATTR_OTHER_ROLE)))
                    handler.player(topic_ref(attrs.getValue(_ATTR_TOPIC_REF)))
                    handler.endRole()
                state = _ASSOCIATION
            else:
                self._scope = self._collect_scope(attrs)
                self._type = self._resolve_type(uri, name)
                self._reifier = attrs.get(_ATTR_REIFIER, None)
                self._datatype = attrs.get(_ATTR_DATATYPE, XSD.string)
                state = _PROPERTY
        elif _ASSOCIATION is state:
            handler.startRole(self._resolve_type(uri, name))
            handler.player(topic_ref(attrs.getValue(_ATTR_TOPIC_REF)))
            self._handle_reifier(attrs)
            handler.endRole()
            state = _AFTER_ROLE
        elif _PROPERTY is state and uri == _NS_TMXML and name == u'value':
            self._content = []
            state = _BASENAME
        elif _NAME is state and uri == _NS_TMXML and name == u'variant':
            self._scope = self._collect_scope(attrs)
            self._reifier = attrs.get(_ATTR_REIFIER, None)
            self._datatype = attrs.get(_ATTR_DATATYPE, XSD.string)
            state = _VARIANT
        self._state = state

    def endElementNS(self, name, qname):
        state = self._state
        handler = self.map_handler
        uri, name = name
        if _TOPICMAP is state:
            state = _INITIAL
        elif _TOPIC is state:
            handler.endTopic()
            state = _TOPICMAP
        elif _IDENTITY is state:
            iri = self._resolve_iri(''.join(self._content))
            if not self._seen_identity:
                self._handle_delayed_topic(name, iri)
            elif name == u'identifier':
                handler.subjectIdentifier(iri)
            else:
                assert name == u'locator'
                handler.subjectLocator(iri)
            self._content = []
            state = _TOPIC
        elif _PROPERTY is state:
            handler.startOccurrence(self._resolve_type(uri, name))
            handler.value(u''.join(self._content), self._datatype)
            self._process_scope(self._scope)
            self._process_reifier(self._reifier)
            handler.endOccurrence()
            self._content = []
            state = _TOPIC
        elif _BASENAME is state:
            handler.startName(self._type)
            self._process_scope(self._scope)
            self._process_reifier(self._reifier)
            handler.value(''.join(self._content))
            self._content = []
            state = _NAME
        elif _NAME is state:
            handler.endName()
            state = _TOPIC
        elif _VARIANT is state:
            handler.startVariant()
            self._process_scope(self._scope)
            self._process_reifier(self._reifier)
            handler.value(''.join(self._content), self._datatype)
            handler.endVariant()
            self._content = []
            state = _NAME
        elif _ASSOCIATION is state:
            handler.endAssociation()
            state = _TOPIC
        elif _AFTER_ROLE is state:
            state = _ASSOCIATION
        self._state = state

    def characters(self, content):
        if self._state in (_IDENTITY, _PROPERTY, _BASENAME, _VARIANT):
            self._content.append(content)

    def _handle_delayed_topic(self, name, iri):
        """\
        Sends a startTopic event with a subject identifier or subject locator.
        """
        if name == u'identifier':
            self._current_topic = mio.SUBJECT_IDENTIFIER, iri
        elif name == u'locator':
            self._current_topic = mio.SUBJECT_LOCATOR, iri
        self.map_handler.startTopic(self._current_topic)
        if self._type:
            self.map_handler.isa(self._type)
            self._type = None

    def _topic_by_reference(self, ref):
        """\
        Resolves a topic either by its subject identifier or item identifier.
        If `ref` is a QName (prefix:local), a subject identifier is returned, 
        otherwise an item identifier.
        """
        if u':' in ref:
            return self._resolve_sid(ref)
        return self._resolve_iid(ref)

    def _resolve_iid(self, ref):
        """\
        Resolves the specified `ref` against the base IRI and returns an 
        item identifier reference.
        """
        return mio.ITEM_IDENTIFIER, self._resolve_iri(u'#%s' % ref)

    def _resolve_sid(self, qname):
        """\
        Resolves the specified `qname` against the base IRI and returns a
        subject identifier reference.
        """
        prefix, local = qname.split(u':')
        try:
            return mio.SUBJECT_IDENTIFIER, self._resolve_iri(self._prefixes[prefix] + local)
        except KeyError:
            raise mio.MIOException('Undefined prefix "%s"' % prefix)

    def _resolve_iri(self, iri):
        """\
        Resolves the specified IRI against the base IRI.
        """
        return resolve_iri(self.doc_iri, iri)

    def _resolve_type(self, uri, name):
        """\
        Returns a topic reference (subject identifier / item identifier) from 
        the specified (uri, name) tuple. Returns ``None`` iff the tuple
        is ('http://psi.ontopia.net/xml/tm-xml/', 'topic') 
        """
        if not uri:
            return self._resolve_iid(name)
        if uri == _NS_TMDM and name == u'topic-name':
            return _TOPIC_NAME
        if uri == _NS_TMXML and name == u'topic':
            return None
        return mio.SUBJECT_IDENTIFIER, self._resolve_iri(uri + name)

    def _collect_scope(self, attrs):
        """\
        Returns topic references from the specified attributes.
        
        If the attributes provide no 'scope' key an empty collection is returned.
        """
        scope = attrs.get(_ATTR_SCOPE, None)
        if not scope:
            return ()
        topic_ref = self._topic_by_reference
        return [topic_ref(theme) for theme in scope.split()]

    def _handle_scope(self, attrs):
        """\
        Retrieves the ``scope`` attribute from the attributes and sends 
        ``startScope`` .. ``endScope`` notifications if the ``scope`` attribute
        is given.
        """
        self._process_scope(self._collect_scope(attrs))

    def _process_scope(self, themes):
        """\
        Sends ``startScope`` .. ``endScope`` notifications iff `themes` is not
        empty.
        """
        if themes:
            handler = self.map_handler
            handler.startScope()
            for theme in themes:
                handler.theme(theme)
            handler.endScope()

    def _handle_reifier(self, attrs):
        """\
        Retrieves the ``reifier`` attribute from the attributes and sends
        ``startReifier`` .. ``endReifier`` notifications iff the attribute is
        given.
        """
        self._process_reifier(attrs.get(_ATTR_REIFIER, None))

    def _process_reifier(self, reifier):
        """\
        Resolves the ``reifier`` reference into an absolute IRI (either
        subject identifier or item identifier) iff ``reifier`` is not ``None``
        and notifies the handler about the reifier.
        """
        if reifier:
            self.map_handler.reifier(self._topic_by_reference(reifier))

