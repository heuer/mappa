# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
Compact RTM (CRTM) lexer.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
from tm.ply import TOKEN
from tm import mio

_DIRECTIVES = {
    '%prefix': 'DIR_PREFIX',
    '%include': 'DIR_INCLUDE',
    '%version': 'DIR_VERSION',
    '%langtoscope': 'DIR_LANG2SCOPE',
}

_KEYWORDS = {
    'true': 'KW_TRUE',
    'false': 'KW_FALSE',
    'lang': 'KW_LANG',
}

_KEYWORDS_MAPPING = {
    'subject-identifier': 'KW_SID', 'sid': 'KW_SID',
    'subject-locator': 'KW_SLO', 'slo': 'KW_SLO',
    'item-identifier': 'KW_IID', 'iid': 'KW_IID',
    'isa': 'KW_ISA',
    'ako': 'KW_AKO',
    'occurrence': 'KW_OCC', 'occ': 'KW_OCC',
    'association': 'KW_ASSOC', 'assoc': 'KW_ASSOC',
}

_ident_start = ur'[a-zA-Z_]|[\u00C0-\u00D6]|[\u00D8-\u00F6]' + \
                ur'|[\u00F8-\u02FF]|[\u0370-\u037D]' + \
                ur'|[\u037F-\u1FFF]|[\u200C-\u200D]' + \
                ur'|[\u2070-\u218F]|[\u2C00-\u2FEF]' + \
                ur'|[\u3001-\uD7FF]|[\uF900-\uFDCF]|[\uFDF0-\uFFFD]'
_ident_char = ur'%s|[\-0-9]|\u00B7|[\u0300-\u036F]|[\u203F-\u2040]' % _ident_start
_ident = ur'(%s)+(\.*(%s))*' % (_ident_start, _ident_char)
_local_part = ur'([0-9]+(\.*(%s))*)' % _ident_char
_qname = ur'(%s):((%s)|(%s))' % (_ident, _local_part, _ident)
_iri = ur'<[^<>\"\{\}\`\\ ]+>'


tokens = tuple(_DIRECTIVES.values()) + tuple(_KEYWORDS.values()) + tuple(set(_KEYWORDS_MAPPING.values())) + (
    'IDENT', 'QNAME', 'IRI',
    # Brackets
    'LPAREN', 'RPAREN', 'LCURLY', 'RCURLY',
    # Delimiters
    'AT', 'HYPHEN', 'COLON', 'COMMA', 'SEMI', 'EQ',
    )

t_LPAREN = r'\('
t_RPAREN = r'\)'
t_LCURLY = r'{'
t_RCURLY = r'}'
t_COMMA = r','
t_HYPHEN = '-'
t_AT = r'@'
t_lang_EQ  = r'='

states = (
  ('kw', 'exclusive'),
  ('lang', 'exclusive'),
)

def t_error(t):
    raise mio.MIOException('Unknown token "%r"' % t)

t_lang_error = t_error
t_kw_error = t_error

def t_comment(t):
    r'\#[^\r\n]*'

def t_ws(t):
    r'\s+'
    t.lexer.lineno += t.value.count('\n')

def t_SEMI(t):
    r';'
    t.lexer.begin('lang')
    return t

def t_COLON(t):
    r':'
    t.lexer.begin('kw')
    return t

@TOKEN('|'.join(_DIRECTIVES.keys()))
def t_directive(t):
    t.type = _DIRECTIVES[t.value]
    if t.value == '%langtoscope':
        t.lexer.begin('lang')
    return t

@TOKEN(_iri)
def t_IRI(t):
    t.value = t.value[1:-1]
    return t

@TOKEN(_qname)
def t_QNAME(t):
    t.value = tuple(t.value.split(':'))
    return t

@TOKEN(_ident)
def t_IDENT(t):
    return t

# State LANG
def t_lang_ws(t):
    r'\s+'
    t.lexer.lineno += t.value.count('\n')

@TOKEN('|'.join(_KEYWORDS.keys()))
def t_lang_commons(t):
    t.type = _KEYWORDS[t.value]
    if t.value in ('true', 'false'):
        t.lexer.begin('INITIAL')
    return t

def t_lang_end(t):
    r'.'
    t.lexer.lexpos = t.lexpos-1 # Pushback one char
    t.lexer.begin('INITIAL')

# State KW
def t_kw_ws(t):
    r'\s+'
    t.lexer.lineno += t.value.count('\n')

@TOKEN('|'.join(_KEYWORDS_MAPPING.keys()))
def t_kw_keyword(t):
    t.type = _KEYWORDS_MAPPING[t.value]
    return t

def t_kw_end(t):
    r'.'
    t.lexer.lexpos = t.lexpos-1 # Pushback one char
    t.lexer.begin('INITIAL')

if __name__ == '__main__':
    import tm.ply.lex as lex
    lexer = lex.lex()
    test_data = [
                 'semagia',
                 '<http://www.semagia.com/sid>',
                 'something: occurrence',
                 'q:name q:123 foaf:name q:12name q:12.2',
                 'hello.again _1 lang name true false occurrence occ assoc association hello.ag.ain',
                 '%langtoscope true true',
                 "%prefix bla <http://psi.semagia.com/test>",
                 "foaf:name: name",
                 "web:site: occurrence web:site: occ"
                 ";lang true false",
                 "lang true false",
                 "%prefix %include %version",
                 'trara # ein Kommentar',
                 ]
    for data in test_data:
        lexer.input(data)
        while True:
            tok = lexer.token()
            if not tok: break
            print(tok)
    
