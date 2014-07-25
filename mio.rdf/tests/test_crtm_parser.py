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
from nose.tools import ok_
from mio.rdf.crtm import _make_parser as make_parser, _make_lexer as make_lexer
from mio.rdf.mapping import MappingHandler


def mk_parser():
    base = u'http://mio.semagia.com/'
    return make_parser(base, debug=True)


def parse(data):
    """\

    """
    parser = mk_parser()
    parser.parse(data, lexer=make_lexer())


def test_make_parser():
    parser = mk_parser()
    ok_(parser)
    ok_(parser.handler is None)
    handler = MappingHandler()
    parser.handler = handler
    ok_(parser.handler is handler)


def test_accept():
    data = [u'''%prefix ident <iri>''',
            u'''%prefix ident <iri> ident:local: occ''',
            u'''%prefix ident <iri> ident:local: occurrence''',
            u'''%prefix ident <iri> ident:local: occ <bla:type>''',
            u'''%prefix ident <iri> ident:local: occurrence <bla:type>''',
            u'''%prefix ident <iri> ident:local: <bla:type>''',
            u'''%prefix ident <iri> ident:local: name''',
            u'''%prefix ident <iri> ident:local: -''',
            u'''%prefix q <iri> q { name: name 123: occurrence 393.333: -}''',
            u'''%prefix q <iri> q { b, c: name d,e: occurrence f, g, h: -}''',
            u'''%prefix q <iri>
                q:b, q:c: name
                q:d, q:e: occurrence q:f, q:g, q:h: -
                ''']
    for d in data:
        yield parse, d


if __name__ == '__main__':
    import nose
    nose.core.runmodule()
