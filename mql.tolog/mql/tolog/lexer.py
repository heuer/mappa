# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
tolog lexer.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD License
"""
import sys
import re
from tm.ply import TOKEN
from tm.mql import SyntaxQueryError

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

_DIRECTIVES = {
    # tolog extensions
    '%prefix': 'DIR_PREFIX',
    '%base': 'DIR_BASE',
    '%import': 'DIR_IMPORT',
    '%version': 'DIR_VERSION',
}

_RESERVED = {
    'select': 'KW_SELECT',
    'from': 'KW_FROM',
    'count': 'KW_COUNT',
    'not': 'KW_NOT',
    'limit': 'KW_LIMIT',
    'offset': 'KW_OFFSET',
    'order': 'KW_ORDER',
    'by': 'KW_BY',
    'asc': 'KW_ASC',
    'desc': 'KW_DESC',
    'import': 'KW_IMPORT',
    'as': 'KW_AS',
    'using': 'KW_USING',
    'for': 'KW_FOR',
    # tolog 1.2
    'delete': 'KW_DELETE',
    'merge': 'KW_MERGE',
    'update': 'KW_UPDATE',
    'insert': 'KW_INSERT',
    # t+
    'load': 'KW_LOAD',
    'create': 'KW_CREATE',
    'drop': 'KW_DROP',
    'into': 'KW_INTO',
    'where': 'KW_WHERE',
    }

# Creating a set here to get rid of the warning that KW_WHERE is defined twice
tokens = tuple(set(_RESERVED.values())) + tuple(_DIRECTIVES.values()) + (
    'IDENT',
    'SID',
    'SLO',
    'IID',
    'OID',
    'VARIABLE',
    'PARAM',
    'QNAME',
    'CURIE',

    # Operators
    # = /= >= > <= <
    'EQ', 'NE', 'GE', 'GT', 'LE', 'LT',

    # Literals
    'STRING', 'INTEGER', 
    # Non-standard tolog
    'DECIMAL', 'DATE', 'DATE_TIME', 'IRI',

    # Delimiters ( ) { } , : | || ? :- .
    'LPAREN', 'RPAREN', 'LCURLY', 'RCURLY',
    'COMMA', 'COLON', 'PIPE', 'PIPE_PIPE', 'QM',
    'IMPLIES', 'DOT',
    # Non-standard tolog
    'CIRCUMFLEX',
    'DOUBLE_CIRCUMFLEX',
    
    # Keeping (unparsed) topic map content. Not really a token, though
    'TM_FRAGMENT',
    
    # Non-standard directives 
    'X_DIRECTIVE',
)

t_ignore = ' \t'

t_EQ = ur'='
t_NE = ur'/='
t_LE = ur'<='
t_LT = ur'<'
t_GE = ur'>='
t_GT = ur'>'


t_LPAREN = ur'\('
t_RPAREN = ur'\)'
t_LCURLY = ur'\{'
t_RCURLY = ur'\}'
t_COMMA = ur','
t_DOT = ur'\.'
t_CIRCUMFLEX = ur'\^'
t_DOUBLE_CIRCUMFLEX = ur'\^\^'
t_IMPLIES = ur':-'
t_COLON = ur':'
t_PIPE_PIPE = ur'\|{2}'
t_PIPE = ur'\|'

states = (
   ('tm', 'exclusive'),
)


#pylint: disable-msg=W0613, W0622

def t_error(t):
    raise SyntaxQueryError('Invalid tolog syntax: %r' % t) #TODO

t_tm_error = t_error # Same error handling within state 'tm'

def t_mlcomment(t):
    ur'/\*[^\*/]*\*/'
    t.lexer.lineno += t.value.count('\n')


def t_comment(t):
    ur'\#[^\r\n]*'


def t_newline(t):
    ur'[\r\n]'
    t.lexer.lineno += 1


def t_QM(t):
    ur'\?'
    # Everything after the ? is ignored
    t.lexer.lexpos = t.lexer.lexlen  # Lexer assumes that it has reached the end
    return t


def t_STRING(t):
    ur'"([^"]|"{2})*"'
    t.value = t.value[1:-1].replace('""', '"')
    return t


def t_IRI(t):
    ur'<[^<>\"\{\}\`\\ ]+>'
    t.value = t.value[1:-1]
    return t

@TOKEN(r'\$' + _IDENT)
def t_VARIABLE(t):
    t.value = t.value[1:]
    return t

@TOKEN(r'%' + _IDENT + r'%')
def t_PARAM(t):
    t.value = t.value[1:-1]
    return t

@TOKEN(r'@([0-9]+|[0-9]*' + _IDENT + ')')
def t_OID(t):
    t.value = t.value[1:]
    return t


def t_SID(t):
    r'i"[^"]+"'
    t.value = t.value[2:-1]
    return t


def t_SLO(t):
    r'a"[^"]+"'
    t.value = t.value[2:-1]
    return t


def t_IID(t):
    r's"[^"]+"'
    t.value = t.value[2:-1]
    return t

@TOKEN(r'\[%s:[^<>\"\{\}\`\\\] ]+\]' % _IDENT)
def t_CURIE(t):
    t.value = t.value[1:-1]
    return t

@TOKEN(ur'%s:(([0-9]+(%s)*)|%s)' % (_IDENT, _IDENT_PART, _IDENT))
def t_QNAME(t):
    return t

@TOKEN(_IDENT)
def t_IDENT(t):
    t.type = _RESERVED.get(t.value.lower(), u'IDENT')
    if t.type == u'KW_INSERT':
        t.lexer.begin('tm') # Switch to TM mode
    elif t.type == u'KW_FROM' and not t.lexer.tolog_plus:
        t.type = u'KW_WHERE'
    return t


def t_directive(t):
    ur'%[A-Z\-a-z]+'
    t.type = _DIRECTIVES.get(t.value.lower())
    if not t.type:
        if t.value[:3] == u'%x-':
            t.value = t.value[3:]
            t.type = 'X_DIRECTIVE'
        else:
            raise SyntaxQueryError('Unknown directive %s' % t.value)
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

# Satisfy PLY and ignore nothing
t_tm_ignore = ''

# We allow something like INSERT from . from . from tolog-predicate
# for the time being although the tolog spec. says that it is an error since
# 'from' is a tolog keyword.
#TODO: Needs more work/tests
_INTO_KEYWORD = re.compile(ur'\s+(?=into\s+)', re.IGNORECASE).finditer
_WHERE_KEYWORD = re.compile(ur'\s+(?=(from|where)\s+(?!(.*?("(.*?(\.|;))|\.|(?:#\))))))', re.IGNORECASE).finditer

# Matches first whitespace characters after INSERT
# Then search for the tolog keyword 'into' or 'from'/'where' or to the
# end of the string. The content between INSERT and from (exclusive) / end of 
# string is returned as TM_FRAGMENT token
def t_tm_content(t):
    ur'\s+'
    def last_match(match_iterator):
        m = None
        for m in match_iterator(t.lexer.lexdata, t.lexer.lexpos):
            pass
        return m
    m = last_match(_INTO_KEYWORD) or last_match(_WHERE_KEYWORD)
    if m:
        start, end = m.start(), m.end()
    else:
        start = t.lexer.lexlen
        end = start
    t.value = t.lexer.lexdata[t.lexer.lexpos:start]
    t.type = 'TM_FRAGMENT'
    t.lexer.lineno += t.value.count('\n')
    # Move the lexer's position to the end of the TM fragment 
    # but in advance of the optional keyword
    t.lexer.lexpos = end
    # Continue with tolog
    t.lexer.begin('INITIAL')
    return t
