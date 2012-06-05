# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2012 -- Lars Heuer - Semagia <http://www.semagia.com/>.
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
from urllib2 import urlopen
import lxml.sax #TODO: Any chance to remove this dependency (here)?
from tm import plyutils, xmlutils
from . import handler as handler_mod, xsl

__all__ = ('parse', 'parse_query')

def parse(src, handler, tolog_plus=False):
    """\
    Parses the provided query and issues events against the provided handler.
    
    `src`
        A `tm.Source` instance to read the query from.
    `handler`
        A `ITologHandler` which receives the events generated by the parser.
    `tolog_plus`
        Indicates if tolog+ parsing mode should be enabled.
        Note: If the query starts with a ``%version`` directive, the 
        tolog+ mode is enabled automatically, regardless of the provided
        `tolog_plus` value
    """
    from mql.tolog import lexer as lexer_mod, parser as parser_mod
    parser = plyutils.make_parser(parser_mod)
    parser_mod.initialize_parser(parser, handler, tolog_plus)
    data = src.stream or urlopen(src.iri)
    handler.start()
    parser.parse(data.read(), lexer=plyutils.make_lexer(lexer_mod))
    handler.end()


def parse_query(src, handler=None, tolog_plus=False, optimizers=None):
    """\
    Parses and optimizes the query and returns an executable query.
    
    `src`
        A `tm.Source` instance to read the query from.
    `handler`
        A `IQueryHandler` which receives events to construct a query
    `tolog_plus`
        Indicates if tolog+ parsing mode should be enabled.
        Note: If the query starts with a ``%version`` directive, the 
        tolog+ mode is enabled automatically, regardless of the provided
        `tolog_plus` value
    `optimizers`
        An optional iterable of optimizer names which should be applied to
        the parsed provided query. If the optimizers are not provided,
        a default set of optimizers will be applied to the query.
        To omit any optimization, an empty iterable must be provided.
    """
    handler = handler or handler_mod.make_queryhandler()
    if optimizers is None:
        optimizers = xsl.DEFAULT_TRANSFORMERS
    xsl.apply_transformations(parse_to_etree(src, tolog_plus), optimizers,
                                        partial(xsl.saxify, handler=handler_mod.TologXMLContentHandler(handler)))
    return handler.query


def parse_to_etree(src, tolog_plus=False):
    """\
    Returns the provided query as Etree.
    
    `src`
        A `tm.Source` instance to read the query from.
    `tolog_plus`
        Indicates if tolog+ parsing mode should be enabled.
        Note: If the query starts with a ``%version`` directive, the 
        tolog+ mode is enabled automatically, regardless of the provided
        `tolog_plus` value
    """
    contenthandler = lxml.sax.ElementTreeContentHandler()
    parse(src, handler_mod.XMLHandler(xmlutils.SAXSimpleXMLWriter(contenthandler)), tolog_plus)
    return contenthandler.etree


def parse_to_tolog(src, tolog_plus=False, hints=False, optimizers=None):
    """\
    Parses the provided query and returns the query as an optimized tolog
    query string. 
    
    This function is mainly useful for debugging purposes.
    
    `src`
        A `tm.Source` instance to read the query from.
    `tolog_plus`
        Indicates if tolog+ parsing mode should be enabled.
        Note: If the query starts with a ``%version`` directive, the 
        tolog+ mode is enabled automatically, regardless of the provided
        `tolog_plus` value
    `hints`
        Indicates if the resulting tolog query string should contain hints
        which are inserted by the query optimizer (disabled by default).
    `optimizers`
        An optional iterable of optimizer names which should be applied to
        the parsed provided query. If the optimizers are not provided,
        a default set of optimizers will be applied to the query.
        To omit any optimization, an empty iterable must be provided.
    """
    return _back_to_tolog(src, False, tolog_plus=tolog_plus, hints=hints, optimizers=optimizers)
    

def parse_to_tologplus(src, tolog_plus=False, hints=False, optimizers=None):
    """\
    Parses the provided query and returns the query as an optimized tolog+
    query string. 
    
    `src`
        A `tm.Source` instance to read the query from.
    `tolog_plus`
        Indicates if tolog+ parsing mode should be enabled.
        Note: If the query starts with a ``%version`` directive, the 
        tolog+ mode is enabled automatically, regardless of the provided
        `tolog_plus` value
    `hints`
        Indicates if the resulting tolog query string should contain hints
        which are inserted by the query optimizer (disabled by default).
    `optimizers`
        An optional iterable of optimizer names which should be applied to
        the parsed provided query. If the optimizers are not provided,
        a default set of optimizers will be applied to the query.
        To omit any optimization, an empty iterable must be provided.
    """
    return _back_to_tolog(src, True, tolog_plus=tolog_plus, hints=hints, optimizers=optimizers)


def _back_to_tolog(src, tolog_plus_out, tolog_plus=False, hints=False, optimizers=None):
    """\
    Parses the provided query and returns the query as an optimized tolog(+)
    query string. 
    
    `src`
        A `tm.Source` instance to read the query from.
    `tolog_plus_out`
        Indicates if the resulting query should use tolog+ syntax.
    `tolog_plus`
        Indicates if tolog+ parsing mode should be enabled.
        Note: If the query starts with a ``%version`` directive, the 
        tolog+ mode is enabled automatically, regardless of the provided
        `tolog_plus` value
    `hints`
        Indicates if the resulting tolog query string should contain hints
        which are inserted by the query optimizer (disabled by default).
    `optimizers`
        An optional iterable of optimizer names which should be applied to
        the parsed provided query. If the optimizers are not provided,
        a default set of optimizers will be applied to the query.
        To omit any optimization, an empty iterable must be provided.
    """
    if optimizers is None:
        optimizers = xsl.DEFAULT_TRANSFORMERS
    transformers = tuple(optimizers) + ('back-to-tolog',)
    return xsl.apply_transformations(parse_to_etree(src, tolog_plus), 
                                        transformers,
                                        **{'render-hints': '"true"' if hints else '"false"',
                                           'tolog-plus': '"true"' if tolog_plus_out else '"false"'})
