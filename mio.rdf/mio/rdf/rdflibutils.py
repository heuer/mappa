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
import collections
from rdflib.store import Store
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


class RDFMappingReader(Store):
    """\

    """
    def __init__(self, handler):
        """\

        `handler`
            A IMappingHandler instance.
        """
        super(RDFMappingReader, self).__init__(configuration=None, identifier=None)
        self.handler = handler
        self._mappings = collections.defaultdict(_Mapping)

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
                raise mio.MIOException('Unknown object of a rtm:maps-to statement. Object: "%r"' % obj)
        elif RDF2TM.type == predicate:
            self._mappings[subject].type = obj
        elif RDF2TM.in_scope == predicate:
            self._mappings[subject].scope.append(obj)
        elif RDF2TM.subject_role == predicate:
            self._mappings[subject].subject = obj
        elif RDF2TM.object_role == predicate:
            self._mappings[subject].object = obj
        else:
            raise mio.MIOException('Unknown predicate: <%s>' % predicate)


class _Mapping(object):
    __slots__ = ['kind', 'type', 'scope', 'subject', 'object']
