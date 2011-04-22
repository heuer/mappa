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
An (experimental) ``tm.mio.handler.MapHandler`` implementation that
translates events into XML Topic Maps (XTM) syntax.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
import logging
from tm import voc, XSD
from tm.mio import SUBJECT_IDENTIFIER, SUBJECT_LOCATOR, ITEM_IDENTIFIER
from tm.xmlutils import XMLWriter
import tm.mio.handler as mio_handler

__all__ = ['XTM21Handler']

_STATE_ILLEGAL = 0
_STATE_INITIAL = 1
_STATE_CHARACTERISTIC = 2
_STATE_INSTANCE_OF = 3
_STATE_TM_IID = 4
_STATE_TOPIC_MAP = 5
_STATE_IDENTITY = 6

from tm import TMDM
_DEFAULT_NAME_TYPE = SUBJECT_IDENTIFIER, TMDM.topic_name
del TMDM

class XTM21Handler(mio_handler.HamsterMapHandler):
    """\
    ``tm.mio.handler.MapHandler`` which writes XTM 2.1.
    """

    _TOPICREF2EL = {
        SUBJECT_IDENTIFIER: 'subjectIdentifierRef',
        SUBJECT_LOCATOR: 'subjectLocatorRef',
        ITEM_IDENTIFIER: 'topicRef'
    }

    _IDENTITY2EL = {
        SUBJECT_IDENTIFIER: 'subjectIdentifier',
        SUBJECT_LOCATOR: 'subjectLocator'
    }

    def __init__(self, fileobj, encoding='utf-8', prettify=False):
        """\

        `fileobj`
            File-like object which provides a ``write`` method.
        `encoding`
            The encoding of the stream (default: utf-8)
        `prettify`
            Indicates if the XML should be prettified or written in one line (default)

        >>> from StringIO import StringIO
        >>> out = StringIO()
        >>> handler = XTM21Handler(out)
        >>> handler.prettify
        False
        >>> handler.startTopicMap()
        >>> handler.startTopic((SUBJECT_IDENTIFIER, 'http://psi.example.org/something'))
        >>> handler.endTopic()
        >>> handler.endTopicMap()
        >>> out.getvalue()
        '<?xml version="1.0" encoding="utf-8" standalone="yes"?>\\n<topicMap xmlns="http://www.topicmaps.org/xtm/" version="2.1"><topic><subjectIdentifier href="http://psi.example.org/something"/></topic></topicMap>\\n'
        >>> out = StringIO()
        >>> handler = XTM21Handler(out, prettify=True)
        >>> handler.startTopicMap()
        >>> handler.startTopic((SUBJECT_IDENTIFIER, 'http://psi.example.org/something'))
        >>> handler.endTopic()
        >>> handler.endTopicMap()
        >>> out.getvalue()
        '<?xml version="1.0" encoding="utf-8" standalone="yes"?>\\n<topicMap xmlns="http://www.topicmaps.org/xtm/" version="2.1">\\n  <topic>\\n    <subjectIdentifier href="http://psi.example.org/something"/>\\n  </topic>\\n</topicMap>\\n'
        """
        self._out = XMLWriter(fileobj, encoding, prettify)
        self._state = _STATE_ILLEGAL
        self._last_topic = None

    def _set_prettify(self, prettify):
        self._out.prettify = prettify

    prettify = property(lambda self: self._out.prettify, _set_prettify, doc='Indicates if the XML should be prettified')

    #
    # MIOHandler methods
    #
    def startTopicMap(self):
        super(XTM21Handler, self).startTopicMap()
        out = self._out
        out.startDocument()
        out.startElement('topicMap', {'xmlns': voc.XTM, 'version': '2.1'})
        self._state = _STATE_INITIAL

    def endTopicMap(self):
        super(XTM21Handler, self).endTopicMap()
        self._finish_pending_topic()
        self._out.endElement('topicMap')
        self._out.endDocument()

    def startTopic(self, identity):
        super(XTM21Handler, self).startTopic(identity)
        self._start_topic(identity, _STATE_IDENTITY)

    #
    # Hamster handler methods
    #
    def _create_topic_by_iid(self, iri):
        return ITEM_IDENTIFIER, iri

    def _create_topic_by_sid(self, iri):
        return SUBJECT_IDENTIFIER, iri

    def _create_topic_by_slo(self, iri):
        return SUBJECT_LOCATOR, iri

    def _handle_type_instance(self, instance, type):
        if not self._start_topic(instance, _STATE_INSTANCE_OF) and self._state == _STATE_INSTANCE_OF:
            self._write_topic_ref(type)
        else:
            self._out.startElement('instanceOf')
            self._write_topic_ref(type)
            self._state = _STATE_INSTANCE_OF

    def _handle_item_identifier(self, topic, iri):
        self._handle_identity(topic, (ITEM_IDENTIFIER, iri))

    def _handle_subject_identifier(self, topic, iri):
        self._handle_identity(topic, (SUBJECT_IDENTIFIER, iri))

    def _handle_subject_locator(self, topic, iri):
        self._handle_identity(topic, (SUBJECT_LOCATOR, iri))

    def _handle_topicmap_item_identifier(self, iri):
        if self._state not in (_STATE_INITIAL, _STATE_TM_IID):
            msg = 'Ignoring topic map item identifier "%s" since it is not allowed to write it according to the schema' % iri
            logging.warn(msg)
            self._out.comment(msg)
        else:
            self._state = _STATE_TM_IID
            self._write_iid(iri)

    def _handle_topicmap_reifier(self, reifier):
        if self._state != _STATE_INITIAL:
            msg = 'Ignoring topic map reifier "%s" since it is not allowed to write it according to the schema' % reifier
            logging.warn(msg)
            self._out.comment(msg)
        else:
            self._write_reifier(reifier)

    def _create_association(self, type, scope, reifier, iids, roles):
        startElement, endElement = self._out.startElement, self._out.endElement
        write_reifier, write_iids, write_type = self._write_reifier, self._write_iids, self._write_type
        self._finish_pending_topic()
        self._state = _STATE_TOPIC_MAP
        startElement('association')
        write_reifier(reifier)
        write_iids(iids)
        write_type(type)
        self._write_scope(scope)
        for role in roles:
            startElement('role')
            write_reifier(role.reifier)
            write_iids(role.iids)
            write_type(role.type)
            self._write_topic_ref(role.player)
            endElement('role')
        endElement('association')

    def _create_occurrence(self, parent, type, value, datatype, scope, reifier, iids):
        self._start_topic(parent, _STATE_CHARACTERISTIC)
        self._state = _STATE_CHARACTERISTIC
        self._out.startElement('occurrence')
        self._write_reifier(reifier)
        self._write_iids(iids)
        self._write_type(type)
        self._write_scope(scope)
        self._write_value_datatype(value, datatype)
        self._out.endElement('occurrence')

    def _create_name(self, parent, type, value, scope, reifier, iids, variants):
        self._start_topic(parent, _STATE_CHARACTERISTIC)
        self._state = _STATE_CHARACTERISTIC
        self._out.startElement('name')
        self._write_reifier(reifier)
        self._write_iids(iids)
        if type != _DEFAULT_NAME_TYPE:
            self._write_type(type)
        self._write_scope(scope)
        self._out.dataElement('value', value)
        for variant in variants:
            self._out.startElement('variant')
            self._write_reifier(variant.reifier)
            self._write_iids(variant.iids)
            self._write_scope(variant.scope)
            self._write_value_datatype(variant.value, variant.datatype)
            self._out.endElement('variant')
        self._out.endElement('name')

    #
    # Private methods
    #
    def _finish_pending_topic(self):
        if self._last_topic:
            self._finish_pending_instanceof()
            self._out.endElement('topic')
            self._last_topic = None
            self._state = _STATE_TOPIC_MAP

    def _finish_pending_instanceof(self):
        if self._state == _STATE_INSTANCE_OF:
            self._out.endElement('instanceOf')

    def _start_topic(self, identity, next_state):
        def next_state_is_compatible():
            state = self._state
            if state == _STATE_CHARACTERISTIC:
                return next_state == state
            if state == _STATE_TOPIC_MAP:
                return next_state != _STATE_IDENTITY
            if state == _STATE_INSTANCE_OF:
                return next_state in (state, _STATE_CHARACTERISTIC)
            return True
        force_new_topic = not next_state_is_compatible()
        if not force_new_topic and self._last_topic and identity in self._last_topic:
            if self._state != next_state:
                self._finish_pending_instanceof()
            return False
        should_merge = self._last_topic and self._last_topic.should_merge_with(identity) and self._state == _STATE_TOPIC_MAP
        new_topic = not self._last_topic or force_new_topic or (self._last_topic and not (should_merge or identity in self._last_topic))
        if new_topic:
            self._finish_pending_topic()
            self._last_topic = _Topic(identity)
            self._out.startElement('topic')
            self._write_identity(identity)
            self._state = _STATE_TOPIC_MAP
        elif should_merge:
            self._last_topic.add_identity(identity)
            self._write_identity(identity)
            self._state = _STATE_TOPIC_MAP
        return not new_topic

    def _handle_identity(self, main_identity, identity):
        written = False
        if self._last_topic and self._state == _STATE_TOPIC_MAP:
            if main_identity in self._last_topic:
                if identity not in self._last_topic:
                    self._last_topic.add_identity(identity)
                    self._write_identity(identity)
                    written = True
            elif identity in self._last_topic:
                self._last_topic.add_identity(main_identity)
                self._write_identity(main_identity)
                written = True
            elif self._last_topic.should_merge_with(main_identity) or self._last_topic.should_merge_with(identity):
                self._last_topic.add_identity(main_identity)
                self._last_topic.add_identity(identity)
                self._write_identity(main_identity)
                self._write_identity(identity)
                written = True
        if not written:
            self._start_topic(main_identity, _STATE_IDENTITY)
            self._state = _STATE_IDENTITY
            self._last_topic.add_identity(identity)
            self._write_identity(identity)

    def _write_identity(self, ref):
        kind, iri = ref
        if kind == ITEM_IDENTIFIER:
            self._write_iid(iri)
        else:
            self._out.emptyElement(XTM21Handler._IDENTITY2EL[kind], {'href': iri})

    def _write_reifier(self, reifier):
        if reifier:
            self._out.startElement('reifier')
            self._write_topic_ref(reifier)
            self._out.endElement('reifier')

    def _write_type(self, type):
        self._out.startElement('type')
        self._write_topic_ref(type)
        self._out.endElement('type')

    def _write_scope(self, scope):
        if scope:
            self._out.startElement('scope')
            write_topic_ref = self._write_topic_ref
            for theme in scope:
                write_topic_ref(theme)
            self._out.endElement('scope')

    def _write_topic_ref(self, topicref):
        kind, iri = topicref
        self._out.emptyElement(XTM21Handler._TOPICREF2EL.get(kind), {'href': iri})

    def _write_iids(self, iids):
        write_iid = self._write_iid
        for iid in iids:
            write_iid(iid)

    def _write_iid(self, iid):
        self._out.emptyElement('itemIdentity', {'href': iid})

    def _write_value_datatype(self, value, datatype):
        if XSD.anyURI == datatype:
            self._out.emptyElement('resourceRef', {'href': value})
        elif XSD.string == datatype:
            self._out.dataElement('resourceData', value)
        else:
            self._out.dataElement('resourceData', value, {'datatype': datatype})


class _Topic(object):
    """\
    Internal class to keep track about a topic and its identities.

    >>> sid = (SUBJECT_IDENTIFIER, 'http://psi.example.org/something')
    >>> t = _Topic(sid)
    >>> sid in t
    True
    >>> iid = ITEM_IDENTIFIER, 'http://www.example.org'
    >>> iid in t
    False
    >>> t.add_identity(iid)
    >>> iid in t
    True
    >>> iid2 = ITEM_IDENTIFIER, sid[1]
    >>> t.should_merge_with(iid2)
    True
    >>> t.should_merge_with(sid)
    True
    >>> t.should_merge_with(iid)
    True
    >>> slo = SUBJECT_LOCATOR, sid[1]
    >>> t.should_merge_with(slo)
    False
    >>> t.add_identity(slo)
    >>> t.should_merge_with(slo)
    True
    """
    def __init__(self, ref):
        self._refs = [ref]

    def add_identity(self, ref):
        self._refs.append(ref)

    def should_merge_with(self, ref):
        kind, iri = ref
        if kind == SUBJECT_LOCATOR:
            return ref in self._refs
        return (SUBJECT_IDENTIFIER, iri) in self._refs or (ITEM_IDENTIFIER, iri) in self._refs

    def __contains__(self, ref):
        return ref in self._refs


if __name__ == '__main__':
    import doctest
    doctest.testmod()
