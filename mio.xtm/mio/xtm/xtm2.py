# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
This module provides classes to read 
`XML Topic Maps (XTM) 2.0 <http://www.isotopicmaps.org/sam/sam-xtm/2006-06-19/>`_
and `XML Topic Maps (XTM) 2.1 <http://www.isotopicmaps.org/sam/sam-xtm/2009-11-19/>`_

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
from StringIO import StringIO
import xml.sax.handler as sax_handler
from xml.sax.saxutils import XMLGenerator
from tm import TMDM, XSD, voc, mio, Source
from tm.mio.deserializer import Context
from tm.irilib import resolve_iri

__all__ = ['XTM2ContentHandler']

# XTM 2.0 namespace
NS_XTM = voc.XTM

# Constants for XTM elements.
MERGE_MAP = u'mergeMap'
TOPIC_MAP = u'topicMap'
TOPIC = u'topic'
ASSOCIATION = u'association'
ROLE = u'role'
OCCURRENCE = u'occurrence'
NAME = u'name'
VARIANT = u'variant'
INSTANCE_OF = u'instanceOf'
TYPE = u'type'
VALUE = u'value'
RESOURCE_REF = u'resourceRef'
RESOURCE_DATA = u'resourceData'
SCOPE = u'scope'
TOPIC_REF = u'topicRef'
SUBJECT_IDENTIFIER = u'subjectIdentifier'
SUBJECT_LOCATOR = u'subjectLocator'
ITEM_IDENTITY = u'itemIdentity'
# XTM 2.1 specific elements
REIFIER = u'reifier'
SUBJECT_IDENTIFIER_REF = u'subjectIdentifierRef'
SUBJECT_LOCATOR_REF = u'subjectLocatorRef'

# Constants for XTM attributes.
_VERSION = (None, u'version')
_REIFIER = (None, u'reifier')
_HREF = (None, u'href')
_ID = (None, u'id')
_DATATYPE = (None, u'datatype')

# States
_STATE_INITIAL = 1
_STATE_TOPIC = 2
_STATE_ASSOCIATION = 3
_STATE_ROLE = 4
_STATE_TYPE = 5
_STATE_INSTANCE_OF = 6
_STATE_SCOPE = 7
_STATE_OCCURRENCE = 8
_STATE_NAME = 9
_STATE_VARIANT = 10
_STATE_REIFIER = 11 # 2.1

#pylint: disable-msg=E1103
class XTM2ContentHandler(sax_handler.ContentHandler):
    """\
    Content handler for `XTM 2.0 <http://www.isotopicmaps.org/sam/sam-xtm/2006-06-19/>`_
    and `XTM 2.1 <http://www.isotopicmaps.org/sam/sam-xtm/2009-11-19/>`_ topic maps.
    """

    # Default topic name type
    _TOPIC_NAME = mio.SUBJECT_IDENTIFIER, TMDM.topic_name

    def __init__(self, map_handler=None, locator=None):
        """\
        Initializes this handler with the specified input adapter `adapter`
        """
        self.map_handler = map_handler
        self.subordinate = False
        self.context = Context()
        self.reset(locator)
        self.version = u'2.0'
        self._seen_identity = False
        self.strict = True

    def reset(self, locator=None):
        self._state = _STATE_INITIAL
        self._next_state = None
        self._seen_type = False
        self._seen_reifier = False
        self._datatype = None
        self.doc_iri = locator
        self._accept_xml = False
        self._accept_content = False
        # The ``_content`` used to keep "ordinary" string content and it is
        # used by the XMLGenerator, so ``_content.truncate(0)`` effects also
        # the output of the XMLGenerator
        self._content = StringIO()
        self._xml_handler = XMLGenerator(self._content)

    def startDocument(self):
        pass

    def startPrefixMapping(self, prefix, uri):
        if self._accept_xml:
            self._xml_handler.startPrefixMapping(prefix, uri)

    def endPrefixMapping(self, prefix):
        if self._accept_xml:
            self._xml_handler.endPrefixMapping(prefix)

    def processingInstruction(self, target, data):
        if self._accept_xml:
            self._xml_handler.processingInstruction(target, data)

    def setDocumentLocator(self, locator):
        if not self._locator:
            self._locator = locator.getSystemId()

    def startElementNS(self, (uri, name), qname, attrs):
        if self._accept_xml:
            self._xml_handler.startElementNS((uri, name), qname, attrs)
            return
        handler = self.map_handler
        state = self._state
        href = self._href
        process_reifier = self._process_reifier_attr
        create_locator = self._create_locator
        if TOPIC_REF == name:
            iid = href(attrs)
            if self.version == u'2.0' and u'#' not in iid:
                raise mio.MIOException('Invalid topic reference "%s". Does not contain a fragment identifier' % iid)
            ref = mio.ITEM_IDENTIFIER, iid
            self._handle_topic_reference(ref)
        elif SUBJECT_IDENTIFIER_REF == name:
            if self.version == u'2.0':
                raise mio.MIOException('The <subjectIdentifierRef/> element is disallowed in XTM 2.0')
            self._handle_topic_reference((mio.SUBJECT_IDENTIFIER, href(attrs)))
        elif SUBJECT_LOCATOR_REF == name:
            if self.version == u'2.0':
                raise mio.MIOException('The <subjectLocatorRef/> element is disallowed in XTM 2.0')
            self._handle_topic_reference((mio.SUBJECT_LOCATOR, href(attrs)))
        elif TOPIC == name:
            ident = attrs.get(_ID)
            if ident:
                handler.startTopic((mio.ITEM_IDENTIFIER, create_locator('#' + ident)))
            elif self.version == u'2.0':
                raise mio.MIOException('Illegal XTM 2.0 instance: The id attribute is missing from the <topic/> element')
            self._state = _STATE_TOPIC
            self._seen_identity = ident is not None
        elif INSTANCE_OF == name:
            if state != _STATE_TOPIC:
                raise mio.MIOException('Unexpected "instanceOf" element')
            self._state = _STATE_INSTANCE_OF
        elif TYPE == name:
            self._next_state, self._state = state, _STATE_TYPE 
        elif SUBJECT_IDENTIFIER == name:
            if not self._seen_identity:
                handler.startTopic((mio.SUBJECT_IDENTIFIER, href(attrs)))
                self._seen_identity = True
            else:
                handler.subjectIdentifier(href(attrs))
        elif SUBJECT_LOCATOR == name:
            if not self._seen_identity:
                handler.startTopic((mio.SUBJECT_LOCATOR, href(attrs)))
                self._seen_identity = True
            else:
                handler.subjectLocator(href(attrs))
        elif ITEM_IDENTITY == name:
            if state == _STATE_TOPIC and not self._seen_identity:
                handler.startTopic((mio.ITEM_IDENTIFIER, href(attrs)))
                self._seen_identity = True
            else:
                handler.itemIdentifier(href(attrs))
        elif ASSOCIATION == name:
            handler.startAssociation()
            process_reifier(attrs)
            self._state = _STATE_ASSOCIATION
        elif ROLE == name:
            handler.startRole()
            process_reifier(attrs)
            self._state = _STATE_ROLE
        elif VALUE == name:
            self._accept_content = True
            self._content.truncate(0)
        elif RESOURCE_DATA == name:
            self._datatype = attrs.get(_DATATYPE, XSD.string)
            self._accept_content = True
            self._content.truncate(0)
            self._accept_xml = self._datatype == XSD.anyType
        elif RESOURCE_REF == name:
            handler.value(href(attrs), XSD.anyURI)
        elif OCCURRENCE == name:
            handler.startOccurrence()
            process_reifier(attrs)
            self._state = _STATE_OCCURRENCE
        elif NAME == name:
            handler.startName()
            process_reifier(attrs)
            self._seen_type = False
            self._state = _STATE_NAME
        elif VARIANT == name:
            handler.startVariant()
            process_reifier(attrs)
            self._state = _STATE_VARIANT
        elif SCOPE == name:
            handler.startScope()
            self._next_state, self._state = state, _STATE_SCOPE
        elif TOPIC_MAP == name:
            version = attrs.get(_VERSION)
            if version not in (u'2.0', u'2.1'):
                raise mio.MIOException('Invalid XTM version. Expected "2.0" or "2.1", got: "%s"' % version)
            self.version = version
            reifier = attrs.get(_REIFIER)
            if reifier:
                self._process_topicmap_reifier((mio.ITEM_IDENTIFIER, self._create_locator(reifier)))
                self._seen_reifier = True
            else:
                self._seen_reifier = False
            self._state = _STATE_INITIAL
        elif MERGE_MAP == name:
            self._process_mergemap(href(attrs))
        elif REIFIER == name:
            if self.version == u'2.0':
                raise mio.MIOException('The <reifier/> element is disallowed in XTM 2.0')
            if self._seen_reifier:
                raise mio.MIOException('Found a reifier attribute and reifier element')
            self._next_state, self._state = state, _STATE_REIFIER
        else:
            raise mio.MIOException('Unknown start element %s' % name)

    def endElementNS(self, (uri, name), qname):
        if self._accept_xml:
            self._xml_handler.endElementNS((uri, name), qname)
            return
        handler = self.map_handler
        if TOPIC == name:
            if not self._seen_identity:
                raise mio.MIOException('Found a topic without an identity')
            self._state = _STATE_INITIAL
        elif name in (TOPIC_MAP, TOPIC_REF, RESOURCE_REF):
            return
        elif SCOPE == name:
            handler.endScope()
            self._state = self._next_state
        elif name in (TYPE, REIFIER):
            self._state = self._next_state
        elif INSTANCE_OF == name:
            self._state = _STATE_TOPIC
        elif ASSOCIATION == name:
            handler.endAssociation()
            self._state = _STATE_INITIAL
        elif ROLE == name:
            handler.endRole()
            self._state = _STATE_ASSOCIATION
        elif OCCURRENCE == name:
            handler.endOccurrence()
            self._state = _STATE_TOPIC
        elif NAME == name:
            if not self._seen_type:
                handler.type(XTM2ContentHandler._TOPIC_NAME)
            handler.endName()
            self._state = _STATE_TOPIC
        elif VARIANT == name:
            handler.endVariant()
            self._state = _STATE_NAME
        elif RESOURCE_DATA == name:
            if self._accept_xml:
                self._content.flush()
                handler.value(self._content.getvalue(), XSD.anyType)
            elif XSD.anyURI == self._datatype:
                handler.value(self._create_locator(self._content.getvalue()), XSD.anyURI)
            else:
                handler.value(self._content.getvalue(), self._datatype)
            self._accept_content = False
            self._accept_xml = False
        elif VALUE == name:
            handler.value(self._content.getvalue())
            self._accept_content = False

    def endDocument(self):
        self.reset()

    def characters(self, content):
        if self._accept_xml:
            self._xml_handler.characters(content)
        elif self._accept_content:
            self._content.write(content)

    def _handle_topic_reference(self, ref):
        """\
        Context-sensitive handling of references to topics (via item identifier,
        subject identifier or subject locator).
        
        `ref`
            A topic reference: (mio.ITEM_IDENTIFIER, iri) 
            or (mio.SUBJECT_IDENTIFIER, iri) or (mio.SUBJECT_LOCATOR, iri)
        """
        state, handler = self._state, self.map_handler
        if state is _STATE_INSTANCE_OF:
            handler.isa(ref)
        elif state is _STATE_ROLE:
            handler.player(ref)
        elif state is _STATE_SCOPE:
            handler.theme(ref)
        elif state is _STATE_TYPE:
            handler.type(ref)
            self._seen_type = True
        elif state is _STATE_REIFIER:
            if self._next_state is _STATE_INITIAL:
                self._process_topicmap_reifier(ref)
            else:
                handler.reifier(ref)
        else:
            raise mio.MIOException('Unexpected topic reference')

    def _process_mergemap(self, iri):
        if iri in self.context.loaded:
            return
        self.context.add_loaded(iri)
        from mio.xtm import create_deserializer
        deserializer = create_deserializer()
        deserializer.context = self.context
        deserializer.handler = self.map_handler
        deserializer.subordinate = True
        deserializer.parse(Source(iri))

    def _process_topicmap_reifier(self, ref):
        """\
        Adds the reifier to the topic map iff the content handler is not
        in ``subordinate`` mode.

        `ref`
            A topic reference: (mio.ITEM_IDENTIFIER, iri) 
            or (mio.SUBJECT_IDENTIFIER, iri) or (mio.SUBJECT_LOCATOR, iri)
        """
        if not self.subordinate:
            self.map_handler.reifier(ref)
        else:
            self.map_handler.topic(ref)

    def _process_reifier_attr(self, attrs):
        """\
        If the ``reifier`` attribute is not ``None``, this method generates
        a ``startReifier``, ``topicRef`` and ``endReifier`` event.
        """
        reifier = attrs.get(_REIFIER, None)
        if reifier:
            self.map_handler.reifier((mio.ITEM_IDENTIFIER, self._create_locator(reifier)))
        self._seen_reifier = reifier is not None

    def _href(self, attrs):
        """\
        Returns a locator from the attributes. Further, the locator is
        resolved against the base locator.
        """
        return self._create_locator(attrs.getValue(_HREF))

    def _create_locator(self, reference):
        """\
        Returns a locator where ``reference`` is resolved against the base
        locator.
        """
        return resolve_iri(self.doc_iri, reference)
