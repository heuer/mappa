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
    __slots__ = ['_writer', '_base', 'prettify', 'export_iids', 'omit_loners', 'version']

    def __init__(self, out, base, version=1.0):
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

    def write(self, topicmap):
        """\
        Serializes the specified ``topicmap``.
        """
        writer = self._writer
        writer.prettify = self.prettify
        writer.start()
        writer.start_object()
        writer.key_value('version', str(self.version))
        writer.key_value('item_type', 'topicmap')
        self._write_iids(topicmap)
        self._write_reifier(topicmap)
        write_if_available = self._write_if_available
        write_if_available('topics', topicmap.topics, self._write_topic)
        write_if_available('associations', topicmap.associations, self._write_association)
        writer.end_object()
        writer.end()

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
            writer.array('item_identifiers', iids)
        writer.array('subject_identifiers', sids)
        writer.array('subject_locators', slos)
        write_if_available = self._write_if_available
        write_if_available('occurrences', topic.occurrences, self._write_occurrence)
        write_if_available('names', topic.names, self._write_name)
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
        writer.key('roles')
        writer.start_array()
        for role in association.roles:
            start_object()
            write_iids(role)
            write_type(role)
            writer.key_value('player', self._topic_ref(role.player))
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
        self._write_if_available('variants', name.variants, self._write_variant)
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
        self._writer.key_value('value', tmc.value)

    def _write_datatype(self, tmc):
        """\
        Writes the ``datatype`` attribute of ``tmc``.
        """
        dt = tmc.datatype
        if not XSD.string == dt:
            if self.version >= 1.1 and dt.startswith(XSD):
                dt = '[xsd:%s]' % dt.replace(XSD, '')
            self._writer.key_value('datatype', dt)

    def _write_iids(self, reifiable):
        """\
        Writes the item identifiers of ``reifiable`` if any.
        """
        if self.export_iids:
            self._writer.array('item_identifiers', reifiable.iids)

    def _write_scope(self, scoped):
        """\
        Writes the scope of ``scoped`` if it is not unconstrained.
        """
        self._writer.array('scope', map(self._topic_ref, scoped.scope))

    def _write_type(self, typed):
        """\
        Writes the type of the ``typed`` Topic Maps construct.
        """
        self._writer.key_value('type', self._topic_ref(typed.type))

    def _write_reifier(self, reifiable):
        """\
        Writes the reifier of the ``reifiable`` Topic Maps construct, if any.
        """
        if reifiable.reifier:
            self._writer.key_value('reifier', self._topic_ref(reifiable.reifier))

    def _topic_ref(self, topic):
        """\
        Returns a reference to the ``topic``. 
        
        If the topic has no subject identifiers, subject locators or 
        item identifiers, an item identifier is generated with the 
        ``base`` and the id of the topic.
        """
        res = one_of(topic.sids)
        if res:
            res = 'si:%s' % res
        else:
            res = one_of(topic.slos)
            if res:
                res = 'sl:%s' % res
            else:
                res = 'ii:%s' % (one_of(topic.iids) or '%s#id-%s' % (self._base, topic.id))
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
