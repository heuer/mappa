# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
Internal utility functions.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD License
"""
from mql.tolog import consts

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
