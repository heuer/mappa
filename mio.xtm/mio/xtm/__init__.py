# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
Provides deserialization of XML 1.0/2.0/2.1 topic maps.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
import xml.sax.handler as sax_handler
import xml.sax as sax
from tm.mio.deserializer import Deserializer, Context
from tm.xmlutils import as_inputsource
from mio.xtm.xtm1 import XTM10ContentHandler, NS_XTM as NS_XTM_10
from mio.xtm.xtm2 import XTM2ContentHandler, NS_XTM as NS_XTM_2
from mio.xtm.miohandler import XTM21Handler

__all__ = ['create_deserializer', 'XTM21Handler']

_CONTENT_HANDLERS = {u'1.0': XTM10ContentHandler,
                     u'2.0': XTM2ContentHandler,
                     u'2.1': XTM2ContentHandler
                     }


def create_deserializer(version=None, strict=True, **kw):
    return XTMDeserializer(version=version)


class XTMDeserializer(Deserializer):
    """\
    Generic XTM deserializer that supports XTM 1.0, XTM 2.0 and 2.1.
    """
    def __init__(self, version=None):
        super(XTMDeserializer, self).__init__()
        self._version = version

    @property        
    def version(self):
        if not self._version:
            raise AttributeError('The version information is not available yet')
        return self._version

    def _do_parse(self, source):
        """\
        
        """
        content_handler = _CONTENT_HANDLERS.get(self._version, XTMContentHandler)()
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
    Content handler that can handle XTM 1.0 and XTM 2.0/2.1 topic maps.
    """
    def __init__(self):
        sax_handler.ContentHandler.__init__(self)
        self._content_handler = None
        self.map_handler = None
        self.subordinate = False
        self.doc_iri = None
        self.context = Context()
        self.version = None

    def startElementNS(self, name, qname, attrs):
        if not self._content_handler:
            self._content_handler = self._create_content_handler(name, qname, attrs)
        self._content_handler.startElementNS(name, qname, attrs)

    def endElementNS(self, name, qname):
        self._content_handler.endElementNS(name, qname)

    def characters(self, content):
        self._content_handler.characters(content)
        
    def _create_content_handler(self, (uri, name), qname, attrs): #pylint: disable-msg=W0613
        if uri == NS_XTM_2:
            handler = XTM2ContentHandler(self.map_handler)
            self.version = attrs.get((None, u'version'))
        elif uri == NS_XTM_10:
            handler = XTM10ContentHandler(self.map_handler)
            self.version = u'1.0'
        elif attrs.get((None, u'version')) in (u'2.0', u'2.1'):
            handler = XTM2ContentHandler(self.map_handler)
            self.version = attrs.get((None, u'version'))
        else:
            handler = XTM10ContentHandler(self.map_handler)
            self.version = u'1.0'
        # Provide missing info
        handler.map_handler = self.map_handler
        handler.subordinate = self.subordinate
        handler.doc_iri = self.doc_iri
        handler.context= self.context
        # Provide the missing event
        handler.startDocument()
        return handler
