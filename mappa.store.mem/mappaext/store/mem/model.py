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
Memory backend.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD License
"""
import cPickle as pickle
from mappa import UCS
from mappa._internal.utils import random_id
from mappa.backend.stub import *
from mappa.utils import is_topic
from mappa.backend.identityman import IdentityManager
from .index import IndexManager

#pylint: disable-msg=W0622

class Connection(object):

    def __init__(self, file=None, persistent=False, **kw):
        self._iri2tm = {}
        self._persistent = persistent
        self._file = file
        self.closed = False

    def create(self, iri):
        if self._iri2tm.get(iri):
            raise ValueError('A topic map with the specified IRI "%s" exists' % iri)
        tm = TopicMap(locator=iri)
        self._iri2tm[iri] = tm
        return tm

    def remove(self, iri):
        del self._iri2tm[iri]

    def get(self, iri):
        return self._iri2tm.get(iri)

    def __contains__(self, iri):
        return iri in self._iri2tm

    def commit(self):
        if self._persistent:
            out = open(self._file, 'wb')
            pickle.dump(self, out)
            out.close()

    def abort(self):
        pass

    def close(self, commit=False):
        self.closed = True
        if commit:
            self.commit()
        self._iri2tm = None

    iris = property(lambda self: self._iri2tm.keys())


class TopicMapsConstructBuilder(object):
    
    def __init__(self, tm):
        self.tm = tm

    def create_topic(self):
        return Topic(self.tm)

    def create_association(self, type, scope=()):
        return Association(self.tm, type, scope)

    def create_role(self, type, player):
        return Role(self.tm, type, player)

    def create_occurrence(self, type, value, scope=()):
        return Occurrence(self.tm, type, value, scope)

    def create_name(self, type, value, scope=()):
        return Name(self.tm, type, value, scope)

    def create_variant(self, value, scope):
        return Variant(self.tm, value, scope)


class TMCMixin(object):
    
    def __init__(self):
        self.id = random_id()

    def _create_iids(self): 
        return set()


class ScopedMixin(TMCMixin):

    def __init__(self):
        TMCMixin.__init__(self)

    def _create_scope(self, scope):
        if not scope:
            return UCS
        return frozenset(scope)

class TopicMap(TopicMapStub, TMCMixin):

    def __init__(self, locator):
        TMCMixin.__init__(self)
        TopicMapStub.__init__(self, locator)
        self._idman = IdentityManager(self)
        self.builder = TopicMapsConstructBuilder(self)
        self.index = IndexManager(self)

    def construct_by_iid(self, iid):
        return self._idman.construct_by_iid(iid)

    def construct_by_id(self, ident):
        if self.id == ident:
            return self
        return self._idman.construct_by_id(ident)

    def topic_by_iid(self, iid):
        tmc = self.construct_by_iid(iid)
        if is_topic(tmc):
            return tmc
        return None

    def topic_by_sid(self, sid):
        return self._idman.topic_by_sid(sid)

    def topic_by_slo(self, slo):
        return self._idman.topic_by_slo(slo)

    def remove(self):
        del self.__dict__

    def _create_topics(self): 
        return set()

    def _create_associations(self): 
        return set()


class Topic(TMCMixin, TopicStub):

    def __init__(self, tm):
        TMCMixin.__init__(self)
        TopicStub.__init__(self, tm)

    def _create_sids(self): 
        return set()

    def _create_slos(self): 
        return set()

    def _create_roles_played(self): 
        return set()

    def _create_occurrences(self): 
        return set()

    def _create_names(self): 
        return set()


class Association(AssociationStub, ScopedMixin):

    def __init__(self, tm, type, scope):
        ScopedMixin.__init__(self)
        AssociationStub.__init__(self, tm, type, scope)

    def _create_roles(self): 
        return set()


class Role(RoleStub, TMCMixin):

    def __init__(self, tm, type, player):
        TMCMixin.__init__(self)
        RoleStub.__init__(self, tm, type, player)


class Occurrence(OccurrenceStub, ScopedMixin):
    
    def __init__(self, tm, type, value, scope):
        ScopedMixin.__init__(self)
        OccurrenceStub.__init__(self, tm, type, value, scope)


class Name(NameStub, ScopedMixin):

    def __init__(self, tm, type, value, scope):
        ScopedMixin.__init__(self)
        NameStub.__init__(self, tm, type, value, scope)

    def _create_variants(self): 
        return set()


class Variant(VariantStub, ScopedMixin):

    def __init__(self, tm, value, scope):
        ScopedMixin.__init__(self)
        VariantStub.__init__(self, tm, value, scope)


from mappa._internal.enhancer import enhance_connection
enhance_connection(Connection)
