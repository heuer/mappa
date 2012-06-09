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

_TOLOG_BASE = u'http://psi.ontopia.net/tolog/'
_TOLOG_STRING_MODULE = _TOLOG_BASE + u'string/'
_TOLOG_EXPERIMENTAL_MODULE = _TOLOG_BASE + u'experimental/'
_TOLOG_NUMBER_MODULE = _TOLOG_BASE + u'numbers/'

_TPLUS_BASE = u'http://psi.semagia.com/tplus/'
_TPLUS_EXPERIMENTAL_MODULE = _TPLUS_BASE + u'experimental/'
_TPLUS_EXPERIMENTAL_DATE_MODULE = _TOLOG_EXPERIMENTAL_MODULE + 'date/'

_INFIX_PREDICATES = ('/=', '<', '<=', '=', '>', '>=')

_BUILTIN_PREDICATES = _INFIX_PREDICATES + (
    'association', 'association-role', 'base-locator',
    'datatype', 'direct-instance-of', 'instance-of', 
    'item-identifier', 'object-id', 'occurrence',
    'reifies', 'resource', 'role-player', 'scope',
    'subject-identifier', 'subject-locator', 'topic',
    'topic-name', 'topicmap', 'type', 'value', 'value-like',
    'variant',
    # tolog 1.2
    'coalesce', #'name',
    # deprecated
    'source-locator', 
    )

_TOLOG_UPDATE_FUNCTIONS = (
    # tolog 1.2
    'value', 'resource',
)

_TOLOG_DELETE_FUNCTIONS = (
    # tolog 1.2
    'subject-identifier', 'subject-locator', 'item-identifier',
    'scope', 'reifies', 'direct-instance-of',
)

_DEFAULT_MODULES = (
    _TOLOG_STRING_MODULE,
    _TOLOG_EXPERIMENTAL_MODULE,
    _TOLOG_NUMBER_MODULE,
    _TPLUS_EXPERIMENTAL_MODULE,
    _TPLUS_EXPERIMENTAL_DATE_MODULE,
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
