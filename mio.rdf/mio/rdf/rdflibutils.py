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
from __future__ import absolute_import
import collections
from rdflib import BNode, Literal
from rdflib import store as rdflibstore, graph as rdflibgraph
from rdflib.parser import create_input_source as rdflib_create_input_source
from tm.proto import implements
from tm import mio, RDF2TM
from tm.voc import RDF2TM as NS_RDF2TM
from . import interfaces

_ASSOC = 1
_OCC = 2
_NAME = 3
_ISA = 4

_OBJ2KIND = {
    RDF2TM.association: _ASSOC,
    RDF2TM.occurrence: _OCC,
    RDF2TM.basename: _NAME,
    RDF2TM.instance_of: _ISA,
}


class RDFMappingReader(rdflibstore.Store):
    """\
    Mapping reader which reads a mapping from a RDF source.
    """
    implements(interfaces.IMappingReader)

    def __init__(self, handler=None):
        super(RDFMappingReader, self).__init__(configuration=None, identifier=None)
        self.handler = handler
        self._mappings = collections.defaultdict(_Mapping)

    def read(self, source):
        """\
        Implements ``IMappingReader.read()``.
        """
        graph = rdflibgraph.Graph(store=self)
        self.handler.start()
        graph.parse(as_rdflib_source(source))
        self._build_mapping()
        self.handler.end()
        self._mappings = None

    def _build_mapping(self):
        handler = self.handler
        for predicate, mapping in self._mappings.iteritems():
            if mapping.kind is _NAME:
                handler.handleName(predicate, scope=mapping.scope,
                                   type=mapping.type)
            elif mapping.kind is _OCC:
                handler.handleOccurrence(predicate, scope=mapping.scope,
                                         type=mapping.type)
            elif mapping.kind is _ISA:
                handler.handleInstanceOf(predicate, scope=mapping.scope)
            elif mapping.kind is _ASSOC:
                handler.handleAssociation(predicate, mapping.subj, mapping.obj,
                                          scope=mapping.scope, type=mapping.type)
            else:
                raise mio.MIOException(u'Invalid mapping for <%s>' % predicate)

    #
    # RDFLib Store implementations
    #
    def bind(self, prefix, namespace):
        super(RDFMappingReader, self).bind(prefix, namespace)
        self.handler.handlePrefix(prefix, namespace)

    def add(self, (subject, predicate, obj), context, quoted=False):
        if not predicate.startswith(NS_RDF2TM):
            return
        if RDF2TM.maps_to == predicate:
            if obj in _OBJ2KIND:
                self._mappings[subject].kind = _OBJ2KIND[obj]
            elif RDF2TM.subject_identifier == obj:
                self.handler.handleSubjectIdentifier(subject)
            elif RDF2TM.subject_locator == obj:
                self.handler.handleSubjectLocator(subject)
            elif RDF2TM.source_locator == obj:
                self.handler.handleItemIdentifier(subject)
            else:
                raise mio.MIOException(u'Unknown object of a rtm:maps-to statement. Object: "%r"' % obj)
        elif RDF2TM.type == predicate:
            self._mappings[subject].type = obj
        elif RDF2TM.in_scope == predicate:
            self._mappings[subject].scope.append(obj)
        elif RDF2TM.subject_role == predicate:
            self._mappings[subject].subj = obj
        elif RDF2TM.object_role == predicate:
            self._mappings[subject].obj = obj
        else:
            raise mio.MIOException(u'Unknown predicate: <%s>' % predicate)


class RDFSourceReader(rdflibstore.Store):
    """\
    RDF reader which translates RDF into MIO events.
    """
    def __init__(self, handler, error_handler, default_mapper=None):
        super(RDFSourceReader, self).__init__(configuration=None, identifier=None)
        self.handler = handler
        self.error_handler = error_handler
        self.default_mapper = default_mapper
        self._mappings = {}

    def resolve_uri(self, uri, is_bnode=None):
        if is_bnode is None:
            is_bnode = isinstance(uri, BNode)
        if is_bnode:
            return (mio.ITEM_IDENTIFIER, 'xxxx')
        return (mio.SUBJECT_IDENTIFIER, 'xxxx')

    #
    # RDFLib Store implementations
    #
    def add(self, (subject, predicate, obj), context, quoted=False):
        mapper = self._mappings.get(predicate, self.default_mapper)
        if not mapper:
            return
        handler = self.handler
        subj = (mio.SUBJECT_IDENTIFIER, 'xxx')
        if isinstance(subject, BNode):
            pass #TODO
        handler.startTopic(subj)
        if isinstance(obj, Literal):
            mapper.handle_literal(handler, self.error_handler, subj,
                                  predicate, obj.value, obj.datatype,
                                  obj.language)
        else:
            is_bnode = isinstance(obj, BNode)
            handler.handle_uri(handler, self.error_handler, subj, predicate,
                               self.resolve_uri(obj, is_bnode), is_bnode)
        handler.endTopic()


class _Mapping(object):
    __slots__ = ['kind', 'type', 'scope', 'subj', 'obj']

    def __init__(self):
        self.kind = None
        self.type = None
        self.scope = []
        self.subj = None
        self.obj = None


def as_rdflib_source(src):
    if src.stream is not None:
        return rdflib_create_input_source(file=src.stream, publicID=src.iri)
    return rdflib_create_input_source(publicID=src.iri)
