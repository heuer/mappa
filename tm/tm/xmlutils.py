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
from xml.sax.handler import ContentHandler
from xml.sax import SAXException
from xml.sax.saxutils import escape, quoteattr, XMLGenerator
from xml.sax.xmlreader import InputSource, AttributesImpl
try:
    from lxml import etree
except ImportError:
    try:
        from xml.etree import cElementTree as etree
    except ImportError:
        from xml.etree import ElementTree as etree


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
        self._out.write(unicode('<?xml version="1.0" encoding="%s" standalone="yes"?>' % self._encoding))
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


# Taken from lxml.sax (but modified); license: BSD
class ETreeContentHandler(ContentHandler):
    """\
    Build an ElementTree from SAX events.
    """
    def __init__(self, makeelement=None, makesubelement=None, makepi=None):
        self._root = None
        self._root_siblings = []
        self._element_stack = []
        self._default_ns = None
        self._ns_mapping = {None: [None]}
        self._new_mappings = {}
        if makeelement is None:
            makeelement = etree.Element
        self._makeelement = makeelement
        if makesubelement is None:
            makesubelement = etree.SubElement
        self._makesubelement = makesubelement
        if makepi is None:
            makepi = etree.ProcessingInstruction
        self._makepi = makepi

    def _get_etree(self):
        """\
        Contains the generated ElementTree after parsing is finished.
        """
        return etree.ElementTree(self._root)

    etree = property(_get_etree, doc=_get_etree.__doc__)

    def setDocumentLocator(self, locator):
        pass

    def startDocument(self):
        pass

    def endDocument(self):
        pass

    def startPrefixMapping(self, prefix, uri):
        self._new_mappings[prefix] = uri
        try:
            self._ns_mapping[prefix].append(uri)
        except KeyError:
            self._ns_mapping[prefix] = [uri]
        if prefix is None:
            self._default_ns = uri

    def endPrefixMapping(self, prefix):
        ns_uri_list = self._ns_mapping[prefix]
        ns_uri_list.pop()
        if prefix is None:
            self._default_ns = ns_uri_list[-1]

    def _buildTag(self, ns_name_tuple):
        ns_uri, local_name = ns_name_tuple
        if ns_uri:
            el_tag = "{%s}%s" % ns_name_tuple
        elif self._default_ns:
            el_tag = "{%s}%s" % (self._default_ns, local_name)
        else:
            el_tag = local_name
        return el_tag

    def startElementNS(self, ns_name, qname, attributes=None):
        el_name = self._buildTag(ns_name)
        if attributes:
            attrs = {}
            try:
                iter_attributes = attributes.iteritems()
            except AttributeError:
                iter_attributes = attributes.items()

            for name_tuple, value in iter_attributes:
                if name_tuple[0]:
                    attr_name = "{%s}%s" % name_tuple
                else:
                    attr_name = name_tuple[1]
                attrs[attr_name] = value
        else:
            attrs = None

        element_stack = self._element_stack
        if self._root is None:
            element = self._root = self._makeelement(el_name, attrs,
                                                     self._new_mappings)
            if self._root_siblings and hasattr(element, 'addprevious'):
                for sibling in self._root_siblings:
                    element.addprevious(sibling)
            del self._root_siblings[:]
        else:
            element = self._makesubelement(element_stack[-1], el_name, attrs,
                                           self._new_mappings)
        element_stack.append(element)
        self._new_mappings.clear()

    def processingInstruction(self, target, data):
        pi = self._makepi(target, data)
        if self._root is None:
            self._root_siblings.append(pi)
        else:
            self._element_stack[-1].append(pi)

    def endElementNS(self, ns_name, qname):
        element = self._element_stack.pop()
        el_tag = self._buildTag(ns_name)
        if el_tag != element.tag:
            raise SAXException("Unexpected element closed: " + el_tag)

    def startElement(self, name, attributes=None):
        if attributes:
            attributes = dict(
                    [((None, k), v) for k, v in attributes.items()]
                )
        self.startElementNS((None, name), name, attributes)

    def endElement(self, name):
        self.endElementNS((None, name), name)

    def characters(self, data):
        last_element = self._element_stack[-1]
        try:
            # if there already is a child element, we must append to its tail
            last_element = last_element[-1]
            last_element.tail = (last_element.tail or '') + data
        except IndexError:
            # otherwise: append to the text
            last_element.text = (last_element.text or '') + data

    ignorableWhitespace = characters


def _is_etree_handler(handler):
    return hasattr(handler, 'etree')

_EMPTY_ATTRS = {}


class SAXSimpleXMLWriter(object):
    """\
    SimpleXMLWriter which translates the events to SAX events
    """
    def __init__(self, handler):
        """\

        """
        self._handler = handler
        if _is_etree_handler(handler):
            setattr(self, 'startElement', self._startElementLXML)
        self._elements = []

    def __getattr__(self, name):
        return getattr(self._handler, name)

    def startElement(self, name, attrs=None):
        self._elements.append(name)
        self._handler.startElement(name, _EMPTY_ATTRS if not attrs else AttributesImpl(attrs))

    def _startElementLXML(self, name, attrs=None):
        self._elements.append(name)
        # lxml.sax.ElementTreeContentHandler and ETreeContentHandler handles attributes as dict, no need for AttributesImpl
        self._handler.startElement(name, attrs or _EMPTY_ATTRS)

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

    `writer`
        `XMLWriter` instance.
    """
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
