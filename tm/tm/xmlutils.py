# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2010 -- Lars Heuer - Semagia <http://www.semagia.com/>.
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
XML Utilities.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:version:      $Rev: 279 $ - $Date: 2009-11-29 18:35:34 +0100 (So, 29 Nov 2009) $
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
        
        """
        self._out = codecs.getwriter(encoding)(out)
        self._encoding = encoding
        self._depth = 0
        self.prettify = prettify

    def startDocument(self):
        """\
        Writes the <?xml version="1.0" ... ?> declaration.
        """
        self._out.write('<?xml version="1.0" encoding="%s" standalone="yes"?>' % self._encoding)
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
        self._out.write('<%s' % name)
        self._write_attributes(attrs)
        self._out.write('>')
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
        self._out.write('</%s>' % name)
    
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
        out.write('<%s' % name)
        self._write_attributes(attrs)
        out.write('/>')
    
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
        write('<?')
        write(target)
        write(' ')
        write(data)
        write('?>')

    def comment(self, comment):
        """\
        Writes a comment.
        """
        write = self._out.write
        self._indent()
        write('<!-- ')
        self.characters(comment)
        write(' -->')
        if not self.prettify:
            self._newline()

    def _write_attributes(self, attrs):
        """\
        Serializes the attributes (a ``dict`` or ``None``), if any.
        """
        if attrs:
            write = self._out.write
            for k, v in attrs.items():
                write(' %s=%s' % (k, quoteattr(v)))

    def _indent(self):
        """\
        Indents a line.
        """
        if self.prettify:
            self._newline()
            self._out.write(' ' * self._depth * 2)

    def _newline(self):
        """\
        Writes a newline character.
        """
        self._out.write('\n')


def xmlwriter_as_contenthandler(writer):
    """\
    Returns a ContentHandler which serializes the events.
    
    All events are serialized to the ``_out`` property of the `writer` using 
    the ``writer._encoding``.
    """
    # pylint: disable-msg=W0212
    return XMLGenerator(writer._out, writer._encoding)

import sys
if sys.platform[:4] == 'java':
    # Jython's SAX implementation behaves differently from CPython. The Java
    # SAX parsers expect an empty string not ``None`` for the namespace
    # This work-around lets Jython accept "attrs.get((None, 'myattr')) instead
    # of "attrs.get(('', 'myattr'))
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
