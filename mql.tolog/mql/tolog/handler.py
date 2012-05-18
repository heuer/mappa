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
tolog handler implementations.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD License
"""
import logging
from . import consts

class ParserHandler(object):
    """\
    Common superclass of tolog handlers.
    """
    pass

class NoopParserHandler(ParserHandler):
    """\
    A TologHandler which does nothing.
    """
    def __getattr__(self, name):
        def noop(*args): pass
        return noop

class LoggingParserHandler(ParserHandler):
    """\
    A TologHandler which loggs all events and delegates the events to
    an underlying TologHandler instance.
    """
    def __init__(self, handler, level='info'):
        """\
        `handler`
            The TologHandler instance which should receive the events.
        `level`
            The logging level (default: 'info')
        """
        self._handler = handler
        self.level = level

    def __getattr__(self, name):
        def logme(*args):
            getattr(logging, self.level)('%s%r' % (name, args))
            getattr(self._handler, name)(*args)
        return logme
        

_NS_TL = 'http://psi.semagia.com/tolog-xml/'

# Elements which have never attributes and are simple containers for child elements
_SIMPLE_ELS = ('select', 'insert', 'update', 'delete', 'merge', 'predicate',
               'where', 'pagination', 'orderby', 'not', 'or', 'pair',
               'type', 'player', 'left', 'right', 'name', 'fragment')

# Elements which have a name attribute
_NAME_ELS = ('count', 'variable', 'parameter', 'ascending', 'descending')

# Elements which have a value attribute
_VALUE_ELS = ('string', 'iri', 'itemidentifier', 'subjectlocator',
              'identifier', 'integer', 'limit', 'offset',
              'objectid', 'date', 'datetime', 'integer', 'decimal')

# Prefix 'kind' to name mapping
_PREFIXKIND2NAME = {
    consts.SID: 'subject-identifier',
    consts.SLO: 'subject-locator',
    consts.IID: 'item-identifier',
    consts.MODULE: 'module',
}

class XMLParserHandler(ParserHandler):
    """\
    TologHandler which translates the events to XML.
    """
    def __init__(self, writer):
        """\

        `writer`
            An object which implements the methods of the ``tm.xmlutils.SimpleXMLWriter` class
        """
        self._writer = writer

    def start(self):
        writer = self._writer
        writer.startDocument()
        writer.startPrefixMapping(None, _NS_TL)
        writer.startElement('query')

    def end(self):
        writer = self._writer
        writer.pop()
        writer.endPrefixMapping(None)
        writer.endDocument()

    def __getattr__(self, name):
        if name.startswith('end'):
            return self._writer.pop
        n = name.lower()
        if n.startswith('start') and n[5:] in _SIMPLE_ELS:
            return lambda: self._writer.startElement(n[5:])
        elif n in _NAME_ELS:
            return lambda v: self._writer.emptyElement(n, {'name': v})
        elif n in _VALUE_ELS:
            return lambda v: self._writer.emptyElement(n, {'value': str(v)})
        raise AttributeError(name)

    def startBranch(self, short_circuit):
        attrs = {'short-circuit': 'true'} if short_circuit else None
        self._writer.startElement('branch', attrs)

    def startRule(self, name, variables):
        self._writer.startElement('rule', {'name': name})
        for v in variables:
            self.variable(v)
        self._writer.startElement('body')

    def endRule(self):
        self._writer.pop() # body
        self._writer.pop() # rule

    def literal(self, lit):
        value, datatype = lit
        self._writer.emptyElement('literal', {'value': value, 'datatype': datatype})

    def curie(self, kind, prefix, lp):
        self._writer.emptyElement('curie', {'kind': _PREFIXKIND2NAME[kind], 'prefix': prefix, 'localpart': lp})

    def qname(self, kind, prefix, lp):
        self._writer.emptyElement('qname', {'kind': _PREFIXKIND2NAME[kind], 'prefix': prefix, 'localpart': lp})

    def startBuiltinPredicate(self, name):
        self._writer.startElement('builtin-predicate', {'name': name})

    def startDynamicPredicate(self):
        self._writer.startElement('dynamic-predicate')

    def startAssociationPredicate(self):
        self._writer.startElement('association-predicate')

    def startFunction(self, name):
        self._writer.startElement('function-call', {'name': name})

    def startInfixPredicate(self, name):
        self._writer.startElement('infix-predicate', {'name': name})

    def fragmentContent(self, fragment):
        self._writer.dataElement('content', fragment)

    def base(self, iri):
        self._writer.emptyElement('base', {'iri': iri})

    def namespace(self, identifier, iri, kind):
        self._writer.emptyElement('namespace', {'identifier': identifier,
                                                 'iri': iri,
                                                 'kind': _PREFIXKIND2NAME[kind] # KeyError is intentional
                                                }
                                  )

