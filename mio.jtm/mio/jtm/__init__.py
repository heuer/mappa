# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
JSON Topic Maps (JTM) 1.0/1.1 deserializer.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
from __future__ import absolute_import
from tm import mio, XSD, TMDM
from tm.irilib import resolve_iri
from tm.mio.deserializer import Deserializer
from . import json

__all__ = ['create_deserializer']

_EMPTY = tuple()

_NS_XSD = XSD.string.replace('string', '')
_DEFAULT_NAME_TYPE = mio.SUBJECT_IDENTIFIER, TMDM.topic_name

_ITEM_TYPES_SUPPORTED = (
    u'topicmap',
    u'topic',
    u'association',
    u'occurrence',
    u'name'
)

_ITEM_TYPES_UNSUPPORTED = (
    u'role',
    u'variant'
)

_ITEM_TYPES = _ITEM_TYPES_SUPPORTED + _ITEM_TYPES_UNSUPPORTED

_IDENTITY2METHOD = {
    mio.SUBJECT_IDENTIFIER: u'subjectIdentifier',
    mio.SUBJECT_LOCATOR: u'subjectLocator',
    mio.ITEM_IDENTIFIER: u'itemIdentifier',
}

_IDENTITYPREFIX2MIO = {
    u'ii': mio.ITEM_IDENTIFIER,
    u'si': mio.SUBJECT_IDENTIFIER,
    u'sl': mio.SUBJECT_LOCATOR,
}

def create_deserializer(version=None, **kw): # pylint: disable-msg=W0613
    return JTMDeserializer()

class JTMDeserializer(Deserializer):
    def __init__(self, version=None):
        super(JTMDeserializer, self).__init__()

    def _do_parse(self, source):
        """\

        """
        dct = None
        if source.stream:
            dct = json.load(source.stream)
        else:
            dct = json.load(source.iri)
        version = dct.get(u'version', u'1.0')
        if version not in (u'1.0', u'1.1'):
            raise mio.MIOException('Unknown JTM version "%s"' % version)
        _issue_events(self.handler, source.iri, dct, version)


def _issue_events(handler, base_iri, dct, version):
    version = float(version)
    prefixes = dct.get(u'prefixes', {})
    if prefixes and not version > 1.0:
        raise mio.MIOException('Prefixes are not allowed in JTM 1.0')
    prefixes[None] = base_iri
    xsd_iri = prefixes.get(u'xsd', None)
    if xsd_iri and xsd_iri != _NS_XSD:
        raise mio.MIOException('The prefix "xsd" is predefined and cannot be bound to "%s"' % xsd_iri)
    else:
        prefixes[u'xsd'] = _NS_XSD
    item_type = dct.get(u'item_type', u'').lower()
    if item_type not in _ITEM_TYPES:
        raise mio.MIOException('Unknown item type: "%s"' % item_type)
    if item_type not in _ITEM_TYPES_SUPPORTED:
        raise mio.MIOException('The item type "%s" is not supported' % item_type)
    if item_type == u'association':
        _handle_association(handler, prefixes, dct)
    elif item_type == u'topic':
        _handle_topic(handler, prefixes, dct)
    elif item_type == u'occurrence':
        _handle_occurrence(handler, prefixes, dct)
    elif item_type == u'name':
        _handle_name(handler, prefixes, dct)
    else:
        _handle_reifier(handler, prefixes, dct)
        for k, v in ((k, v) for k, v in dct.iteritems() if k not in (u'version', u'prefixes', u'item_type', u'reifier')):
            if k == u'item_identifiers':
                _handle_iids(handler, prefixes, dct)
            elif k == u'topics':
                for topic in v:
                    _handle_topic(handler, prefixes, topic, version)
            elif k == u'associations':
                for assoc in v:
                    _handle_association(handler, prefixes, assoc)

def _resolve_topicref(prefixes, ref):
    kind = _IDENTITYPREFIX2MIO.get(ref[:2], None)
    if kind is None:
        raise mio.MIOException('Unknown identity type: "%s"' % ref[:2])
    return kind, _resolve_iri(prefixes, ref[3:])

def _resolve_iri(prefixes, qiri):
    if qiri[0] == '[':
        if qiri[-1] != ']':
            raise mio.MIOException('Illegal QName: "%s"' % qiri)
        colon_idx = qiri.find(u':')
        if not colon_idx > 0:
            raise mio.MIOException('Illegal QName: "%s"' % qiri)
        prefix, local = qiri[1:colon_idx], qiri[colon_idx+1:-1]
        base = prefixes.get(prefix, None)
        if base is None:
            raise mio.MIOException('Undefined prefix "%s"' % prefix)
        iri = resolve_iri(base, local)
    else:
        iri = resolve_iri(prefixes[None], qiri)
    return iri

def _handle_topic(handler, prefixes, dct, version=1.0):
    types = dct.get(u'instance_of', _EMPTY)
    if types and not version >= 1.1:
        raise mio.MIOException('"instance_of" is illegal in version "%s"' % version)
    kind, iri = None, None
    sids, slos, iids = dct.get(u'subject_identifiers', _EMPTY), dct.get(u'subject_locators', _EMPTY), dct.get(u'item_identifiers', _EMPTY)
    if sids:
        kind, iri = mio.SUBJECT_IDENTIFIER, sids[0]
        sids = sids[1:]
    elif slos:
        kind, iri = mio.SUBJECT_LOCATOR, slos[0]
        slos = slos[1:]
    elif iids:
        kind, iri = mio.ITEM_IDENTIFIER, iids[0]
        iids = iids[1:]
    handler.startTopic((kind, _resolve_iri(prefixes, iri)))
    for sid in sids:
        handler.subjectIdentifier(_resolve_iri(prefixes, sid))
    for slo in slos:
        handler.subjectLocator(_resolve_iri(prefixes, slo))
    for iid in iids:
        handler.itemIdentifier(_resolve_iri(prefixes, iid))
    for typ in types:
        handler.isa(_resolve_topicref(prefixes, typ))
    for occ in dct.get(u'occurrences', _EMPTY):
        _handle_occurrence(handler, prefixes, occ)
    for name in dct.get(u'names', _EMPTY):
        _handle_name(handler, prefixes, name)
    handler.endTopic()

def _get_type(prefixes, dct, default=None):
    type_ = dct.get(u'type', None)
    if not type_:
        if default:
            return default
        raise mio.MIOException('Expected a type')
    return _resolve_topicref(prefixes, type_)


def _handle_scope(handler, prefixes, dct):
    scope = dct.get(u'scope', _EMPTY)
    if scope:
        handler.startScope()
        for theme in scope:
            handler.theme(_resolve_topicref(prefixes, theme))
        handler.endScope()


def _handle_iids(handler, prefixes, dct):
    for iid in dct.get(u'item_identifiers', _EMPTY):
        handler.itemIdentifier(_resolve_iri(prefixes, iid))


def _handle_reifier(handler, prefixes, dct):
    reifier = dct.get(u'reifier', None)
    if reifier:
        handler.reifier(_resolve_topicref(prefixes, reifier))


def _handle_value_datatype(handler, prefixes, dct):
    value, datatype = dct[u'value'], _resolve_iri(prefixes, dct.get(u'datatype', XSD.string))
    if datatype == XSD.anyURI:
        value = _resolve_iri(prefixes, value)
    handler.value(value, datatype)


def _handle_association(handler, prefixes, dct):
    handler.startAssociation(_get_type(prefixes, dct))
    for role in dct.get(u'roles', _EMPTY):
        handler.startRole(_get_type(prefixes, role))
        handler.player(_resolve_topicref(prefixes, role.get(u'player')))
        _handle_reifier(handler, prefixes, role)
        _handle_iids(handler, prefixes, role)
        handler.endRole()
    _handle_iids(handler, prefixes, dct)
    _handle_reifier(handler, prefixes, dct)
    _handle_scope(handler, prefixes, dct)
    handler.endAssociation()


def _start_parent(handler, prefixes, dct):
    parent = dct.get(u'parent', _EMPTY)
    if parent:
        handler.startTopic(_resolve_topicref(prefixes, parent[0]))
        for kind, iri in (_resolve_topicref(prefixes, iri) for iri in parent[1:]):
            getattr(handler, _IDENTITY2METHOD[kind])(iri)
        return True
    return False

def _handle_occurrence(handler, prefixes, dct):
    parent = _start_parent(handler, prefixes, dct)
    handler.startOccurrence(_get_type(prefixes, dct))
    _handle_reifier(handler, prefixes, dct)
    _handle_scope(handler, prefixes, dct)
    _handle_value_datatype(handler, prefixes, dct)
    _handle_iids(handler, prefixes, dct)
    handler.endOccurrence()
    if parent:
        handler.endTopic()

def _handle_name(handler, prefixes, dct):
    parent = _start_parent(handler, prefixes, dct)
    handler.startName(_get_type(prefixes, dct, default=_DEFAULT_NAME_TYPE))
    _handle_reifier(handler, prefixes, dct)
    _handle_scope(handler, prefixes, dct)
    handler.value(dct[u'value'])
    _handle_iids(handler, prefixes, dct)
    for var in dct.get(u'variants', _EMPTY):
        handler.startVariant()
        _handle_scope(handler, prefixes, var)
        _handle_value_datatype(handler, prefixes, var)
        _handle_reifier(handler, prefixes, var)
        _handle_iids(handler, prefixes, var)
        handler.endVariant()
    handler.endName()
    if parent:
        handler.endTopic()

