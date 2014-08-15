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
from __future__ import absolute_import
from urllib import urlopen
from tm import mio, plyutils
from . import parser as parser_mod, lexer as lexer_mod


class CRTMMappingReader(object):
    """\
    CRTM mapping reader.
    """
    def __init__(self):
        self.handler = None

    def read(self, src):
        self.handler.start()
        parser = _make_parser(src.iri, self.handler)
        data = src.stream
        if not data:
            try:
                data = urlopen(src.iri)
            except IOError:
                raise mio. MIOException('Cannot read from "%s"' % src.iri)
        parser.parse(data, _make_lexer())
        self.handler.end()


def _make_parser(base_iri, handler=None, debug=False):
    parser = plyutils.make_parser(parser_mod, debug=debug)
    parser.context = parser_mod.ParserContext(base_iri)
    parser.handler = handler
    return parser


def _make_lexer(debug=False):
    return plyutils.make_lexer(lexer_mod, debug=debug)
