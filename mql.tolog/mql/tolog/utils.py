# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2012 -- Lars Heuer - Semagia <http://www.semagia.com/>.
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
Internal utility functions.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD License
"""
from mql.tolog import consts

_INFIX_PREDICATES = (u'/=', u'<', u'<=', u'=', u'>', u'>=')

_BUILTIN_PREDICATES = _INFIX_PREDICATES + (
    u'association', u'association-role', u'base-locator',
    u'datatype', u'direct-instance-of', u'instance-of', 
    u'item-identifier', u'object-id', u'occurrence',
    u'reifies', u'resource', u'role-player', u'scope',
    u'subject-identifier', u'subject-locator', u'topic',
    u'topic-name', u'topicmap', u'type', u'value', u'value-like',
    u'variant',
    # tolog 1.2
    u'coalesce', #'name',
    # deprecated
    u'source-locator', 
    )

_TOLOG_UPDATE_FUNCTIONS = (
    # tolog 1.2
    u'value', u'resource',
)

_TOLOG_DELETE_FUNCTIONS = (
    # tolog 1.2
    u'subject-identifier', u'subject-locator', u'item-identifier',
    u'scope', u'reifies', u'direct-instance-of',
)

_DEFAULT_MODULES = (
    consts.TOLOG_STRING_MODULE_IRI,
    consts.TOLOG_EXPERIMENTAL_MODULE_IRI,
    consts.TOLOG_NUMBER_MODULE_IRI,
    consts.TPLUS_EXPERIMENTAL_MODULE_IRI,
    consts.TPLUS_EXPERIMENTAL_DATE_MODULE_IRI,
)

def is_module_iri(iri):
    """\
    Returns if ``iri`` represents a default module.
    """
    return iri in _DEFAULT_MODULES

def is_infix_predicate(name):
    """\
    Retuns if ``name`` is an infix predicate.
    """
    return name in _INFIX_PREDICATES

def is_builtin_predicate(name):
    """\
    Returns if ``name`` is a built-in predicate name
    """
    return name in _BUILTIN_PREDICATES

def is_delete_function(name):
    """\
    Returns if ``name`` is a delete function.
    """
    return name in _TOLOG_DELETE_FUNCTIONS

def is_update_function(name):
    """\
    Returns if ``name`` is a update function.
    """
    return name in _TOLOG_UPDATE_FUNCTIONS
