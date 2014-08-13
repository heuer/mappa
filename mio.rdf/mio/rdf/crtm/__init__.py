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
from . import parser as parser_mod, lexer as lexer_mod


def _make_parser(base_iri, handler=None, prefix_listener=None, debug=False):
    parser = plyutils.make_parser(parser_mod, debug=debug)
    parser.context = parser_mod.ParserContext(base_iri)
    parser.handler = handler
    parser.prefix_listener = prefix_listener
    return parser


def _make_lexer(debug=False):
    return plyutils.make_lexer(lexer_mod, debug=debug)
