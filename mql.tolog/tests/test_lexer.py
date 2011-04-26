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
from nose.tools import ok_
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
        ok_(expected_type == tok.type, expected_type)
        ok_(expected_value == tok.value, expected_value)
        i+=1

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


if __name__ == '__main__':
    import nose
    nose.core.runmodule()

