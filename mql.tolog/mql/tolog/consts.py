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
TPLUS_EXPERIMENTAL_DATE_MODULE_IRI = TPLUS_EXPERIMENTAL_MODULE_IRI + u'date/'


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
    VARIABLE: u'variable',
    DECIMAL: u'decimal',
    INTEGER: u'integer',
    IDENT: u'identifier',
    PARAM: u'parameter',
    OID: u'objectid',
    QNAME: u'qname',
    CURIE: u'curie',
    MODULE: u'module',
    SID: u'iri',
    SLO: u'subjectlocator',
    IID: u'itemidentifier',
    DATE: u'date',
    DATE_TIME: u'datetime',
    STRING: u'string',
    LITERAL: u'literal',
    ASC: u'ascending',
    DESC: u'descending',
    COUNT: u'count'
}

def get_name(constant):
    return _CONST2NAME.get(constant)

        
