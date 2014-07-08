# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
Constants.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD License
"""
from tm import mio

#
#-- Module IRIs
#
_TOLOG_BASE = u'http://psi.ontopia.net/tolog/'
TOLOG_STRING_MODULE_IRI = _TOLOG_BASE + u'string/'
TOLOG_EXPERIMENTAL_MODULE_IRI = _TOLOG_BASE + u'experimental/'
TOLOG_NUMBER_MODULE_IRI = _TOLOG_BASE + u'numbers/'

_TPLUS_BASE = u'http://psi.semagia.com/tplus/'
TPLUS_EXPERIMENTAL_MODULE_IRI = _TPLUS_BASE + u'experimental/'
TPLUS_EXPERIMENTAL_DATE_MODULE_IRI = TPLUS_EXPERIMENTAL_MODULE_IRI + 'date/'


#
#-- Constants for grammar constructs
#
IID = mio.ITEM_IDENTIFIER
SID = mio.SUBJECT_IDENTIFIER
SLO = mio.SUBJECT_LOCATOR

IRI = SID

IDENT = 100
OID = 101
QNAME = 102
CURIE = 103
PARAM = 104
VARIABLE = 105

DESC = 106
ASC  = 107

DATE = 108
DATE_TIME = 109
STRING = 110
INTEGER = 111
DECIMAL = 112
LITERAL = 113
MODULE = 114

COUNT = 1000

_CONST2NAME = {
    VARIABLE: 'variable',
    DECIMAL: 'decimal',
    INTEGER: 'integer',
    IDENT: 'identifier',
    PARAM: 'parameter',
    OID: 'objectid',
    QNAME: 'qname',
    CURIE: 'curie',
    MODULE: 'module',
    SID: 'iri',
    SLO: 'subjectlocator',
    IID: 'itemidentifier',
    DATE: 'date',
    DATE_TIME: 'datetime',
    STRING: 'string',
    LITERAL: 'literal',
    ASC: 'ascending',
    DESC: 'descending',
    COUNT: 'count'
}

def get_name(constant):
    return _CONST2NAME.get(constant)

        
