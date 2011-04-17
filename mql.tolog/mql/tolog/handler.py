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
from tm.xmlutils import SimpleXMLWriter

class TologHandler(object):
    """\
    Common superclass of tolog handlers.
    """
    pass

class NoopHandler(TologHandler):
    """\
    A TologHandler which does nothing.
    """
    def __getattr__(self, name):
        def noop(*args): pass
        return noop

class LoggingHandler(TologHandler):
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
              'identifier', 'integer', 'limit', 'offset', 'qname',
              'objectid', 'date', 'datetime', 'integer', 'decimal')

# Namespace 'kind' to name mapping
_NSKIND2NAME = {
    consts.SID: 'subject-identifier',
    consts.SLO: 'subject-locator',
    consts.IID: 'item-identifier',
}

class XMLHandler(TologHandler):
    """\
    TologHandler which translates the events to XML.
    """
    def __init__(self, out, encoding='utf-8', prettify=False):
        """\

        `out`
            File-like object
        `encoding`
            The encoding (default: utf-8)
        `prettify`
            Indicates if the XML should be prettified (default: False)
        """
        self._writer = SimpleXMLWriter(out, encoding=encoding, prettify=prettify)

    def start(self):
        writer = self._writer
        writer.startDocument()
        writer.startElement('query', {'xmlns': _NS_TL})

    def end(self):
        writer = self._writer
        writer.pop()
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

    def startBuiltinPredicate(self, name):
        self._writer.startElement('builtin-predicate', {'name': name})

    def startAssociationPredicate(self):
        self._writer.startElement('association-predicate')

    def startFunction(self, name):
        self._writer.startElement('function', {'name': name})

    def startComparison(self, name):
        self._writer.startElement('comparison', {'name': name})

    def fragmentContent(self, fragment):
        self._writer.dataElement('content', fragment)

    def namespace(self, identifier, iri, kind=None):
        attrs = {'identifier': identifier, 'iri': iri}
        if kind:
            kind_name = _NSKIND2NAME[kind] # KeyError is intentional
            attrs.update({'kind': kind_name})
        self._writer.emptyElement('namespace', attrs)

