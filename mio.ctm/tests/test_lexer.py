# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
Tests against mio.ctm.lexer.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
from nose.tools import eq_
from mio.ctm import _make_lexer as make_lexer


def the_lexer(data):
    lexer = make_lexer()
    lexer.input(data)
    return lexer


def lex(data, expected):
    lexer = the_lexer(data)
    i = 0
    while True:
        tok = lexer.token()
        if not tok:
            break
        expected_type, expected_value = expected[i]
        eq_(expected_type, tok.type)
        eq_(expected_value, tok.value)
        i += 1


def simple_lex(data):
    lexer = the_lexer(data)
    while True:
        tok = lexer.token()
        if not tok:
            break


def test_accept():
    for d in _DATA:
        yield simple_lex, d


_DATA = [
                 u'k:reden-beëndiging-ambtsbekleding .',
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
                 u'ü͡ØΨ㬟͡.'
                 ]


if __name__ == '__main__':
    import nose
    nose.core.runmodule()
