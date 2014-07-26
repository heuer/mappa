# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\


:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD License
"""
from mappa.predicates import cid

def scoped_signature(scoped):
    return tuple(sorted(map(cid, scoped.scope)))

def association_signature(assoc):
    return (assoc.type.id, tuple(sorted([role_signature(r) for r in assoc.roles])), scoped_signature(assoc))

def role_signature(role):
    return role.type.id, role.player.id

def occurrence_signature(occ):
    return (occ.type.id, occ.value, occ.datatype, scoped_signature(occ))

def name_signature(name):
    return (name.type.id, name.value, scoped_signature(name))

def variant_signature(variant):
    return (variant.value, variant.datatype, scoped_signature(variant))

