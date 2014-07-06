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
from StringIO import StringIO
from xml.sax import saxutils
import lxml
import lxml.sax
from tm import xmlutils


def test_simplesaxhandler():
    h = lxml.sax.ElementTreeContentHandler()
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
