# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
XML Utilities.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
import codecs
from xml.sax.saxutils import escape, quoteattr, XMLGenerator
from xml.sax.xmlreader import InputSource


def as_inputsource(source):
    """\
    Converts a ``tm.mio.Source`` into a ``xml.sax.xmlreader.InputSource``
    """
    input_source = InputSource()
    input_source.setSystemId(source.iri)
    input_source.setByteStream(source.stream)
    input_source.setEncoding(source.encoding)
    return input_source


class XMLWriter(object):
    """\
    Simple SAX alike XML writer
    """
    __slots__ = ['_out', '_encoding', '_depth', 'prettify']
    
    def __init__(self, out, encoding='utf-8', prettify=False):
        """\

        `out`
            A file object
        `encoding`
            An encoding (default: UTF-8)
        `prettify`
            Indicates if the XML should be prettified (default: False)
        """
        self._out = codecs.getwriter(encoding)(out)
        self._encoding = encoding
        self._depth = 0
        self.prettify = prettify

    def startDocument(self):
        """\
        Writes the <?xml version="1.0" ... ?> declaration.
        """
        self._out.write(u'<?xml version="1.0" encoding="%s" standalone="yes"?>' % self._encoding)
        if not self.prettify:
            self._newline()
        self._depth = 0
    
    def endDocument(self):
        """\
        Flushes to the output.
        """
        self._newline()
        self._out.flush()
    
    def startElement(self, name, attrs=None):
        """\
        Writes a start tag with the optional attributes (a dict).
        """
        self._indent()
        self._out.write(u'<%s' % name)
        self._write_attributes(attrs)
        self._out.write(u'>')
        self._depth+=1
    
    def endElement(self, name, indent=True):
        """\
        Writes an end tag. 
        
        `name`
            The name of the tag.
        `indent`
            Indicating if whitespaces in front of the element are allowed.
        """
        self._depth-=1
        if indent:
            self._indent()
        self._out.write(u'</%s>' % name)
    
    def dataElement(self, name, data, attrs=None):
        """\
        Writes a start tag, the data and an end tag.
        """
        self.startElement(name, attrs)
        self.characters(data)
        self.endElement(name, False)

    def emptyElement(self, name, attrs=None):
        """\
        Writes ``<name att1="attr-val1" attr2="attr-val2"/>``
        """
        self._indent()
        out = self._out
        out.write(u'<%s' % name)
        self._write_attributes(attrs)
        out.write(u'/>')
    
    def characters(self, content):
        """\
        Writes an escaped value.
        """
        self._out.write(escape(content))

    def processingInstruction(self, target, data):
        """\
        Writes a processing instruction.
        """
        write = self._out.write
        write(u'<?')
        write(target)
        write(u' ')
        write(data)
        write(u'?>')

    def comment(self, comment):
        """\
        Writes a comment.
        """
        write = self._out.write
        self._indent()
        write(u'<!-- ')
        self.characters(comment.replace(u'--', u'- -'))
        write(u' -->')
        if not self.prettify:
            self._newline()

    def _write_attributes(self, attrs):
        """\
        Serializes the attributes (a ``dict`` or ``None``), if any.
        """
        if attrs:
            write = self._out.write
            for k, v in attrs.items():
                write(u' %s=%s' % (k, quoteattr(v)))

    def _indent(self):
        """\
        Indents a line.
        """
        if self.prettify:
            self._newline()
            self._out.write(u' ' * self._depth * 2)

    def _newline(self):
        """\
        Writes a newline character.
        """
        self._out.write(u'\n')


class SimpleXMLWriter(XMLWriter):
    """\
    XMLWriter which remembers the names of started elements and provides
    a simple `pop` method to close the last element.
    """
    def __init__(self, out, encoding='utf-8', prettify=False):
        """\

        `out`
            A file object
        `encoding`
            An encoding (default: UTF-8)
        `prettify`
            Indicates if the XML should be prettified (default: False)
        """
        super(SimpleXMLWriter, self).__init__(out, encoding=encoding, prettify=prettify)
        self._elements = []

    def startElement(self, name, attrs=None):
        super(SimpleXMLWriter, self).startElement(name, attrs)
        self._elements.append(name)

    def endElement(self, name, indent=True):
        super(SimpleXMLWriter, self).endElement(name, indent)
        self._elements.pop()

    def pop(self, indent=True):
        """\
        Closes the last started element.

        `indent`
            Indicating if whitespaces in front of the element are allowed.
        """
        self.endElement(self._elements[-1], indent)


try:
    import lxml.sax
    def is_lxml_handler(handler):
        return isinstance(handler, lxml.sax.ElementTreeContentHandler)
except ImportError:
    def is_lxml_handler(handler):
        return False

from xml.sax.xmlreader import AttributesImpl
_EMPTY_ATTRS = {}

class SAXSimpleXMLWriter(object):
    """\
    SimpleXMLWriter which translates the events to SAX events
    """
    def __init__(self, handler):
        """\

        """
        self._handler = handler
        if is_lxml_handler(handler):
            setattr(self, 'startElement', self._startElementLXML)
        self._elements = []

    def __getattr__(self, name):
        return getattr(self._handler, name)

    def startElement(self, name, attrs=None):
        self._elements.append(name)
        self._handler.startElement(name, _EMPTY_ATTRS if not attrs else AttributesImpl(attrs))

    def _startElementLXML(self, name, attrs=None):
        self._elements.append(name)
        self._handler.startElement(name, _EMPTY_ATTRS if not attrs else dict([((None, k), v) for k, v in attrs.items()]))

    def endElement(self, name):
        assert name == self._elements.pop()
        self._handler.endElement(name)

    def dataElement(self, name, data, attrs=None):
        """\
        Writes a start tag, the data and an end tag.
        """
        self.startElement(name, attrs)
        self.characters(data)
        self.endElement(name)

    def emptyElement(self, name, attrs=None):
        """\
        Writes ``<name att1="attr-val1" attr2="attr-val2"/>``
        """
        self.startElement(name, attrs)
        self.endElement(name)

    def pop(self, indent=True):
        """\
        Closes the last started element.

        `indent`
            Ignored
        """
        self.endElement(self._elements[-1])

    def processingInstruction(self, target, data):
        """\
        Writes a processing instruction.
        """
        self._handler.processingInstruction(target, data)

    def comment(self, comment):
        """\
        Writes a comment (unsupported).
        """


def xmlwriter_as_contenthandler(writer):
    """\
    Returns a ContentHandler which serializes the events.
    
    All events are serialized to the ``_out`` property of the `writer` using 
    the ``writer._encoding``.
    """
    # pylint: disable-msg=W0212
    return XMLGenerator(writer._out, writer._encoding)

#
# Taken from RDFLib <http://rdflib.net/>
# License: BSD
#
from unicodedata import category

NAME_START_CATEGORIES = ["Ll", "Lu", "Lo", "Lt", "Nl"]
NAME_CATEGORIES = NAME_START_CATEGORIES + ["Mc", "Me", "Mn", "Lm", "Nd"]
ALLOWED_NAME_CHARS = [u"\u00B7", u"\u0387", u"-", u".", u"_"]

#
# http://www.w3.org/TR/REC-xml-names/#NT-NCName
#  [4] NCName ::= (Letter | '_') (NCNameChar)* /* An XML Name, minus
#      the ":" */
#  [5] NCNameChar ::= Letter | Digit | '.' | '-' | '_' | CombiningChar
#      | Extender

def is_ncname(name):
    first = name[0]
    if first == '_' or category(first) in NAME_START_CATEGORIES:
        for i in xrange(1, len(name)):
            c = name[i]
            if not category(c) in NAME_CATEGORIES:
                if c in ALLOWED_NAME_CHARS:
                    continue
                return False
        return True
    return False

import sys
if sys.platform[:4] == 'java':
    # Jython's SAX implementation behaves differently from CPython. The Java
    # SAX parsers expect an empty string not ``None`` for the namespace
    # This work-around lets Jython accept "attrs.get((None, 'myattr')) instead
    # of "attrs.get(('', 'myattr'))
    # Fixed in Jython >= 2.5.2b1
    from xml.sax.drivers2.drv_javasax import AttributesNSImpl #pylint: disable-msg=E0611, F0401
    class AttrsImpl(AttributesNSImpl):
        def __init__(self, attrs):
            AttributesNSImpl.__init__(self, attrs._attrs) #pylint: disable-msg=W0212
        def getValue(self, name):
            return AttributesNSImpl.getValue(self, (name[0] or '', name[1]))
    def attributes(attrs):
        """\
        Returns an AttributesNS implementation which accepts ``None`` for the
        non-existent namespace IRI, i.e. ``getValue((None, 'myattr'))``
        """
        return AttrsImpl(attrs)
else:
    def attributes(attrs):
        """\
        Returns the attributes unmodified
        """
        return attrs
del sys
