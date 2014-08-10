# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
Compact Topic Maps (CTM) lexer.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
import sys
from tm.ply import TOKEN
from tm.mio import MIOException

_DIRECTIVES = {
    '%prefix': 'DIR_PREFIX',
    '%encoding': 'DIR_ENCODING',
    '%version': 'DIR_VERSION',
    '%mergemap': 'DIR_MERGEMAP',
    '%include': 'DIR_INCLUDE',
    }

_KEYWORDS = {
    'isa': 'KW_ISA',
    'ako': 'KW_AKO',
    'def': 'KW_DEF',
    'end': 'KW_END',
    }

tokens = tuple(_DIRECTIVES.values()) + tuple(_KEYWORDS.values()) + (
    #Identifiers
    'WILDCARD', 'NAMED_WILDCARD', 'QNAME', 'IDENT', 'VARIABLE',
    # Brackets
    'LPAREN', 'RPAREN', 'LBRACK', 'RBRACK',
    # Delimiters
    'COMMA', 'SEMI', 'COLON', 'DOT', 'DOUBLE_CIRCUMFLEX', 'EQ', 'CIRCUMFLEX',
    'TILDE', 'HYPHEN', 'AT', 'STAR',
    # Datatypes 
    'STRING', 'IRI', 'INTEGER', 'DECIMAL', 'DATE', 'DATE_TIME'
    )

# Start of an identifier
_IDENT_START = ur'[a-zA-Z_]' \
               ur'|[\u00C0-\u00D6]|[\u00D8-\u00F6]' \
               ur'|[\u00F8-\u02FF]|[\u0370-\u037D]' \
               ur'|[\u037F-\u1FFF]|[\u200C-\u200D]' \
               ur'|[\u2070-\u218F]|[\u2C00-\u2FEF]' \
               ur'|[\u3001-\uD7FF]|[\uF900-\uFDCF]' \
               ur'|[\uFDF0-\uFFFD]'

if not sys.maxunicode == 0xffff:
    # <http://bugs.python.org/issue12729>, <http://bugs.python.org/issue12749>,
    # <http://bugs.python.org/issue3665>
    _IDENT_START += ur'|[\U00010000-\U000EFFFF]'
del sys

_IDENT_PART = ur'%s|[\-0-9]|[\u00B7]|[\u0300-\u036F]|[\u203F-\u2040]' % _IDENT_START

# Identifier
_IDENT = ur'(%s)+(\.*(%s))*' % (_IDENT_START, _IDENT_PART)

_DATE = ur'\-?(000[1-9]|00[1-9][0-9]|0[1-9][0-9][0-9]|[1-9][0-9][0-9][0-9]+)\-(0[1-9]|1[0-2])\-(0[1-9]|1[0-9]|2[0-9]|3[0-1])'
# Timezone
_TZ = ur'Z|((\+|\-)[0-9]{2}:[0-9]{2})'
# Time
_TIME = ur'[0-9]{2}:[0-9]{2}:[0-9]{2}(\.[0-9]+)?(%s)?' % _TZ

VARIABLE = ur'(\$%s)' % _IDENT

t_WILDCARD = ur'\?'
t_LPAREN = ur'\('
t_RPAREN = ur'\)'
t_LBRACK = ur'\['
t_RBRACK = ur'\]'
t_COMMA = ur','
t_SEMI = ur';'
t_COLON = ur':'
t_DOT = ur'\.'
t_DOUBLE_CIRCUMFLEX = ur'\^\^'
t_EQ = ur'='
t_CIRCUMFLEX = ur'\^'
t_TILDE = ur'~'
t_HYPHEN = ur'-'
t_AT = ur'@'
t_STAR = ur'\*'


states = (
  ('mlcomment', 'exclusive'),
)


def t_error(t):
    raise MIOException('Unexpected token "%r"' % t)


def t_mlcomment(t):
    ur'\#\('
    t.lexer.comment_level = 1
    t.lexer.begin('mlcomment')


def t_mlcomment_content(t):
    ur'[^#\(\)]+'
    t.lexer.lineno += t.value.count('\n')


def t_mlcomment_start(t):
    ur'\#\('
    t.lexer.comment_level += 1


def t_mlcomment_end(t):
    ur'\)\#'
    t.lexer.comment_level -= 1
    if t.lexer.comment_level == 0:
        t.lexer.begin('INITIAL')


def t_mlcomment_content2(t):
    ur'\#|\(|\)'

def t_mlcomment_error(t):
    raise MIOException('Unexpected token "%r"' % t)


def t_comment(t):
    ur'\#[^\r\n]*'


def t_ws(t):
    ur'\s+'
    t.lexer.lineno += t.value.count('\n')


def t_IRI(t):
    ur'[a-zA-Z]+[a-zA-Z0-9\+\-\.]*://([;\.\)]*[^\s;\]\.\(\)]+)+'
    return t


def t_iri2(t):
    u'<[^<>\"\{\}\`\\ ]+>'
    t.value = t.value[1:-1]
    t.type = 'IRI'
    return t


def t_directive(t):
    ur'%[a-z]+'
    directive = _DIRECTIVES.get(t.value)
    if not directive:
        raise MIOException('Unknown directive %s' % t.value)
    t.type = directive
    return t 

@TOKEN(ur'%s:(([0-9]+(%s)*)|%s)' % (_IDENT, _IDENT_PART, _IDENT))
def t_QNAME(t):
    t.value = tuple(t.value.split(':'))
    return t

@TOKEN(_IDENT)
def t_IDENT(t):
    t.type = _KEYWORDS.get(t.value, 'IDENT')
    return t

@TOKEN(VARIABLE)
def t_VARIABLE(t):
    t.value = t.value[1:]
    return t

@TOKEN(ur'\?%s' % _IDENT)
def t_NAMED_WILDCARD(t):
    t.value = t.value[1:]
    return t

@TOKEN(ur'%sT%s' % (_DATE, _TIME))
def t_DATE_TIME(t):
    return t

@TOKEN(_DATE)
def t_DATE(t):
    return t


def t_DECIMAL(t):
    ur'(\-|\+)?([0-9]+\.[0-9]+|\.([0-9])+)'
    return t


def t_INTEGER(t):
    ur'(\-|\+)?[0-9]+'
    return t


def t_triple_string(t):
    ur'"{3}([^"\\]|(\\[\\"rntuU])|"|"")*"{3}'
    t.value = t.value[3:-3]
    t.type = 'STRING'
    t.lexer.lineno += t.value.count('\n')
    return t


def t_STRING(t):
    ur'"([^"\\]|(\\[\\"rntuU]))*"'
    t.value = t.value[1:-1]
    t.lexer.lineno += t.value.count('\n')
    return t
