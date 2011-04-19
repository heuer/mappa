# -*- coding: utf-8 -*-
#
# Copyright (c) 2010 -- Lars Heuer - Semagia <http://www.semagia.com/>.
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
tolog lexer.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD License
"""
import re
from ply.lex import TOKEN #pylint: disable-msg=F0401, E0611
from tm.mql import SyntaxQueryError

# We allow something like INSERT from . from . from tolog-predicate
# for the time being although the tolog spec. says that it is an error since
# 'from' is a tolog keyword.
_END_OF_FRAGMENT = re.compile(r'$|\s+(?=from\s+(?!(.*?("|\.|\#))))', re.IGNORECASE).search

# Start of an identifier
_IDENT_START = ur'[a-zA-Z_]|[\u00C0-\u00D6]|[\u00D8-\u00F6]' + \
                ur'|[\u00F8-\u02FF]|[\u0370-\u037D]' + \
                ur'|[\u037F-\u1FFF]|[\u200C-\u200D]' + \
                ur'|[\u2070-\u218F]|[\u2C00-\u2FEF]' + \
                ur'|[\u3001-\uD7FF]|[\uF900-\uFDCF]|[\uFDF0-\uFFFD]'

_IDENT_PART = ur'%s|[\.\-0-9]|[\u00B7]|[\u0300-\u036F]|[\u203F-\u2040]' % _IDENT_START

# Identifier
_IDENT = ur'(%s)+(%s)*' % (_IDENT_START, _IDENT_PART)

_DATE = r'\-?(000[1-9]|00[1-9][0-9]|0[1-9][0-9][0-9]|[1-9][0-9][0-9][0-9]+)\-(0[1-9]|1[0-2])\-(0[1-9]|1[0-9]|2[0-9]|3[0-1])'
# Timezone
_TZ = r'Z|((\+|\-)[0-9]{2}:[0-9]{2})'
# Time
_TIME = r'[0-9]{2}:[0-9]{2}:[0-9]{2}(\.[0-9]+)?(%s)?' % _TZ

_DIRECTIVES = {
    # tolog extensions
    '%version': 'DIR_VERSION',
    '%prefix': 'DIR_PREFIX',
}

reserved = {
    'select': 'KW_SELECT',
    'from': 'KW_FROM',
    'where': 'KW_FROM',
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
    }

tokens = tuple(set(reserved.values())) + tuple(_DIRECTIVES.values()) + (
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
)

t_ignore = ' \t'

t_EQ        = r'='
t_NE        = r'(/|!)='
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

t_DIR_VERSION = r'%version'
t_DIR_PREFIX = r'%prefix'

states = (
   ('tm','exclusive'),
)


#pylint: disable-msg=W0613, W0622

def t_error(t):
    raise SyntaxQueryError('Invalid tolog syntax: %r' % t) #TODO

def t_comment(t):
    r'/\*[^\*/]*\*/'
    t.lexer.lineno += t.value.count('\n')

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

@TOKEN(r'\[[^\]]+\]')
def t_CURIE(t):
    t.value = t.value[1:-1]
    return t

@TOKEN(r':'.join([_IDENT, r'[_\w\.-]+']))
def t_QNAME(t):
    return t

@TOKEN(_IDENT)
def t_IDENT(t):
    t.type = reserved.get(t.value.lower(), 'IDENT')
    if t.type == 'KW_INSERT':
        t.lexer.begin('tm') # Switch to TM mode
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

# Matches first whitespace characters after INSERT
# Then search for the tolog keyword 'from' or to the
# end of the string. The content between INSERT and from (exclusive) / end of 
# string is returned as TM_FRAGMENT token
def t_tm_content(t):
    r'\s+'
    m = _END_OF_FRAGMENT(t.lexer.lexdata, t.lexer.lexpos)
    if not m:
        raise Exception('Internal error: Cannot find topic map content to insert')
    t.value = t.lexer.lexdata[t.lexer.lexpos:m.start()]
    t.type = 'TM_FRAGMENT'
    t.lexer.lineno += t.value.count('\n')
    # Move the lexer's position to the end of the TM fragment 
    # but in advance of the optional 'from' keyword
    t.lexer.lexpos = m.end()
    # Continue with tolog
    t.lexer.begin('INITIAL')
    return t

def t_tm_error(t):
    raise Exception() #TODO

if __name__ == '__main__':
    test_data = [
                 'select $x from instance-of($x, $y)?',
                 'homepage($t, "http://www.semagia.com/")?',
                 'homepage($t, "http://www.semagia.com/")? Ignore this text, please',
                 '''INSERT
  tolog-updates isa update-language;
    - "tolog updates".''',
                 '''import "http://psi.ontopia.net/tolog/string/" as str
  insert $topic $psi . from
  article-about($topic, $psi),
  str:starts-with($psi, "http://en.wikipedia.org/wiki/")''',
                '''update value($TN, "Ontopia") from
  topic-name(oks, $TN)''',
                    '''merge $T1, $T2 from
  email($T1, $EMAIL),
  email($T2, $EMAIL)''',
                '''influenced-by($A, $B) :- {
  pupil-of($A : pupil, $B : teacher) |
  composed-by($OPERA : opera, $A : composer),
  based-on($OPERA : result, $WORK : source),
  written-by($WORK : work, $B : writer)
}.

instance-of($COMPOSER, composer),
influenced-by($COMPOSER, $INFLUENCE),
born-in($INFLUENCE : person, $PLACE : place),
not(located-in($PLACE : containee, italy : container))?''',
'''INSERT from-hell - "I am from hell".''',
'''INSERT #( from )# me. to. you. from tolog-predicate($x)''',
'''INSERT
  from . from article-about($topic, $psi)''',
'''INSERT
  from . from . from article-about($topic, $psi)''',
'''INSERT
  from .''',
'''schau an, ein <http://iri.here>''',
'''do-you-recognise-the-lt<here?''',
'''"oh ein"^^xsd:string''',
                 '-1976-09-19',
                 '1976-09-19',
                 '1976-09-19T24:24:24',
                 '1 -1  +1',
                 '1.1 +1.1 -1.1 .12',
                 'opera:influenced-by($COMPOSER, $INFLUENCE)',
                 'a %param% here',
                 'update value(@2312, "Ontopia")',
                 'update value(@2312heresom3thing3ls3, "Ontopia")',
                 'update value(@tritratrullala, "Ontopia")',
                 '%prefix bla <http://www.semagia.com/>',
                 ' ^<http://www.semagia.com/>',
                 ' "x"^^<http://www.semagia.com/>',
                 ' select $x where bla($blub)?',
                 ' != /= ',
                 '[CU:RIE] [c:/ddjdjjdjdjdd]',
                 ]
    import ply.lex as lex
    for data in test_data:
        lexer = lex.lex()
        lexer.input(data)
        while True:
            tok = lexer.token()
            if not tok: break
            print(tok)

