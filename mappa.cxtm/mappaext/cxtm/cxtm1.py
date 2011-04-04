# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2009 -- Lars Heuer - Semagia <http://www.semagia.com/>.
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
`Canonical XTM (CXTM) <http://www.isotopicmaps.org/cxtm/>`_ serializer.

CXTM is a format that guarantees that two equivalent Topic Maps Data Model 
instances [ISO/IEC 13250-2] will always produce byte-by-byte identical 
serializations, and that non-equivalent instances will always produce 
different serializations.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:version:      $Rev: 251 $ - $Date: 2009-08-12 14:52:04 +0200 (Mi, 12 Aug 2009) $
:license:      BSD license
"""
import codecs
from mappa import XSD
from mappa.utils import remove_duplicates, is_occurrence

__all__ = ['CXTMTopicMapWriter']

try:
    enumerate([], start=0)
except TypeError:
    from itertools import count, izip
    #pylint: disable-msg= W0622
    def enumerate(iterable, start=0):
        return izip(count(start), iterable)

def enum(iterable):
    """\
    Same as ``enumerate`` but starts with ``1``.
    """
    return enumerate(iterable, start=1)

class CXTMTopicMapWriter(object):
    """\
    Serializer that writes CXTM.
    """
    def __init__(self, out, base):
        """\
        Initializes the canonicalizer.
        
        `out`
            File object, which provides at least the ``write`` and ``flush``
            methods.
        `base`
            An IRI which is used to resolve IRIs against.
        """
        if not out:
            raise TypeError('"out" is not specified')
        if not base:
            raise TypeError('"base" is not specified')
        self._writer = CXTMWriter(out)
        self._base = self._normalize_baseiri(base)
        self._iri2norm = {}
        self._topics = None
        self._assocs = None
        self._assoc2roles = None
        self._tmc2id = None

    def write(self, topicmap):
        """\
        Serializes the `topicmap` into CXTM.
        
        `topicmap`
            The topic map to serialize. The topic map MUST NOT contain duplicate
            Topic Maps constructs.
        """
        remove_duplicates(topicmap)
        self._create_index(topicmap)
        writer = self._writer
        writer.startDocument()
        writer.startElement('topicMap', self._add_reifier({}, topicmap))
        writer.newline()
        self._write_iids(topicmap)
        write_topic = self._write_topic
        for topic in self._topics:
            write_topic(topic)
        write_assoc = self._write_association
        for assoc in self._assocs:
            write_assoc(assoc)
        writer.endElement('topicMap')
        writer.newline()
        writer.endDocument()
        self._topics = None
        self._assocs = None
        self._assoc2roles = None
        self._tmc2id = None
        self._iri2norm = None

    def _index(self, construct):
        """\
        Returns the index of the Topic Maps ``construct``.
        
        `construct`
            A topic, an association or a role.
        """
        return self._tmc2id[construct]

    def _create_index(self, topicmap):
        """\
        Creates an index for the topics and associations (with the roles) which
        belong to the ``topicmap``.
        
        `topicmap`
            The topic map to create the index for.
        """
        self._topics = sorted(topicmap.topics, self._cmp_topic)
        assoc2roles = {}
        self._tmc2id = {}
        tmc2id = self._tmc2id
        for i, topic in enum(self._topics):
            tmc2id[topic] = i
        self._assocs = sorted(topicmap.associations, self._cmp_assoc)
        for i, assoc in enum(self._assocs):
            tmc2id[assoc] = i
            roles = sorted(assoc.roles, self._cmp_role_ignore_parent)
            assoc2roles[assoc] = roles
            for j, role in enum(roles):
                tmc2id[role] = j
        self._assoc2roles = assoc2roles

    def _write_topic(self, topic):
        """\
        Serializes the ``topic``.
        """
        index_of = self._index
        startElement, endElement, newline = self._writer.startElement, self._writer.endElement, self._writer.newline
        startElement('topic', {'number': index_of(topic)})
        newline()
        self._write_locators('subjectIdentifiers', topic.sids)
        self._write_locators('subjectLocators', topic.slos)
        self._write_iids(topic)
        write_name = self._write_name
        for pos, name in enum(self._names(topic)):
            write_name(name, pos)
        write_occurrence = self._write_occurrence
        for pos, occ in enum(self._occs(topic)):
            write_occurrence(occ, pos)
        emptyElement = self._writer.emptyElement
        for role in sorted(topic.roles_played, self._cmp_role):
            emptyElement('rolePlayed', {'ref': 'association.%s.role.%s' % (index_of(role.parent), index_of(role))})
            newline()
        endElement('topic')
        newline()

    def _write_association(self, association):
        """\
        Serializes the ``association``.
        """
        index_of = self._index
        attrs = self._attributes
        startElement, endElement, newline = self._writer.startElement, self._writer.endElement, self._writer.newline
        topic_ref = self._topic_ref
        startElement('association', attrs(association, index_of(association)))
        newline()
        write_type, write_iids = self._write_type, self._write_iids
        write_type(association)
        emptyElement = self._writer.emptyElement
        for role in self._roles(association):
            startElement('role', attrs(role, index_of(role)))
            newline()
            emptyElement('player', topic_ref(role.player))
            newline()
            write_type(role)
            write_iids(role)
            endElement('role')
            newline()
        self._write_scope(association)
        write_iids(association)
        endElement('association')
        newline()

    def _write_name(self, name, pos):
        """\
        Serializes the ``name``.
        
        `name`
            The name to serialize.
        `pos`
            The position of the name within the parent topic.
        """
        attrs = self._attributes
        startElement, endElement, newline = self._writer.startElement, self._writer.endElement, self._writer.newline
        startElement('name', attrs(name, pos))
        newline()
        self._write_value(name.value)
        self._write_type(name)
        self._write_scope(name)
        write_datatyped_construct = self._write_datatyped_construct
        for vpos, variant in enum(self._variants(name)):
            startElement('variant', attrs(variant, vpos))
            write_datatyped_construct(variant)
            endElement('variant')
            newline()
        self._write_iids(name)
        endElement('name')
        newline()

    def _write_occurrence(self, occurrence, pos):
        """\
        Serializes the ``occurrence``.
        
        `occurrence`
            The occurrence to serialize.
        `pos`
            The position of the occurrence within the parent topic.
        """
        writer = self._writer
        writer.startElement('occurrence', self._attributes(occurrence, pos))
        self._write_datatyped_construct(occurrence)
        writer.endElement('occurrence')
        writer.newline()

    def _write_iids(self, construct):
        """\
        Serializes the item identifiers of the ``construct``.
        """
        self._write_locators('itemIdentifiers', construct.iids)

    def _write_locators(self, name, locs):
        """\
        Serializes the locators using a root element ``name``.
        """
        if not locs:
            return
        newline = self._writer.newline
        self._writer.startElement(name)
        newline()
        normalize_iri = self._normalize_iri
        dataElement = self._writer.dataElement
        for loc in sorted([normalize_iri(loc) for loc in locs]):
            dataElement('locator', loc)
            newline()
        self._writer.endElement(name)
        newline()

    def _write_datatyped_construct(self, construct):
        """\
        Writes the characteristics of an occurrence or variant.
        
        `construct`
            An occurrence or variant.
        """
        writer = self._writer
        value, dt = construct.value, construct.datatype
        if dt == XSD.anyURI:
            value = self._normalize_iri(value)
        writer.newline()
        self._write_value(value)
        writer.dataElement('datatype', dt)
        writer.newline()
        if (is_occurrence(construct)):
            self._write_type(construct)
        self._write_scope(construct)
        self._write_iids(construct)

    def _write_value(self, value):
        """\
        Writes the specified value.
        
        `value`
            A string.
        """
        writer = self._writer
        writer.dataElement('value', value)
        writer.newline()

    def _write_type(self, typed):
        """\
        Writes the type of a ``typed`` Topic Maps construct.
        
        `typed`
            An association, a role, an occurrence, or name.
        """
        writer = self._writer
        writer.emptyElement('type', self._topic_ref(typed.type))
        writer.newline()

    def _write_scope(self, scoped):
        """\
        Serializes the scope of the ``scoped`` Topic Maps construct if the 
        scope is not the unconstrained scope.
        
        `scoped`
            An association, an occurrence, a name, or variant.
        """
        newline = self._writer.newline
        emptyElement = self._writer.emptyElement
        written = False
        for i, theme in enumerate(sorted(scoped.scope, self._cmp_topic)):
            if not i:
                self._writer.startElement('scope')
                newline()
                written = True
            emptyElement('scopingTopic', self._topic_ref(theme))
            newline()
        if written:
            self._writer.endElement('scope')
            newline()

    def _occs(self, topic):
        """\
        Returns sorted occurrences from the `topic`.
        """
        return sorted(topic.occurrences, self._cmp_occ)

    def _names(self, topic):
        """\
        Returns sorted names from the `topic`.
        """
        return sorted(topic.names, self._cmp_name)

    def _roles(self, association):
        """\
        Returns sorted roles from the `association`.
        """
        return self._assoc2roles[association]

    def _variants(self, name):
        """\
        Returns sorted variants from the `name`.
        """
        return sorted(name.variants, self._cmp_variant)

    def _attributes(self, reifiable, pos):
        """\
        Returns a ``dict`` with the number of the ``reifiable`` Topic Maps 
        construct and the index of the reifier (if any).
        
        `reifiable`
            A reifiable Topic Maps construct.
        `pos`
            The position of the reifiable construct within its parent context.
        """
        return self._add_reifier({'number': pos}, reifiable)

    def _add_reifier(self, attrs, reifiable):
        """\
        Adds the index of the reifier (if any) to the `attrs`.
        """
        reifier = reifiable.reifier
        if reifier:
            attrs['reifier'] = self._index(reifier)
        return attrs

    def _topic_ref(self, topic):
        """\
        Returns a ``dict`` with a ``topicref`` attribute.
        
        `topic`
            A topic to which the ``topicref`` should point to.
        """
        return {'topicref': self._index(topic)}

    def _normalize_iri(self, iri):
        """\
        Normalizes the specified ``iri``.
        """
        def clean(iri):
            import unicodedata
            from urllib import unquote
            # Converts the percent encoding into a Unicode equivalent
            # 'Normalizing' IRIs while writing might be wrong, though.
            if not isinstance(iri, unicode):
                iri = unicode(unquote(iri), 'utf-8', 'replace')
            else:
                iri = unquote(iri)
            return unicodedata.normalize('NFC', iri).encode('utf-8')
        normalized = self._iri2norm.get(iri)
        if normalized:
            return normalized
        normalized = iri
        base = self._base
        if normalized.startswith(base):
            normalized = normalized.lstrip(base)
        else:
            i = 0
            slash_pos = -1
            max_len = min(len(normalized), len(base))
            while i < max_len and base[i] == normalized[i]:
                if base[i] == '/':
                    slash_pos = i
                i+=1
            if slash_pos > -1:
                normalized = normalized[slash_pos:]
        if normalized and normalized[0] == '/':
            normalized = normalized[1:]
        normalized = clean(normalized)
        self._iri2norm[iri] = normalized
        return normalized

    def _normalize_baseiri(self, iri):
        """\
        Normalizes the base locator according to the following procedure 
        (CXTM 3.19 - 1.):
        
            [...] the base locator with any fragment identifier and query 
            removed and any trailing "/" character removed.[...]
        
        """
        i = iri.rfind('#')
        if i > 0:
            iri = iri[:i]
        i = iri.rfind('?')
        if i > 0:
            iri = iri[:i]
        if iri[-1] == '/':
            iri = iri[:-1]
        return iri

    def _cmp_topic(self, a, b):
        """\
        Canonical sort order:
        1. [subject identifiers]
        2. [subject locators]
        3. [item identifiers]
        """
        if a == b:
            return 0
        cmp_locators = self._cmp_locators
        return cmp_locators(a.sids, b.sids) \
                or cmp_locators(a.slos, b.slos) \
                or cmp_locators(a.iids, b.iids)

    def _cmp_role_ignore_parent(self, a, b):
        """\
        Role comparator which ignores the parent association.
        """
        if a == b:
            return 0
        return self._cmp_topic(a.player, b.player) or self._cmp_topic(a.type, b.type)
    
    def _cmp_role(self, a, b):
        """\
        Canonical sort order:
        1. [player]
        2. [type]
        3. [parent]
        """
        if a == b:
            return 0
        return self._cmp_role_ignore_parent(a, b) or self._cmp_assoc(a.parent, b.parent)
    
    def _cmp_assoc(self, a, b):
        """\
        Canonical sort order:
        1. [type]
        2. [roles]
        3. [scope]
        4. [parent]
        """
        if a == b:
            return 0
        return self._cmp_topic(a.type, b.type) \
                or self._cmp_roles(a.roles, b.roles) \
                or self._cmp_scope(a, b)

    def _cmp_occ(self, a, b):
        """\
        Canonical sort order:
        1. [value]
        2. [datatype]
        3. [type]
        4. [scope]
        5. [parent]
        """
        if a == b:
            return 0
        return cmp(a.value, b.value) \
                or cmp(a.datatype, b.datatype) \
                or self._cmp_topic(a.type, b.type) \
                or self._cmp_scope(a, b)

    def _cmp_name(self, a, b):
        """\
        Canonical sort order:
        1. [value]
        2. [type]
        3. [scope]
        4. [parent]
        """
        if a == b:
            return 0
        return cmp(a.value, b.value) or self._cmp_topic(a.type, b.type) \
                or self._cmp_scope(a, b)

    def _cmp_variant(self, a, b):
        """\
        Canonical sort order:
        1. [value]
        2. [datatype]
        3. [scope]
        4. [parent]
        """
        if a == b:
            return 0
        return cmp(a.value, b.value) or cmp(a.datatype, b.datatype) \
                or self._cmp_scope(a, b)

    def _cmp_size(self, a, b):
        """\
        Compares the size of ``a`` and ``b``.
        """
        return len(a) - len(b)
    
    def _cmp_set_content(self, a, b, comparator=cmp):
        """\
        Compares the content of ``a`` and ``b``. 
        
        Both must have the same size.
        """
        coll_a = sorted(a, comparator)
        coll_b = sorted(b, comparator)
        for i in xrange(len(a)):
            res = comparator(coll_a[i], coll_b[i])
            if res:
                return res
        return 0

    def _cmp_locators(self, a, b):
        """\
        Compares the locator collection ``a`` and ``b``.
        """
        normalize_iri = self._normalize_iri
        return self._cmp_size(a, b) \
                or self._cmp_set_content([normalize_iri(iri) for iri in a], 
                                         [normalize_iri(iri) for iri in b])

    def _cmp_roles(self, a, b):
        """\
        Compares the collections `a` and `b`. Both collections must consist 
        of roles.
        """
        return self._cmp_size(a, b) \
                or self._cmp_set_content(a, b, self._cmp_role_ignore_parent)
    
    def _cmp_scope(self, a, b):
        """\
        Compares the scope of the scoped constructs `a` and `b`.
        """
        scope_a = list(a.scope)
        scope_b = list(b.scope)
        return self._cmp_size(scope_a, scope_b) \
                or self._cmp_set_content(scope_a, scope_b, self._cmp_topic)

class CXTMWriter(object):
    """\
    A canonical XML writer which provides a subset of C14N-XML.
    """

    def __init__(self, out):
        self._out = codecs.getwriter('utf-8')(out)

    def startDocument(self):
        """\
        Notification about the start of the writing.
        """
        pass

    def endDocument(self):
        """\
        Forces a flush on the underlying file object.
        """
        self._out.flush()

    def startElement(self, name, attrs=None):
        """\
        Serializes a start tag with the optional attributes (a dict)
        """
        out = self._out
        out.write(u'<%s' % name)
        if attrs:
            for name in sorted(attrs.keys()):
                out.write(u' %s="%s"' % (name, _escape_attr_value(attrs[name])))
        out.write(u'>')

    def endElement(self, name):
        """\
        Serializes an end tag.
        """
        self._out.write(u'</%s>' % name)

    def dataElement(self, name, data, attrs=None):
        """\
        Writes <name attr="attr-val" attr1="attr1-val">data</name> to the output.
        """
        self.startElement(name, attrs)
        self.characters(data)
        self.endElement(name)

    def emptyElement(self, name, attrs=None):
        """\
        Writes <name attr="attr-val" attr1="attr1-val"></name> to the output.
        """
        self.startElement(name, attrs)
        self.endElement(name)

    def characters(self, data):
        """\
        Serializes the specified `data` in escaped form (if necessary).
        """
        self._out.write(_escape_text(data))

    def newline(self):
        """\
        Writes a nl character.
        """
        self._out.write(u'\n')


def _escape_text(val):
    """\
    Escapes content according to canonical XML.
    """
    return val.replace(u'&', u'&amp;') \
                .replace(u'\r', u'&#xD;') \
                .replace(u'<', u'&lt;') \
                .replace(u'>', u'&gt;')

def _escape_attr_value(val):
    """\
    Escapes the attribute's value according to canonical XML.
    """
    if isinstance(val, int):
        return val
    return val.replace(u'&', u'&amp;') \
                .replace(u'\t', u'&#x9;') \
                .replace(u'\n', u'&#xA;') \
                .replace(u'\r', u'&#xD;') \
                .replace(u'"', u'&quot;') \
                .replace(u'<', u'&lt;')
