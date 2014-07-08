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
import re
from tm.ply import TOKEN
from tm.mql import SyntaxQueryError

# Start of an identifier
_IDENT_START = ur'[a-zA-Z_]|[\u00C0-\u00D6]|[\u00D8-\u00F6]' + \
                ur'|[\u00F8-\u02FF]|[\u0370-\u037D]' + \
                ur'|[\u037F-\u1FFF]|[\u200C-\u200D]' + \
                ur'|[\u2070-\u218F]|[\u2C00-\u2FEF]' + \
                ur'|[\u3001-\uD7FF]|[\uF900-\uFDCF]|[\uFDF0-\uFFFD]'

_IDENT_PART = ur'%s|[\-0-9]|[\u00B7]|[\u0300-\u036F]|[\u203F-\u2040]' % _IDENT_START

# Identifier
_IDENT = ur'(%s)+(\.*(%s))*' % (_IDENT_START, _IDENT_PART)

_DATE = r'\-?(000[1-9]|00[1-9][0-9]|0[1-9][0-9][0-9]|[1-9][0-9][0-9][0-9]+)\-(0[1-9]|1[0-2])\-(0[1-9]|1[0-9]|2[0-9]|3[0-1])'
# Timezone
_TZ = r'Z|((\+|\-)[0-9]{2}:[0-9]{2})'
# Time
_TIME = r'[0-9]{2}:[0-9]{2}:[0-9]{2}(\.[0-9]+)?(%s)?' % _TZ

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

t_EQ        = r'='
t_NE        = r'/='
t_LE        = r'<='
t_LT        = r'<'
t_GE        = r'>='
t_GT        = r'>'


t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_LCURLY    = r'\{'
t_RCURLY    = r'\}'
t_COMMA     = r','
t_DOT       = r'\.'
t_CIRCUMFLEX = r'\^'
t_DOUBLE_CIRCUMFLEX = r'\^\^'
t_IMPLIES   = r':-'
t_COLON     = r':'
t_PIPE_PIPE = r'\|{2}'
t_PIPE      = r'\|'

states = (
   ('tm', 'exclusive'),
)


#pylint: disable-msg=W0613, W0622

def t_error(t):
    raise SyntaxQueryError('Invalid tolog syntax: %r' % t) #TODO

t_tm_error = t_error # Same error handling within state 'tm'

def t_mlcomment(t):
    r'/\*[^\*/]*\*/'
    t.lexer.lineno += t.value.count('\n')

def t_comment(t):
    r'\#[^\r\n]*'

def t_newline(t):
    r'[\r\n]'
    t.lexer.lineno += 1

def t_QM(t):
    r'\?'
    # Everything after the ? is ignored
    t.lexer.lexpos = t.lexer.lexlen  # Lexer assumes that it has reached the end
    return t

def t_STRING(t):
    r'"([^"]|"{2})*"'
    t.value = t.value[1:-1].replace('""', '"')
    return t

def t_IRI(t):
    r'<[^<>\"\{\}\`\\ ]+>'
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

@TOKEN(r':'.join([_IDENT, r'[_\w\.-]+']))
def t_QNAME(t):
    return t

@TOKEN(_IDENT)
def t_IDENT(t):
    t.type = _RESERVED.get(t.value.lower(), 'IDENT')
    if t.type == 'KW_INSERT':
        t.lexer.begin('tm') # Switch to TM mode
    elif t.type == 'KW_FROM' and not t.lexer.tolog_plus:
        t.type = 'KW_WHERE'
    return t

def t_directive(t):
    r'%[A-Z\-a-z]+'
    t.type = _DIRECTIVES.get(t.value.lower())
    if not t.type:
        if t.value[:3] == u'%x-':
            t.value = t.value[3:]
            t.type = 'X_DIRECTIVE'
        else:
            raise SyntaxQueryError('Unknown directive %s' % t.value)
    return t

@TOKEN(r'%sT%s' % (_DATE, _TIME))
def t_DATE_TIME(t):
    return t

@TOKEN(_DATE)
def t_DATE(t):
    return t

def t_DECIMAL(t):
    r'(\-|\+)?([0-9]+\.[0-9]+|\.([0-9])+)'
    return t

def t_INTEGER(t):
    r'(\-|\+)?[0-9]+'
    return t

# Satisfy PLY and ignore nothing
t_tm_ignore = ''

# We allow something like INSERT from . from . from tolog-predicate
# for the time being although the tolog spec. says that it is an error since
# 'from' is a tolog keyword.
#TODO: Needs more work/tests
_INTO_KEYWORD = re.compile(r'\s+(?=into\s+)', re.IGNORECASE).finditer
_WHERE_KEYWORD = re.compile(r'\s+(?=(from|where)\s+(?!(.*?("(.*?(\.|;))|\.|(?:#\))))))', re.IGNORECASE).finditer

# Matches first whitespace characters after INSERT
# Then search for the tolog keyword 'into' or 'from'/'where' or to the
# end of the string. The content between INSERT and from (exclusive) / end of 
# string is returned as TM_FRAGMENT token
def t_tm_content(t):
    r'\s+'
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


if __name__ == '__main__':
    test_data = [
                 ]
    import tm.ply.lex as lex
    for data in test_data:
        lexer = lex.lex()
        lexer.input(data)
        while True:
            tok = lexer.token()
            if not tok: break
            print(tok)

