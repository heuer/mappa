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
    u'%prefix': u'DIR_PREFIX',
    u'%include': u'DIR_INCLUDE',
    u'%version': u'DIR_VERSION',
    u'%langtoscope': u'DIR_LANG2SCOPE',
}

_KEYWORDS = {
    u'true': u'KW_TRUE',
    u'false': u'KW_FALSE',
    u'lang': u'KW_LANG',
}

_KEYWORDS_MAPPING = {
    u'subject-identifier': u'KW_SID', u'sid': u'KW_SID',
    u'subject-locator': u'KW_SLO', u'slo': u'KW_SLO',
    u'item-identifier': u'KW_IID', u'iid': u'KW_IID',
    u'isa': u'KW_ISA',
    u'ako': u'KW_AKO',
    u'occurrence': u'KW_OCC', u'occ': u'KW_OCC',
    u'association': u'KW_ASSOC', u'assoc': u'KW_ASSOC',
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
    u'IDENT', u'QNAME', u'IRI',
    # Brackets
    u'LPAREN', u'RPAREN', u'LCURLY', u'RCURLY',
    # Delimiters
    u'AT', u'HYPHEN', u'COLON', u'COMMA', u'SEMI', u'EQ',
    )

t_LPAREN = ur'\('
t_RPAREN = ur'\)'
t_LCURLY = ur'{'
t_RCURLY = ur'}'
t_COMMA = ur','
t_HYPHEN = u'-'
t_AT = ur'@'
t_lang_EQ = ur'='

states = (
  (u'kw', u'exclusive'),
  (u'lang', u'exclusive'),
)


def t_error(t):
    raise mio.MIOException(u'Unknown token "%r"' % t)

t_lang_error = t_error
t_kw_error = t_error


def t_comment(t):
    ur'\#[^\r\n]*'


def t_ws(t):
    r'\s+'
    t.lexer.lineno += t.value.count(u'\n')


def t_SEMI(t):
    ur';'
    t.lexer.begin(u'lang')
    return t


def t_COLON(t):
    ur':'
    t.lexer.begin(u'kw')
    return t


@TOKEN('|'.join(_DIRECTIVES.keys()))
def t_directive(t):
    t.type = _DIRECTIVES[t.value]
    if t.value == u'%langtoscope':
        t.lexer.begin(u'lang')
    return t


@TOKEN(_iri)
def t_IRI(t):
    t.value = t.value[1:-1]
    return t


@TOKEN(_qname)
def t_QNAME(t):
    t.value = tuple(t.value.split(u':'))
    return t


@TOKEN(_ident)
def t_IDENT(t):
    return t


# State LANG
def t_lang_ws(t):
    ur'\s+'
    t.lexer.lineno += t.value.count(u'\n')


@TOKEN(u'|'.join(_KEYWORDS.keys()))
def t_lang_commons(t):
    t.type = _KEYWORDS[t.value]
    if t.value in (u'true', u'false'):
        t.lexer.begin(u'INITIAL')
    return t


def t_lang_end(t):
    ur'.'
    t.lexer.lexpos = t.lexpos-1 # Pushback one char
    t.lexer.begin(u'INITIAL')


# State KW
def t_kw_ws(t):
    ur'\s+'
    t.lexer.lineno += t.value.count(u'\n')


@TOKEN(u'|'.join(_KEYWORDS_MAPPING.keys()))
def t_kw_keyword(t):
    t.type = _KEYWORDS_MAPPING[t.value]
    return t


def t_kw_end(t):
    ur'.'
    t.lexer.lexpos = t.lexpos-1 # Pushback one char
    t.lexer.begin(u'INITIAL')


if __name__ == '__main__':
    import tm.ply.lex as lex
    lexer = lex.lex()
    test_data = [
                 u'semagia',
                 u'<http://www.semagia.com/sid>',
                 u'something: occurrence',
                 u'q:name q:123 foaf:name q:12name q:12.2',
                 u'hello.again _1 lang name true false occurrence occ assoc association hello.ag.ain',
                 u'%langtoscope true true',
                 u"%prefix bla <http://psi.semagia.com/test>",
                 u"foaf:name: name",
                 u"web:site: occurrence web:site: occ"
                 u";lang true false",
                 u"lang true false",
                 u"%prefix %include %version",
                 u'trara # ein Kommentar',
                 ]
    for data in test_data:
        lexer.input(data)
        while True:
            tok = lexer.token()
            if not tok:
                break
            print(tok)
