# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2009 -- Lars Heuer - Semagia <http://www.semagia.com/>.
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
Provides deserialization of XML 1.0/2.0/2.1 topic maps.

Port of the Java ``com.semagio.mio.xtm`` package to Python.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:version:      $Rev: 372 $ - $Date: 2010-05-09 18:27:41 +0200 (So, 09 Mai 2010) $
:license:      BSD license
"""
import xml.sax.handler as sax_handler
import xml.sax as sax
from tm.mio.deserializer import Deserializer, Context
from tm.xmlutils import as_inputsource, attributes
from xtm1 import XTM10ContentHandler, NS_XTM as NS_XTM_10
from xtm2 import XTM2ContentHandler, NS_XTM as NS_XTM_2
from miohandler import XTM21Handler

__all__ = ['create_deserializer', 'XTM21Handler']

_CONTENT_HANDLERS = {'1.0': XTM10ContentHandler,
                     '2.0': XTM2ContentHandler,
                     '2.1': XTM2ContentHandler
                     }

def create_deserializer(**kw):
    return XTMDeserializer(version=kw.get('version'), strict=kw.get('strict', True))


class XTMDeserializer(Deserializer):
    """\
    Generic XTM deserializer that supports XTM 1.0, XTM 2.0 and 2.1.
    """
    def __init__(self, version=None, strict=True):
        super(XTMDeserializer, self).__init__()
        self._version = version
        self._strict = strict

    @property        
    def version(self):
        if not self._version:
            raise AttributeError('The version information is not available yet')
        return self._version

    def _do_parse(self, source):
        """\
        
        """
        content_handler = _CONTENT_HANDLERS.get(self._version, XTMContentHandler)()
        content_handler.strict = self._strict
        content_handler.map_handler = self.handler
        content_handler.doc_iri = source.iri
        content_handler.subordinate = self.subordinate
        content_handler.context = self.context
        parser = sax.make_parser()
        parser.setFeature(sax.handler.feature_namespaces, True)
        parser.setContentHandler(content_handler)
        parser.parse(as_inputsource(source))
        self._version = self._version or content_handler.version


class XTMContentHandler(sax_handler.ContentHandler):
    """\
    Content handler that can handle XTM 1.0 and XTM 2.0 / 2.1 topic maps.
    """
    def __init__(self):
        sax_handler.ContentHandler.__init__(self)
        self._content_handler = None
        self.map_handler = None
        self.subordinate = False
        self.doc_iri = None
        self.context = Context()
        self.version = None
        self.strict = True
    
    def startElementNS(self, name, qname, attrs):
        if not self._content_handler:
            self._content_handler = self._create_content_handler(name, qname, attrs)
        self._content_handler.startElementNS(name, qname, attrs)

    def endElementNS(self, name, qname):
        self._content_handler.endElementNS(name, qname)

    def characters(self, content):
        self._content_handler.characters(content)
        
    def _create_content_handler(self, (uri, name), qname, attrs): #pylint: disable-msg=W0613
        attrs = attributes(attrs)
        if uri == NS_XTM_2:
            handler = XTM2ContentHandler(self.map_handler)
            self.version = attrs.get((None, 'version'))
        elif uri == NS_XTM_10:
            handler = XTM10ContentHandler(self.map_handler)
            self.version = '1.0'
        elif attrs.get((None, 'version')) in ('2.0', '2.1'):
            handler = XTM2ContentHandler(self.map_handler)
            self.version = attrs.get((None, 'version'))
        else:
            handler = XTM10ContentHandler(self.map_handler)
            self.version = '1.0'
        # Provide missing info
        handler.map_handler = self.map_handler
        handler.strict = self.strict
        handler.subordinate = self.subordinate
        handler.doc_iri = self.doc_iri
        handler.context= self.context
        # Provide the missing event
        handler.startDocument()
        return handler
