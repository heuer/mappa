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
#     * Neither the name of the project nor the names of the contributors 
#       may be used to endorse or promote products derived from this 
#       software without specific prior written permission.
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
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD License
"""
from collections import defaultdict
from mappa.utils import is_association, is_role, is_occurrence, is_name, is_literal
from mappa.backend.event import *
from mappa import XSD, TMDM, Literal

class IndexManager(object):

    def __init__(self, dispatcher):
        self.type_instance = TypeInstanceIndex(dispatcher)
        self.scoped = ScopedIndex(dispatcher)
        self.literal = LiteralIndex(dispatcher)


class Index(object):
    pass

def as_literal(lit):
    if not is_literal(lit):
        return Literal(lit, XSD.string)
    return lit

class LiteralIndex(Index):
    
    def __init__(self, dispatcher):
        super(LiteralIndex, self).__init__()
        self._lit2occ = {}
        self._lit2name = {}
        self._lit2var = {}
        self.subscribe(dispatcher)

    def subscribe(self, dispatcher):
        dispatcher.subscribe(SetValue, self._set_value)
        dispatcher.subscribe(AddOccurrence, self._add_occ)
        dispatcher.subscribe(RemoveOccurrence, self._remove_occ)
        dispatcher.subscribe(AddName, self._add_name)
        dispatcher.subscribe(RemoveName, self._remove_name)
        dispatcher.subscribe(AddVariant, self._add_var)
        dispatcher.subscribe(RemoveVariant, self._remove_var)

    def _set_value(self, evt):
        source = evt.source
        if is_occurrence(source):
            dct = self._lit2occ
        elif is_name(source):
            dct = self._lit2name
        else:
            dct = self._lit2var
        _unregister_literal(dct, source, evt.old)
        _register_literal(dct, source, evt.new)

    def _add_occ(self, evt):
        _register_literal(self._lit2occ, evt.new, evt.new.literal)

    def _remove_occ(self, evt):
        _unregister_literal(self._lit2occ, evt.old, evt.old.literal)

    def _add_name(self, evt):
        _register_literal(self._lit2name, evt.new, evt.new.literal)

    def _remove_name(self, evt):
        _unregister_literal(self._lit2name, evt.old, evt.old.literal)

    def _add_var(self, evt):
        _register_literal(self._lit2var, evt.new, evt.new.literal)

    def _remove_var(self, evt):
        _unregister_literal(self._lit2var, evt.old, evt.old.literal)

    def occurrences(self, lit):
        return self._lit2occ.get(as_literal(lit)) or ()

    def names(self, lit):
        return self._lit2name.get(as_literal(lit)) or ()

    def variants(self, lit):
        return self._lit2var.get(as_literal(lit)) or ()


def _register_literal(dct, construct, literal):
    if literal not in dct:
        dct[literal] = []
    dct[literal].append(construct)

def _unregister_literal(dct, construct, literal):
    l = dct.get(literal)
    if l and construct in l:
        l.remove(construct)

class ScopedIndex(Index):

    def __init__(self, dispatcher):
        super(ScopedIndex, self).__init__()
        self._scope2assoc = {}
        self._scope2occ = {}
        self._scope2name = {}
        self._scope2var = {}
        self.subscribe(dispatcher)

    def subscribe(self, dispatcher):
        dispatcher.subscribe(AddAssociation, self._add_assoc)
        dispatcher.subscribe(RemoveAssociation, self._remove_assoc)
        dispatcher.subscribe(AddOccurrence, self._add_occ)
        dispatcher.subscribe(RemoveOccurrence, self._remove_occ)
        dispatcher.subscribe(AddName, self._add_name)
        dispatcher.subscribe(RemoveName, self._remove_name)
        dispatcher.subscribe(AddVariant, self._add_var)
        dispatcher.subscribe(RemoveVariant, self._remove_var)
        dispatcher.subscribe(SetScope, self._set_scope)

    def _set_scope(self, evt):
        src = evt.source
        old_scope = evt.old
        new_scope = evt.new
        if is_association(src):
            dct = self._scope2assoc
        elif is_occurrence(src):
            dct = self._scope2occ
        elif is_name(src):
            dct = self._scope2name
        else:
            dct = self._scope2var
        _unregister_scope(dct, src, old_scope)
        _register_scope(dct, src, new_scope)

    def _add_assoc(self, evt):
        _register_scope(self._scope2assoc, evt.new, evt.new.scope)

    def _remove_assoc(self, evt):
        _unregister_scope(self._scope2assoc, evt.old, evt.old.scope)

    def _add_occ(self, evt):
        _register_scope(self._scope2occ, evt.new, evt.new.scope)

    def _remove_occ(self, evt):
        _unregister_scope(self._scope2occ, evt.old, evt.old.scope)

    def _add_name(self, evt):
        _register_scope(self._scope2name, evt.new, evt.new.scope)

    def _remove_name(self, evt):
        _unregister_scope(self._scope2name, evt.old, evt.old.scope)

    def _add_var(self, evt):
        _register_scope(self._scope2var, evt.new, evt.new.scope)

    def _remove_var(self, evt):
        _unregister_scope(self._scope2var, evt.old, evt.old.scope)

    def associations(self, scope, exact=True):
        return _filter(self._scope2assoc, scope, exact)

    def associations_by_theme(self, theme):
        return self._scope2assoc.get(theme, ())

    def association_themes(self):
        return self._scope2assoc.keys()

    def occurrences(self, scope, exact=True):
        return _filter(self._scope2occ, scope, exact)

    def occurrences_by_theme(self, theme):
        return self._scope2occ.get(theme, ())

    def occurrence_themes(self):
        return self._scope2occ.keys()

    def names(self, scope, exact=True):
        return _filter(self._scope2name, scope, exact)

    def names_by_theme(self, theme):
        return self._scope2name.get(theme, ())

    def name_themes(self):
        return self._scope2name.keys()

    def variants(self, scope, exact=True):
        return _filter(self._scope2var, scope, exact)

    def variants_by_theme(self, theme):
        return self._scope2var.get(theme, ())

    def variant_themes(self):
        return self._scope2var.keys()

def _register_scope(dct, scoped, scope):
    for theme in scope:
        if theme not in dct:
            dct[theme] = []
        dct[theme].append(scoped)
 
def _unregister_scope(dct, scoped, scope):
    for theme in scope:
        l = dct.get(theme)
        if l and scoped in l:
            l.remove(scoped)

def _filter(dct, scope, exact):
    raise NotImplementedError()

class TypeInstanceIndex(Index):

    def __init__(self, dispatcher):
        super(TypeInstanceIndex, self).__init__()
        self._type2topic = defaultdict(list)
        self._type2assoc = defaultdict(list)
        self._type2role = defaultdict(list)
        self._type2occ = defaultdict(list)
        self._type2name = defaultdict(list)
        self.subscribe(dispatcher)

    def subscribe(self, dispatcher):
        dispatcher.subscribe(SetType, self._set_type)
        dispatcher.subscribe(AddAssociation, self._add_assoc)
        dispatcher.subscribe(RemoveAssociation, self._remove_assoc)
        dispatcher.subscribe(AddRole, self._add_role)
        dispatcher.subscribe(RemoveRole, self._remove_role)
        dispatcher.subscribe(AddOccurrence, self._add_occ)
        dispatcher.subscribe(RemoveOccurrence, self._remove_occ)
        dispatcher.subscribe(AddName, self._add_name)
        dispatcher.subscribe(RemoveName, self._remove_name)
 
    def _set_type(self, evt):
        src = evt.source
        if is_association(src):
            dct = self._type2assoc
        elif is_role(src):
            dct = self._type2role
        elif is_occurrence(src):
            dct = self._type2occ
        elif is_name(src):
            dct = self._type2name
        else:
            raise TypeError
        _unregister_type(dct, src, evt.old)
        _register_type(dct, src, evt.new)

    def _add_assoc(self, evt):
        _register_type(self._type2assoc, evt.new, evt.new.type)

    def _remove_assoc(self, evt):
        _unregister_type(self._type2assoc, evt.old, evt.old.type)
 
    def _add_role(self, evt):
        def find_type(assoc):
            for t, p in assoc.roles:
                if TMDM.type in t.sids:
                    return p
        role, type = evt.new, evt.new.type
        _register_type(self._type2role, role, type)
        #TODO: Use a dedicated add_type-event. Assert that assoc.type is tmdm:type_instance
        #FIXME: Who says that the tmdm:type role is already available?
        if TMDM.instance in type.sids:
            _register_type(self._type2topic, role.player, find_type(evt.source))

    def _remove_role(self, evt):
        def find_type(assoc):
            for t, p in assoc.roles:
                if TMDM.type in t.sids:
                    return p
        role, type = evt.old, evt.old.type
        _unregister_type(self._type2role, role, type)
        #TODO: Use a dedicated remove_type-event. Assert that assoc.type is tmdm:type_instance
        #FIXME: Who says that the tmdm:type role is still available?
        if TMDM.instance in type.sids:
            _unregister_type(self._type2topic, role.player, find_type(evt.source))

    def _add_occ(self, evt):
        _register_type(self._type2occ, evt.new, evt.new.type)

    def _remove_occ(self, evt):
        _unregister_type(self._type2occ, evt.old, evt.old.type)

    def _add_name(self, evt):
        _register_type(self._type2name, evt.new, evt.new.type)

    def _remove_name(self, evt):
        _unregister_type(self._type2name, evt.old, evt.old.type)

    def topics(self, type):
        return self._type2topic[type]

    def topic_types(self):
        return self._type2topic.iterkeys()

    def associations(self, type):
        return self._type2assoc[type]

    def association_types(self):
        return self._type2assoc.iterkeys()

    def roles(self, type):
        return self._type2role[type]

    def role_types(self):
        return self._type2role.iterkeys()

    def occurrences(self, type):
        return self._type2occ[type]

    def occurrence_types(self):
        return self._type2occ.iterkeys()

    def names(self, type):
        return self._type2name[type]

    def name_types(self):
        return self._type2name.iterkeys()

def _register_type(dct, typed, type):
    dct[type].append(typed)

def _unregister_type(dct, typed, type):
    if typed in dct:
        dct[type].remove(typed)
