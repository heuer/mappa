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
#     * Neither the project name nor the names of the contributors may be 
#       used to endorse or promote products derived from this software 
#       without specific prior written permission.
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
Compact Topic Maps (CTM) lexer.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
# For some reason pylint thinks that ply.lex and ply.yacc do not exist
# pylint: disable-msg=F0401, E0611
from ply.lex import TOKEN
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
_ident_start = ur'[a-zA-Z_]|[\u00C0-\u00D6]|[\u00D8-\u00F6]' + \
                ur'|[\u00F8-\u02FF]|[\u0370-\u037D]' + \
                ur'|[\u037F-\u1FFF]|[\u200C-\u200D]' + \
                ur'|[\u2070-\u218F]|[\u2C00-\u2FEF]' + \
                ur'|[\u3001-\uD7FF][\uF900-\uFDCF]|[\uFDF0-\uFFFD]'

_ident_part = ur'[\-0-9]|%s|\u00B7|[\u0300-\u036F]|[\u203F-\u2040]' % _ident_start

# Identifier
_ident = ur'(?:(?:%s)+(?:\.*(?:%s)+)*)' % (_ident_start, _ident_part)


_date = r'\-?[0-9]{4,}\-(0[1-9]|1[0-2])\-(0[1-9]|1[0-9]|2[0-9]|3[0-1])'
# Timezone
_tz = r'Z|((\+|\-)[0-9]{2}:[0-9]{2})'
# Time
_time = r'[0-9]{2}:[0-9]{2}:[0-9]{2}(\.[0-9]+)?(%s)?' % _tz

t_WILDCARD = r'\?'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LBRACK = r'\['
t_RBRACK = r'\]'
t_COMMA = r','
t_SEMI = r';'
t_COLON = r':'
t_DOT = r'\.'
t_DOUBLE_CIRCUMFLEX = r'\^\^'
t_EQ  = r'='
t_CIRCUMFLEX = r'\^'
t_TILDE = r'~'
t_HYPHEN = '-'
t_AT = r'@'
t_STAR = r'\*'


states = (
  ('mlcomment', 'exclusive'),
)


def t_error(t):
    raise MIOException('Unexpected token "%r"' % t)

def t_mlcomment(t):
    r'\#\('
    t.lexer.comment_level = 1
    t.lexer.begin('mlcomment')

def t_mlcomment_content(t):
    r'[^#\(\)]+'
    t.lexer.lineno += t.value.count('\n')

def t_mlcomment_start(t):
    r'\#\('
    t.lexer.comment_level += 1

def t_mlcomment_end(t):
    r'\)\#'
    t.lexer.comment_level -= 1
    if t.lexer.comment_level == 0:
        t.lexer.begin('INITIAL')

def t_mlcomment_content2(t):
    r'\#|\(|\)'

def t_mlcomment_error(t):
    raise MIOException('Unexpected token "%r"' % t)

def t_comment(t):
    r'\#[^\r\n]*'

def t_ws(t):
    r'\s+'
    t.lexer.lineno += t.value.count('\n')

def t_IRI(t):
    r'[a-zA-Z]+[a-zA-Z0-9\+\-\.]*://([;\.\)]*[^\s;\]\.\(\)]+)+'
    return t

def t_iri2(t):
    '<[^<>\"\{\}\`\\ ]+>'
    t.value = t.value[1:-1]
    t.type = 'IRI'
    return t

def t_directive(t):
    r'%[a-z]+'
    directive = _DIRECTIVES.get(t.value)
    if not directive:
        raise MIOException('Unknown directive %s' % t.value)
    t.type = directive
    return t 

@TOKEN(ur'%s:(\.*(%s))+' % (_ident, _ident_part))
def t_QNAME(t):
    t.value = tuple(t.value.split(':'))
    return t

@TOKEN(_ident)
def t_IDENT(t):
    t.type = _KEYWORDS.get(t.value, 'IDENT')
    return t

@TOKEN(ur'\$%s' % _ident)
def t_VARIABLE(t):
    t.value = t.value[1:]
    return t

@TOKEN(ur'\?%s' % _ident)
def t_NAMED_WILDCARD(t):
    t.value = t.value[1:]
    return t

@TOKEN(r'%sT%s' % (_date, _time))
def t_DATE_TIME(t):
    return t

@TOKEN(_date)
def t_DATE(t):
    return t

def t_DECIMAL(t):
    r'(\-|\+)?([0-9]+\.[0-9]+|\.([0-9])+)'
    return t

def t_INTEGER(t):
    r'(\-|\+)?[0-9]+'
    return t

def t_triple_string(t):
    r'"{3}([^"\\]|(\\[\\"rntuU])|"|"")*"{3}'
    t.value = t.value[3:-3]
    t.type = 'STRING'
    t.lexer.lineno += t.value.count('\n')
    return t

def t_STRING(t):
    r'"([^"\\]|(\\[\\"rntuU]))*"'
    t.value = t.value[1:-1]
    t.lexer.lineno += t.value.count('\n')
    return t

if __name__ == '__main__':
    import ply.lex as lex
    lexer = lex.lex()
    test_data = [
                 'semagia.',
                 '<http://www.semagia.com/sid>.',
                 'http://www.semagia.com/sid.',
                 'http://www.semagia.com/sid(',
                 'http://www.semagia.com/sid)',
                 'http://www.semagia.com/sid[',
                 'http://www.semagia.com/sid]',
                 '^<#iid>',
                 'q:name ',
                 'another:0ne',
                 'next:123',
                 'next-one:.123..1',
                 '-1976-09-19',
                 '1976-09-19',
                 '1976-09-19T24:24:24',
                 '1 -1  +1',
                 '1.1 +1.1 -1.1 .12',
                 'Semagia - "Semagia".',
                 '_semagia-id',
                 's123456',
                 '@attention, please',
                 '([)]:,.^-^^=~*',
                 u'üäö',
                 u'ün.test - "Ün test".',
                 '%include %mergemap %prefix %encoding %version',
                 'def end isa ako',
                 '?who ?',
                 u'$variable $variüble $ün.variüble',
                 u'?ün.wüldcard',
                 'ui #a comment! :)))',
                 '''hey #( This
                 is a multiline comment #( nested )# )# ho''',
                 '''"""This is
                 a "string<p class="stupid"/>"""''',
                 '''"This is 
                 also a string"''',
                 '"Quote (\\") character"',
                 '''%prefix 

#(

a

)#

ex 

# A comment

http://psi.example.org/ ex:fake.''',
                 u'yippiieehhya...yeah___3..2...1...----0...boom',
                 'a123',
                 ]
    for data in test_data:
        lexer.input(data)
        while True:
            tok = lexer.token()
            if not tok: break
            print(tok)
