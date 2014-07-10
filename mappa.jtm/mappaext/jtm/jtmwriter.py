# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
A ``TopicMapWriter`` implementation that serializes a topic map into
a `JSON Topic Maps (JTM) <http://www.cerny-online.com/jtm/>`_ representation.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
from tm.voc import XSD
from mio.jtm.json import JSONWriter
from mappa._internal.it import one_of, no
from mappa.utils import is_default_name, is_default_name_type


class JTMTopicMapWriter(object):
    """\
    Writer for JSON Topic Maps (JTM).
    """
    __slots__ = ['_writer', '_base', 'prettify', 'export_iids',
                 'omit_loners', 'version', 'prefixes']

    def __init__(self, out, base, version=1.0, prefixes=None):
        if not out:
            raise ValueError('"out" is not specified')
        if not base:
            raise ValueError('"base" is not specified')
        self._writer = JSONWriter(out)
        self._base = base
        self.prettify = False
        self.export_iids = True
        self.version = version
        self.omit_loners = False
        self.prefixes = {}
        if prefixes:
            for ident, iri in prefixes.iteritems():
                self.add_prefix(ident, iri)

    def add_prefix(self, ident, iri):
        """\
        Adds a prefix/IRI binding.
        """
        if self.version < 1.1:
            raise ValueError('JTM versions <= 1.1 do not support prefixes')
        else:
            if u'xsd' == ident.lower() and iri != XSD:
                raise ValueError('The prefix "xsd" is reserved')
            self.prefixes[ident] = iri

    def write(self, topicmap):
        """\
        Serializes the specified ``topicmap``.
        """
        writer = self._writer
        writer.prettify = self.prettify
        writer.start()
        writer.start_object()
        writer.key_value(u'version', unicode(self.version))
        self._write_prefixes()
        writer.key_value(u'item_type', u'topicmap')
        self._write_iids(topicmap)
        self._write_reifier(topicmap)
        write_if_available = self._write_if_available
        write_if_available(u'topics', topicmap.topics, self._write_topic)
        write_if_available(u'associations', topicmap.associations, self._write_association)
        writer.end_object()
        writer.end()

    def _write_prefixes(self):
        if self.prefixes:
            writer = self._writer
            writer.key(u'prefixes')
            writer.start_object()
            for ident, iri in self.prefixes.iteritems():
                writer.key_value(ident, iri)
            writer.end_object()

    def _uri(self, uri):
        if self.version >= 1.1:
            for prefix, iri in self.prefixes.iteritems():
                if uri.startswith(iri):
                    return u'[%s:%s]' % (prefix, uri[len(iri):])
        return uri

    def _uris(self, uris):
        uri = self._uri
        return (uri(u) for u in uris)

    def _write_topic(self, topic):
        """\
        Serializes the ``topic``.
        """
        iids = tuple(topic.iids)
        sids = tuple(topic.sids)
        slos = tuple(topic.slos)
        if (self.omit_loners or is_default_name_type(topic)) and _is_omitable(topic, sids, slos, iids):
            return
        writer = self._writer
        writer.start_object()
        if self.export_iids or not (sids or slos):
            writer.array(u'item_identifiers', self._uris(iids))
        writer.array(u'subject_identifiers', self._uris(sids))
        writer.array(u'subject_locators', self._uris(slos))
        write_if_available = self._write_if_available
        write_if_available(u'occurrences', topic.occurrences, self._write_occurrence)
        write_if_available(u'names', topic.names, self._write_name)
        writer.end_object()

    def _write_association(self, association):
        """\
        Serializes the ``association`` incl. its roles.
        """
        writer = self._writer
        start_object, end_object = self._writer.start_object, self._writer.end_object
        write_iids, write_type, write_reifier = self._write_iids, self._write_type, self._write_reifier
        start_object()
        write_iids(association)
        write_type(association)
        self._write_scope(association)
        write_reifier(association)
        writer.key(u'roles')
        writer.start_array()
        for role in association.roles:
            start_object()
            write_iids(role)
            write_type(role)
            writer.key_value(u'player', self._topic_ref(role.player))
            write_reifier(role)
            end_object()
        writer.end_array()
        writer.end_object()

    def _write_name(self, name):
        """\
        Serializes the ``name``.
        """
        writer = self._writer
        writer.start_object()
        self._write_iids(name)
        if not is_default_name(name):
            self._write_type(name)
        self._write_scope(name)
        self._write_reifier(name)
        self._write_value(name)
        self._write_if_available(u'variants', name.variants, self._write_variant)
        self._writer.end_object()

    def _write_variant(self, variant):
        """\
        Serializes the ``variant``.
        """
        self._writer.start_object()
        self._write_iids(variant)
        self._write_scope(variant)
        self._write_reifier(variant)
        self._write_value(variant)
        self._write_datatype(variant)
        self._writer.end_object()

    def _write_occurrence(self, occurrence):
        """\
        Serializes the ``occurrence``.
        """
        self._writer.start_object()
        self._write_iids(occurrence)
        self._write_type(occurrence)
        self._write_scope(occurrence)
        self._write_reifier(occurrence)
        self._write_value(occurrence)
        self._write_datatype(occurrence)
        self._writer.end_object()

    def _write_value(self, tmc):
        """\
        Writes the ``value`` attribute of ``tmc``.
        """
        self._writer.key_value(u'value', tmc.value)

    def _write_datatype(self, tmc):
        """\
        Writes the ``datatype`` attribute of ``tmc``.
        """
        dt = tmc.datatype
        if not XSD.string == dt:
            if self.version >= 1.1:
                if dt.startswith(XSD):
                    dt = u'[xsd:%s]' % dt.replace(XSD, '')
                else:
                    dt = self._uri(dt)
            self._writer.key_value(u'datatype', dt)

    def _write_iids(self, reifiable):
        """\
        Writes the item identifiers of ``reifiable`` if any.
        """
        if self.export_iids:
            self._writer.array(u'item_identifiers', self._uris(reifiable.iids))

    def _write_scope(self, scoped):
        """\
        Writes the scope of ``scoped`` if it is not unconstrained.
        """
        self._writer.array(u'scope', map(self._topic_ref, scoped.scope))

    def _write_type(self, typed):
        """\
        Writes the type of the ``typed`` Topic Maps construct.
        """
        self._writer.key_value(u'type', self._topic_ref(typed.type))

    def _write_reifier(self, reifiable):
        """\
        Writes the reifier of the ``reifiable`` Topic Maps construct, if any.
        """
        if reifiable.reifier:
            self._writer.key_value(u'reifier', self._topic_ref(reifiable.reifier))

    def _topic_ref(self, topic):
        """\
        Returns a reference to the ``topic``. 
        
        If the topic has no subject identifiers, subject locators or 
        item identifiers, an item identifier is generated with the 
        ``base`` and the id of the topic.
        """
        res = one_of(topic.sids)
        if res:
            res = u'si:%s' % self._uri(res)
        else:
            res = one_of(topic.slos)
            if res:
                res = u'sl:%s' % self._uri(res)
            else:
                res = one_of(topic.iids)
                if res:
                    self._uri(res)
                else:
                    res = u'%s#id-%s' % (self._base, topic.id)
                res = u'ii:%s' % res
        return res

    def _write_if_available(self, key, iterable, func):
        """\
        Serializes the ``iterable`` using ``func`` iff ``iterable`` is not empty.
        """
        writer = self._writer
        written = False
        for i, e in enumerate(iterable):
            if not i:
                writer.key(key)
                writer.start_array()
                written = True
            func(e)
        if written:
            writer.end_array()


def _is_omitable(topic, sids, slos, iids):
    """\
    Returns if the `topic` has just one identity and no further 
    characteristics (occurrences, names).
    """
    # No need to check 'roles played' and 'reified' here since
    # the reified statement refers to the topic already and
    # the roles played are serialized through the associations
    return len(iids) + len(sids) + len(slos) <= 1 \
            and no(topic.names) \
            and no(topic.occurrences)
