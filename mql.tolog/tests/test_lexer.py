# -*- coding: utf-8 -*-
#
# Copyright (c) 2010 - 2011 -- Lars Heuer - Semagia <http://www.semagia.com/>.
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
Tests against the lexer.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD License
"""
from nose.tools import eq_
from tm import plyutils
import mql.tolog.lexer as lexer_mod

def lex(data, expected):
    lexer = plyutils.make_lexer(lexer_mod)
    lexer.input(data)
    i = 0
    while True:
        tok = lexer.token()
        if not tok:
            break
        expected_type, expected_value = expected[i]
        eq_(expected_type, tok.type)
        eq_(expected_value, tok.value)
        i+=1

def simple_lex(data):
    lexer = plyutils.make_lexer(lexer_mod)
    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok:
            break

def lex_tokenlist(data):
    """\
    Tokenizes `data` and returns a list of tokens.
    """
    lexer = plyutils.make_lexer(lexer_mod)
    lexer.input(data)
    tokens = []
    while True:
        tok = lexer.token()
        if not tok:
            break
        tokens.append(tok)
    return tokens

def fail(msg):
    raise AssertionError(msg)

def test_tm_fragment_from():
    data = (('''INSERT from-hell - "I am from hell".''',
              [('KW_INSERT', 'INSERT'), ('TM_FRAGMENT', 'from-hell - "I am from hell".')]),
            ('''INSERT #( from )# me. to. you. from tolog-predicate($x)''',
             [('KW_INSERT', 'INSERT'), ('TM_FRAGMENT', '#( from )# me. to. you.'), ('KW_FROM', 'from'), ('IDENT', 'tolog-predicate'), ('LPAREN', '('), ('VARIABLE', 'x'), ('RPAREN', ')')]),
             )
    for q, expected in data:
        yield lex, q, expected

def test_string_escape():
    data = '"Se""magia"'
    token = lex_tokenlist(data)[0]
    eq_('STRING', token.type)
    eq_('Se"magia', token.value)

def test_tokentypes():
    def check(data, expected):
        tokens = lex_tokenlist(data)
        eq_(len(expected), len(tokens))
        # Walk through the reference tokens and compare each with the 
        # generated tokens
        for i, ttype in enumerate(expected):
            eq_(ttype, tokens[i].type)

    for data, expected in _TEST_DATA:
        yield check, data, expected

def test_accept():
    for d in _ACCEPT_DATA:
        yield simple_lex, d

# (input, (tokentype1, tokentype2, ...))
_TEST_DATA = (
("instance-of($x, $y)", ('IDENT', 'LPAREN', 'VARIABLE', 'COMMA', 'VARIABLE', 'RPAREN')),

("select $x from instance-of($x, $y)", 
('KW_SELECT', 'VARIABLE', 'KW_FROM', 'IDENT', 'LPAREN', 'VARIABLE', 'COMMA', 'VARIABLE', 'RPAREN')),

("sEleCt $x frOm instance-of($x, $y)", 
('KW_SELECT', 'VARIABLE', 'KW_FROM', 'IDENT', 'LPAREN', 'VARIABLE', 'COMMA', 'VARIABLE', 'RPAREN')),

('q:name($x, $y)', ('QNAME', 'LPAREN', 'VARIABLE', 'COMMA', 'VARIABLE', 'RPAREN')),

('i"http://psi.example.org"($x, $y)', ('SID', 'LPAREN', 'VARIABLE', 'COMMA', 'VARIABLE', 'RPAREN')),

('a"http://www.semagia.com/"($x, $y)', ('SLO', 'LPAREN', 'VARIABLE', 'COMMA', 'VARIABLE', 'RPAREN')),

('s"http://www.semagia.com/"($x, $y)', ('IID', 'LPAREN', 'VARIABLE', 'COMMA', 'VARIABLE', 'RPAREN')),

("""
influenced-by($A, $B) :- {
  pupil-of($A : pupil, $B : teacher) |
  composed-by($OPERA : opera, $A : composer),
  based-on($OPERA : result, $WORK : source),
  written-by($WORK : work, $B : writer)
}.
""",
('IDENT', 'LPAREN', 'VARIABLE', 'COMMA', 'VARIABLE', 'RPAREN', 'IMPLIES', 'LCURLY',
'IDENT', 'LPAREN', 'VARIABLE', 'COLON', 'IDENT', 'COMMA', 'VARIABLE', 'COLON', 'IDENT', 'RPAREN', 'PIPE',
#composed-by (      $OPERA      :        opera    ,        $A          :        composer )
'IDENT', 'LPAREN', 'VARIABLE', 'COLON', 'IDENT', 'COMMA', 'VARIABLE', 'COLON', 'IDENT', 'RPAREN', 'COMMA',
#based-on (         
'IDENT', 'LPAREN', 'VARIABLE', 'COLON', 'IDENT', 'COMMA', 'VARIABLE', 'COLON', 'IDENT', 'RPAREN', 'COMMA',
#written-by
'IDENT', 'LPAREN', 'VARIABLE', 'COLON', 'IDENT', 'COMMA', 'VARIABLE', 'COLON', 'IDENT', 'RPAREN',
'RCURLY', 'DOT'
)),

("""
select $A, count($B) from
  composed-by($A : composer, $B : opera)
order by $B desc limit 1?
""", 
('KW_SELECT', 'VARIABLE', 'COMMA', 'KW_COUNT', 'LPAREN', 'VARIABLE', 'RPAREN', 'KW_FROM',
'IDENT', 'LPAREN', 'VARIABLE', 'COLON', 'IDENT', 'COMMA', 'VARIABLE', 'COLON', 'IDENT', 'RPAREN',
'KW_ORDER', 'KW_BY', 'VARIABLE', 'KW_DESC', 'KW_LIMIT', 'INTEGER', 'QM'
)),

("""
composed-by($A : composer, $B : opera)?

Everything after an ? must be ignored a.k.a. do not produce tokens and failures :)
""",
('IDENT', 'LPAREN', 'VARIABLE', 'COLON', 'IDENT', 'COMMA', 'VARIABLE', 'COLON', 'IDENT', 'RPAREN', 'QM')
),
('''
    foo.
    f.oo
    f12oo
    foo.12
''',
('IDENT', 'DOT', 'IDENT', 'IDENT', 'IDENT')),
)

_ACCEPT_DATA = (
    
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
'''INSERT
  from . from article-about($topic, $psi)''',
'''INSERT
  from . from . from article-about($topic, $psi)''',
'''INSERT
  from .''',
'''INSERT where-are-you - "Where are you".''',
'''INSERT #( where )# a. b. c. where tolog-predicate($x)''',
'''INSERT
  where . where article-about($topic, $psi)''',
'''INSERT
  where . where . where article-about($topic, $psi)''',
'''INSERT
  where .''',
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
                 ' /= ',
                 '[CU:RIE] [c:/ddjdjjdjdjdd]',
)

if __name__ == '__main__':
    import nose
    nose.core.runmodule()

