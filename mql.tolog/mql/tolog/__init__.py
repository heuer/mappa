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
Provides functions to parse tolog queries.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
from functools import partial
import lxml.sax
from tm import plyutils, xmlutils
from . import handler as handler_mod, xsl

__all__ = ('parse', 'parse_query')

def parse(query, handler, tolog_plus=False):
    """\
    Parses the provided query and issues events against the provided handler.
    
    `handler`
        The ParserHandler which receives the parsing events.
    `tolog_plus`
        Indicates if tolog+ mode should be enabled.
    """
    if hasattr(query, 'read'): #TODO: Use tm.mio.Source
        query = query.read()
    from mql.tolog import lexer as lexer_mod, parser as parser_mod
    parser = plyutils.make_parser(parser_mod)
    parser_mod.initialize_parser(parser, handler, tolog_plus)
    handler.start()
    parser.parse(query, lexer=plyutils.make_lexer(lexer_mod))
    handler.end()


def parse_query(query, handler=None, tolog_plus=False):
    """\
    Parses and optimizes the query and returns an executable query.
    
    `handler`
        The QueryHandler which receives the events to construct a query
    `tolog_plus`
        Indicates if tolog+ mode should be enabled.
    """
    handler = handler or handler_mod.DefaultQueryHandler()
    xsl.apply_default_transformations(parse_to_etree(query, tolog_plus), 
                                        partial(xsl.saxify, handler=handler_mod.SAXHandler(handler)))
    return handler.query


def parse_to_etree(query, tolog_plus=False):
    """\
    Returns the provided query as Etree.
    
    `tolog_plus`
        Indicates if tolog+ mode should be enabled.
    """
    contenthandler = lxml.sax.ElementTreeContentHandler()
    parse(query, handler_mod.XMLParserHandler(xmlutils.SAXSimpleXMLWriter(contenthandler)), tolog_plus)
    return contenthandler.etree
