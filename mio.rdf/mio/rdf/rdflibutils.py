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
        super(RDFLibHandler, self).__init__(configuration=None, identifier=None)
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
