# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
Tests against the ``xmlutils`` module.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
from nose.tools import ok_
from StringIO import StringIO
from xml.sax import saxutils
from tm import xmlutils


def test_simplesaxhandler():
    h = xmlutils.ETreeContentHandler()
    ok_(h.etree is None)
    handler = xmlutils.SAXSimpleXMLWriter(h)
    handler.startDocument()
    handler.startElement('xml')
    handler.startElement('a')
    handler.characters('b')
    handler.endElement('a')
    handler.startElement('c', {'d': 'e'})
    handler.pop()
    handler.emptyElement('f')
    handler.dataElement('g', 'h')
    handler.dataElement('i', 'j', {'k': 'l'})
    handler.endElement('xml')
    handler.endDocument()
    ok_(h.etree is not None)


def test_simplesaxhandler2():
    out = StringIO()
    h = saxutils.XMLGenerator(out)
    handler = xmlutils.SAXSimpleXMLWriter(h)
    handler.startDocument()
    handler.startElement('xml')
    handler.startElement('a')
    handler.characters('b')
    handler.endElement('a')
    handler.startElement('c', {'d': 'e'})
    handler.pop()
    handler.emptyElement('f')
    handler.dataElement('g', 'h')
    handler.dataElement('i', 'j', {'k': 'l'})
    handler.endElement('xml')
    handler.endDocument()
    

if __name__ == '__main__':
    import nose
    nose.core.runmodule()
