# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2009 -- Lars Heuer - Semagia <http://www.semagia.com/>.
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
Linear Topic Maps Notation (LTM) 1.3 lexer.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:version:      $Rev: 315 $ - $Date: 2009-12-25 15:01:14 +0100 (Fr, 25 Dez 2009) $
:license:      BSD license
"""
from tm.mio import MIOException
from mio.ltm.utils import unescape_unicode

directives = {
    'PREFIX': 'DIR_PREFIX',
    'VERSION': 'DIR_VERSION',
    'TOPICMAP': 'DIR_TOPICMAP',
    'MERGEMAP': 'DIR_MERGEMAP',
    'INCLUDE': 'DIR_INCLUDE',
    'BASEURI': 'DIR_BASEURI',
    }

tokens = tuple(directives.values()) + (
    # Identifiers
    'IDENT',
    'QNAME',

    # Literals
    'STRING', 'DATA',

    # Delimiters [ ] { } ( ) , ; : ~ = @ / %
    'LBRACK', 'RBRACK',
    'LCURLY', 'RCURLY',
    'LPAREN', 'RPAREN',
    'COMMA', 'SEMI', 'COLON', 'TILDE', 'EQ', 'AT', 'SLASH', 'PERCENT',
)

t_IDENT     = r'[a-zA-Z_][\-\.\w]*'
t_LBRACK    = r'\['
t_RBRACK    = r'\]'
t_LCURLY    = r'{'
t_RCURLY    = r'}'
t_LPAREN    = r'\('
t_RPAREN    = r'\)'
t_COLON     = r':'
t_COMMA     = r','
t_SEMI      = r';'
t_TILDE     = r'~'
t_EQ        = r'='
t_AT        = r'@'
t_SLASH     = r'/'
t_PERCENT   = r'%'

def t_error(t):
    raise MIOException('Unexpected token "%r"' % t)

def t_newline(t):
    r'[\r\n]+'
    t.lineno += len(t.value)

def t_ws(t):    # Disable unsused arg msg: pylint: disable-msg=W0613
    r'[\t ]+'
    pass

def t_comment(t):
    r'/\*([^*]|\*[^/])*\*/'
    t.lineno += t.value.count('\n')

def t_QNAME(t):
    t.value = t.value.split(':')
    return t

t_QNAME.__doc__ = r':'.join([t_IDENT, t_IDENT]) # Disable redefine __doc__ msg: pylint: disable-msg=W0622

def t_STRING(t):
    r'"([^"]|"{2})*"'
    val = t.value[1:-1].replace('""', '"')
    if not isinstance(val, unicode):
        val = unicode(val, 'utf-8')
    t.value = unescape_unicode(val)
    t.lineno += t.value.count('\n')
    return t

def t_DATA(t):
    r'\[\[([^\]]|\](?!\]))*\]\]'
    t.value = unescape_unicode(t.value[2:-2])
    t.lineno += t.value.count('\n')
    return t

def t_directive(t):
    r'\#[A-Z]+'
    t.type = directives.get(t.value[1:])
    if not t.type:
        raise MIOException('Unknown directive "%s"' % t.value)
    return t


if __name__ == '__main__':
    # For some reason pylint thinks that ply.lex and ply.yacc do not exist
    # pylint: disable-msg=F0401, E0611
    import ply.lex as lex
    lexer = lex.lex()
    test_data = [
                 '[semagia]', 
                 '[semagia = /* This is a comment */ "Semagia"]'
                 '[semagia = "\u0022Semagia\u0022"]',
                 '[semagia = "\u0022Sem""agia\u0022"]',
                 '[semagia = "\u0022\u0022Sem""agia\u0022"]',
                 '[beg = "Bjørg"]',
                 '[hiragana = "らがな"]'
                 ]
    for data in test_data:
        lexer.input(data)
        while True:
            tok = lexer.token()
            if not tok: break
            print tok
