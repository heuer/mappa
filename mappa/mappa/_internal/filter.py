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
Supports filters for Topic Maps construct properties.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD License
"""
from itertools import ifilter
from functools import partial
from mappa import ANY
from mappa.utils import has_type, has_scope
from mappa.predicates import parent

# pylint: disable-msg=W0622

def filter_by_type_scope(type, scope, exact, coll):
    """\
    Filters the collection by the specified `type` and `scope`.
    
    `type`
        The type to filter, may be ``ANY``
    `scope`
        The scope to filter, may be ``ANY``
    `exact`
        Indicates if the scope should be exactly matched.
    `coll`
        The collection to filter.
    """
    pred_type, pred_scope = bool, bool
    if type is not ANY:
        pred_type = partial(has_type, type=type)
    if scope is not ANY:
        pred_scope = partial(has_scope, scope=scope, exact=exact)
    return ifilter(lambda e: pred_type(e) and pred_scope(e), coll)

def filter_roles(type, assoc_type, scope, exact, roles):
    """\
    Filters the roles by their `type` and optionally by the parent `assoc_type`
    and the parent's `scope`
    
    `type`
        The type to filter, may be ``ANY``
    `assoc_type`
        The role parent's type.
    `scope`
        The scope to filter, may be ``ANY``
    `exact`
        Indicates if the scope should be exactly matched.
    `roles`
        The collection of roles to filter.
    """
    pred_assoc_type, pred_assoc_scope = bool, bool
    if assoc_type is not ANY:
        pred_assoc_type = partial(has_type, type=assoc_type)
    if scope is not ANY:
        pred_assoc_scope = partial(has_scope, scope=scope, exact=exact)
    pred_assoc = lambda a: pred_assoc_type(a) and pred_assoc_scope(a)
    return ifilter(lambda r: has_type(r, type) and pred_assoc(parent(r)), roles)
