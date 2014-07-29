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
from __future__ import absolute_import
import logging
from . import consts
from xml.sax import ContentHandler


class TologHandler(object):
    """\
    Common superclass of tolog handlers.
    """


class NoopParserHandler(TologHandler):
    """\
    A ParserHandler which does nothing.
    """
    def __getattr__(self, name):
        def noop(*args, **kw): pass
        return noop


class LoggingParserHandler(TologHandler):
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
_SIMPLE_ELS = (u'select', u'insert', u'update', u'delete', u'merge',
               u'predicate', u'where', u'pagination', u'orderby', u'not', u'or',
               u'pair', u'type', u'player', u'left', u'right', u'name',
               u'fragment')

# Elements which have a name attribute
_NAME_ELS = (u'count', u'variable', u'parameter', u'ascending', u'descending')

# Elements which have a value attribute
_VALUE_ELS = (u'string', u'iri', u'itemidentifier', u'subjectlocator',
              u'identifier', u'integer', u'limit', u'offset',
              u'objectid', u'date', u'datetime', u'integer', u'decimal')

# Elements/events which do not have an "end..." event
_NO_END_EVENT_ELS = _NAME_ELS + _VALUE_ELS + \
                    (u'base', u'namespace', u'curie', u'qname',
                     # 'body' has also no start event since it is used to
                     # distinguish the rule header from the rule body and
                     # <body> issues the startRule event
                     u'body')

# Prefix 'kind' to name mapping
_PREFIXKIND2NAME = {
    consts.SID: u'subject-identifier',
    consts.SLO: u'subject-locator',
    consts.IID: u'item-identifier',
    consts.MODULE: u'module',
}

_PREFIXNAME2KIND = {v:k for k, v in _PREFIXKIND2NAME.items()}

_NAME_ATTR = (None, u'name')
_VALUE_ATTR = (None, u'value')
_KIND_ATTR = (None, u'kind')
_COST_ATTR = (None, u'cost')
_HINT_ATTR = (None, u'hint')


class XMLParserHandler(TologHandler):
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
        self._writer.pop()  # body
        self._writer.pop()  # rule

    def literal(self, value, datatype_iri=None, datatype_prefix=None, datatype_lp=None):
        attrs = {}
        if datatype_iri:
            attrs[u'datatype-iri'] = datatype_iri
        else:
            attrs[u'datatype-prefix'] = datatype_prefix
            attrs[u'datatype-localpart'] = datatype_lp
        self._writer.dataElement(u'literal', value, attrs)

    def curie(self, kind, prefix, lp):
        self._writer.emptyElement(u'curie', {u'kind': _PREFIXKIND2NAME[kind],
                                             u'prefix': prefix,
                                             u'localpart': lp})

    def qname(self, kind, prefix, lp):
        self._writer.emptyElement(u'qname', {u'kind': _PREFIXKIND2NAME[kind],
                                             u'prefix': prefix,
                                             u'localpart': lp})

    def startPredicate(self, costs=None):
        attrs = {}
        if costs is not None:
            attrs[u'cost'] = costs
        self._writer.startElement(u'predicate', attrs)

    def startBuiltinPredicate(self, name, costs=None, hints=None):
        attrs = {u'name': name}
        if costs is not None:
            attrs[u'cost'] = costs
        if hints is not None:
            attrs[u'hint'] = u' '.join(hints)
        self._writer.startElement(u'builtin-predicate', attrs)

    def startInternalPredicate(self, name, removed_variables, costs=None, hints=None):
        attrs = {u'name': name,
                 u'removed-variables': u' '.join(removed_variables)}
        if costs is not None:
            attrs[u'cost'] = costs
        if hints is not None:
            attrs[u'hint'] = u' '.join(hints)
        self._writer.startElement(u'internal-predicate', attrs)

    def startDynamicPredicate(self, costs=None):
        attrs = None
        if costs is not None:
            attrs = {u'cost': costs}
        self._writer.startElement(u'dynamic-predicate', attrs)

    def startAssociationPredicate(self, costs=None):
        attrs = None
        if costs is not None:
            attrs = {u'cost': costs}
        self._writer.startElement(u'association-predicate', attrs)

    def startFunction(self, name, costs=None):
        attrs = {u'name': name}
        if costs is not None:
            attrs[u'cost'] = costs
        self._writer.startElement(u'function-call', attrs)

    def startInfixPredicate(self, name, costs=None):
        attrs = {u'name': name}
        if costs is not None:
            attrs[u'cost'] = costs
        self._writer.startElement(u'infix-predicate', attrs)

    def fragmentContent(self, fragment):
        self._writer.dataElement(u'content', fragment)

    def base(self, iri):
        self._writer.emptyElement(u'base', {u'iri': iri})

    def namespace(self, identifier, iri, kind):
        self._writer.emptyElement(u'namespace',
                                  {u'identifier': identifier,
                                   u'iri': iri,
                                   # KeyError is intentional
                                   u'kind': _PREFIXKIND2NAME[kind]
                                   })


class SAXMediator(ContentHandler):
    """\
    Translates SAX events to `ITologHandler` events.
    """
    def __init__(self, handler):
        """\

        `handler`
            `ITologHandler` instance.
        """
        ContentHandler.__init__(self)
        self._handler = handler
        self._states = []
        self._rule_name = None
        self._rule_params = []

    def startElementNS(self, (uri, name), qname, attrs):
        handler = self._handler
        if name == u'tolog':
            handler.start()
            return
        if name == u'rule':
            self._rule_name = attrs.get(_NAME_ATTR)
            self._states.append(u'Rule')
            return
        if name == u'body':
            handler.startRule(self._rule_name, self._rule_params)
            self._rule_name, self._rule_params = None, []
            return
        args = ()
        evt = None
        method = None
        if name in _SIMPLE_ELS:
            evt = name.title()
        elif name == u'builtin-predicate':
            args = [attrs.get(_NAME_ATTR)]
            evt = u'BuiltinPredicate'
        elif name == u'internal-predicate':
            args = [attrs.get(_NAME_ATTR)]
            evt = u'InternalPredicate'
            args.append(attrs.get((None, u'removed-variables')).split())
        elif name == u'dynamic-predicate':
            evt = u'DynamicPredicate'
        elif name == u'association-predicate':
            evt = u'AssociationPredicate'
        elif name in _NAME_ELS:
            var_name = attrs.get(_NAME_ATTR)
            if name == u'variable' and self._states[-1] == u'Rule':
                # Don't emit events, collect variables
                self._rule_params.append(var_name)
                return
            args = [var_name]
            method = getattr(handler, name)
        elif name in _VALUE_ELS:
            args = [attrs.get(_VALUE_ATTR)]
            method = getattr(handler, name)
        elif name == u'namespace':
            args = [attrs.get((None, u'identifier')), attrs.get((None, u'iri')),
                    _PREFIXNAME2KIND[attrs.get(_KIND_ATTR)]]
            method = getattr(handler, name)
        elif name in (u'curie', u'qname'):
            args = [_PREFIXNAME2KIND[attrs.get(_KIND_ATTR)],
                    attrs.get((None, u'prefix')), attrs.get((None, u'localpart'))]
            method = getattr(handler, name)
        elif name == u'branch':
            args = [attrs.get((None, u'short-circuit')) == u'true']
            evt = u'Branch'
        elif name == u'infix-predicate':
            args = [attrs.get(_NAME_ATTR)]
            evt = u'InfixPredicate'
        elif name == u'function-call':
            args = [attrs.get(_NAME_ATTR)]
            evt = u'Function'
        kw = {}
        costs, hints = attrs.get(_COST_ATTR), attrs.get(_HINT_ATTR)
        if costs:
            kw['costs'] = costs
        if hints:
            kw['hints'] = hints.split()
        if not method:
            method = getattr(handler, u'start%s' % evt)
            self._states.append(evt)
        method(*args, **kw)

    def endElementNS(self, (uri, name), qname):
        if name in _NO_END_EVENT_ELS:
            return
        if name == u'tolog':
            self._handler.end()
            return
        state = self._states.pop()
        getattr(self._handler, u'end%s' % state)()
