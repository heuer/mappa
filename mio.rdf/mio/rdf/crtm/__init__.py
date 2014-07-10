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
from tm import plyutils
from mio.rdf.crtm import parser as parser_mod, lexer as lexer_mod


def make_parser(base_iri, debug=False):
    parser = plyutils.make_parser(parser_mod, debug=debug)
    parser.context = parser_mod.ParserContext(base_iri)
    parser.handler = None
    return parser


def make_lexer(debug=False):
    return plyutils.make_lexer(lexer_mod, debug=debug)
