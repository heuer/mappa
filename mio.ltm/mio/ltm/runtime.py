# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
Linear Topic Maps Notation (LTM) 1.3 runtime environment.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
from tm import mio, Source
from tm.irilib import resolve_iri
from tm.mio.deserializer import Context


class LTMContext(object):
    """\
    
    """
    def __init__(self, handler, iri, subordinate, legacy=False, included_by=None, context=None):
        self.handler = handler
        self._legacy = legacy
        self._is_subordinate = subordinate
        self._slo_prefixes = {}
        self._sid_prefixes = {}
        self._doc_iri = iri
        self._base_iri = iri
        self._seen_base = False
        self._included_by = included_by or set()
        self._mergemaps = set()
        self._context = context or Context()
        self._context.add_loaded(iri)

    def include(self, iri):
        included_by = set(self._included_by)
        included_by.add(self._doc_iri)
        self.merge_ltm(iri, included_by)

    def merge_ltm(self, iri, included=None):
        doc_iri = self.resolve_iri(iri)
        if doc_iri in self._context.loaded:
            return
        self._context.add_loaded(doc_iri)
        from mio.ltm import LTMDeserializer
        deser = LTMDeserializer(legacy=self._legacy, 
                                context=self._context, 
                                included_by=(included or set()))
        deser.handler = self.handler
        deser.subordinate = True
        deser.parse(Source(doc_iri))

    def merge(self, iri, syntax='ltm'):
        if syntax.lower() == 'ltm':
            self.merge_ltm(iri)
        else:
            doc_iri = self.resolve_iri(iri)
            if doc_iri in self._context.loaded:
                return
            self._context.add_loaded(doc_iri)
            deser = mio.create_deserializer(syntax)
            if not deser:
                raise mio.MIOException('Unsupported syntax: "%s"' % syntax)
            deser.subordinate = True
            deser.context = self._context
            deser.handler = self.handler
            deser.parse(Source(doc_iri))

    def register_slo_prefix(self, prefix, iri):
        """\
        Registeres a prefix for subject locators.
        """
        self._check_unique_prefix(prefix)
        self._slo_prefixes[prefix] = self.resolve_iri(iri)

    def register_sid_prefix(self, prefix, iri):
        """\
        Registeres a prefix for subject identifiers.
        """
        self._check_unique_prefix(prefix)
        self._sid_prefixes[prefix] = self.resolve_iri(iri)

    def _check_unique_prefix(self, prefix):
        """\
        Checks if the specified `prefix` is not registered already (either as
        sid or as slo prefix).
        """
        if prefix in self._slo_prefixes:
            raise mio.MIOException('The prefix "%s" is already used as subject locator prefix' % prefix)
        if prefix in self._sid_prefixes:
            raise mio.MIOException('The prefix "%s" is already used as subject identifier prefix' % prefix)

    def set_baseuri(self, baseuri):
        """\
        Sets the base URI.
        """
        if self._seen_base:
            raise mio.MIOException('Only one #BASEURI directive is allowed')
        self._base_iri = baseuri
        self._seen_base = True

    def check_version(self, version):
        if version != u'1.3':
            raise mio.MIOException('Version "%s" is not supported.' % version)

    def create_topic_by_iid(self, ident):
        """\
        
        """
        frag = u'#%s' % ident
        ref = mio.ITEM_IDENTIFIER, resolve_iri(self._doc_iri, frag)
        if self._included_by:
            # Creating topic here to add the included by item identifiers
            handler = self.handler
            handler.startTopic(ref)
            for iri in self._included_by:
                handler.itemIdentifier(resolve_iri(iri, frag))
            handler.endTopic()
        return ref

    def resolve_iri(self, reference):
        """\
        
        """
        if reference[0] == u'#':
            return resolve_iri(self._doc_iri, reference)
        else:
            return resolve_iri(self._base_iri, reference)

    def create_topic_by_qname(self, prefix, local):
        """\

        """
        iri = self._sid_prefixes.get(prefix)
        if iri:
            kind = mio.SUBJECT_IDENTIFIER
        else:
            iri = self._slo_prefixes.get(prefix)
            kind = mio.SUBJECT_LOCATOR
        if not iri:
            raise mio.MIOException('The prefix "%s" is not bound' % prefix)
        return kind, resolve_iri(iri, local)

    def tm_reifier(self, reifier_id):
        if self._legacy or not self._is_subordinate:
            self.reifier(reifier_id)
        else:
            reifier = mio.ITEM_IDENTIFIER, self.resolve_iri('#' + reifier_id)
            self.handler.startTopic(reifier)
            self.handler.endTopic()

    def tm_iid(self, iid):
        if not self._is_subordinate:
            self.handler.itemIdentifier(self.resolve_iri('#' + iid))

    def reifier(self, reifier_id):
        if not reifier_id:
            return
        reifier = mio.ITEM_IDENTIFIER, self.resolve_iri('#' + reifier_id)
        if not self._legacy:
            self.handler.reifier(reifier)
        else:
            handler = self.handler
            iri = resolve_iri(self._base_iri, u'#--reified--' + reifier_id)
            handler.itemIdentifier(iri)
            handler.startReifier()
            handler.startTopic(reifier)
            handler.subjectIdentifier(iri)
            handler.endTopic()
            handler.endReifier()
