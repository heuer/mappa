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
from rdflib import store as rdflibstore, graph as rdflibgraph
from rdflib.parser import create_input_source as rdflib_create_input_source
from mio.rdf import interfaces
from tm.proto import implements
from tm import mio, RDF2TM
from tm.voc import RDF2TM as NS_RDF2TM

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
        self.prefix_listener = None
        self._mappings = collections.defaultdict(_Mapping)

    def read(self, source):
        """\
        Implements ``IMappingReader.read()``.
        """
        def as_rdflib_source(src):
            if src.stream is not None:
                return rdflib_create_input_source(file=src.stream, publicID=src.iri)
            return rdflib_create_input_source(publicID=src.iri)
        graph = rdflibgraph.Graph(store=self)
        self.handler.start()
        graph.parse(as_rdflib_source(source))
        self._build_mapping()
        self.handler.end()
        self._mappings = None

    def _build_mapping(self):
        handler = self.handler
        for predicate in self._mappings:
            mapping = self._mappings[predicate]
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
        if self.prefix_listener:
            self.prefix_listener.handleNamespace(prefix, namespace)
        super(RDFMappingReader, self).bind(prefix, namespace)

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


class _Mapping(object):
    __slots__ = ['kind', 'type', 'scope', 'subj', 'obj']

    def __init__(self):
        self.kind = None
        self.type = None
        self.scope = []
        self.subj = None
        self.obj = None
