# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
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
    A ParserHandler which does nothing.
    """
    def __getattr__(self, name):
        def noop(*args, **kw): pass
        return noop


class LoggingParserHandler(ParserHandler):
    """\
    A ParserHandler which loggs all events and delegates the events to
    an underlying ParserHandler instance.
    """
    def __init__(self, handler, level=logging.INFO):
        """\
        `handler`
            The ParserHandler instance which should receive the events.
        `level`
            The logging level (default: logging.INFO)
        """
        self._handler = handler
        self._logging_function = None
        self.level = level

    def _set_level(self, level):
        self._level = level
        self._logging_function = getattr(logging, logging.getLevelName(level).lower())

    def __getattr__(self, name):
        def logme(*args, **kw):
            self._logging_function('%s %r %r' % (name, args, kw))
            getattr(self._handler, name)(*args, **kw)
        return logme

    level = property(lambda self: self._level, _set_level)
        

_NS_TL = u'http://psi.semagia.com/tolog-xml/'

# Elements which have never attributes and are simple containers for child elements
_SIMPLE_ELS = (u'select', u'insert', u'update', u'delete', u'merge', u'predicate',
               u'where', u'pagination', u'orderby', u'not', u'or', u'pair',
               u'type', u'player', u'left', u'right', u'name', u'fragment')

# Elements which have a name attribute
_NAME_ELS = (u'count', u'variable', u'parameter', u'ascending', u'descending')

# Elements which have a value attribute
_VALUE_ELS = (u'string', u'iri', u'itemidentifier', u'subjectlocator',
              u'identifier', u'integer', u'limit', u'offset',
              u'objectid', u'date', u'datetime', u'integer', u'decimal')

# Prefix 'kind' to name mapping
_PREFIXKIND2NAME = {
    consts.SID: u'subject-identifier',
    consts.SLO: u'subject-locator',
    consts.IID: u'item-identifier',
    consts.MODULE: u'module',
}


class XMLParserHandler(ParserHandler):
    """\
    ParserHandler which translates the events to XML.
    """
    def __init__(self, writer):
        """\

        `writer`
            An object which implements the methods of the
            ``tm.xmlutils.SimpleXMLWriter` class
        """
        self._writer = writer

    def start(self):
        writer = self._writer
        writer.startDocument()
        writer.startPrefixMapping(None, _NS_TL)
        writer.startElement(u'tolog')

    def end(self):
        writer = self._writer
        writer.pop()
        writer.endPrefixMapping(None)
        writer.endDocument()

    def __getattr__(self, name):
        if name.startswith(u'end'):
            return self._writer.pop
        n = name.lower()
        if n.startswith(u'start') and n[5:] in _SIMPLE_ELS:
            return lambda: self._writer.startElement(n[5:])
        elif n in _NAME_ELS:
            return lambda v: self._writer.emptyElement(n, {u'name': v})
        elif n in _VALUE_ELS:
            return lambda v: self._writer.emptyElement(n, {u'value': str(v)})
        raise AttributeError(name)

    def startBranch(self, short_circuit):
        attrs = {u'short-circuit': u'true'} if short_circuit else None
        self._writer.startElement(u'branch', attrs)

    def startRule(self, name, variables):
        self._writer.startElement(u'rule', {u'name': name})
        for v in variables:
            self.variable(v)
        self._writer.startElement(u'body')

    def endRule(self):
        self._writer.pop() # body
        self._writer.pop() # rule

    def literal(self, value, datatype_iri=None, datatype_prefix=None, datatype_lp=None):
        attrs = {u'value': value}
        if datatype_iri:
            attrs[u'datatype-iri'] = datatype_iri
        else:
            attrs[u'datatype-prefix'] = datatype_prefix
            attrs[u'datatype-localpart'] = datatype_lp
        self._writer.emptyElement(u'literal', attrs)

    def curie(self, kind, prefix, lp):
        self._writer.emptyElement(u'curie', {u'kind': _PREFIXKIND2NAME[kind],
                                             u'prefix': prefix,
                                             u'localpart': lp})

    def qname(self, kind, prefix, lp):
        self._writer.emptyElement(u'qname', {u'kind': _PREFIXKIND2NAME[kind],
                                             u'prefix': prefix,
                                             u'localpart': lp})

    def startBuiltinPredicate(self, name):
        self._writer.startElement(u'builtin-predicate', {u'name': name})

    def startDynamicPredicate(self):
        self._writer.startElement(u'dynamic-predicate')

    def startAssociationPredicate(self):
        self._writer.startElement(u'association-predicate')

    def startFunction(self, name):
        self._writer.startElement(u'function-call', {u'name': name})

    def startInfixPredicate(self, name):
        self._writer.startElement(u'infix-predicate', {u'name': name})

    def fragmentContent(self, fragment):
        self._writer.dataElement(u'content', fragment)

    def base(self, iri):
        self._writer.emptyElement(u'base', {u'iri': iri})

    def namespace(self, identifier, iri, kind):
        self._writer.emptyElement(u'namespace', {u'identifier': identifier,
                                                 u'iri': iri,
                                                 u'kind': _PREFIXKIND2NAME[kind] # KeyError is intentional
                                                 }
                                  )

