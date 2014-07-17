# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\


:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
from mio.rdf.crtm import _make_lexer as make_lexer


def lex(data):
    """\

    """
    lexer = make_lexer()
    lexer.input(data)
    while True:
        tok = lexer.token()
        if not tok:
            break
        #print(tok)


def test_accept():
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
                 u"%prefix %include",
                 u'trara # ein Kommentar',
                 ]
    for d in test_data:
        yield lex, d


if __name__ == '__main__':
    import nose
    nose.core.runmodule()
