# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
`TM/XML <http://www.ontopia.net/topicmaps/tmxml.html>`_ topic maps support.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
import xml.sax.handler as sax_handler
import xml.sax as sax
from tm.mio.deserializer import Deserializer
from tm.xmlutils import as_inputsource
from .handler import TMXMLContentHandler

__all__ = ['create_deserializer']


def create_deserializer():
    """\
    Creates and returns a deserializer that is able to parse
    `TM/XML <http://www.ontopia.net/topicmaps/tmxml.html>`_ topic maps.
    """
    return TMXMLDeserializer()


class TMXMLDeserializer(Deserializer):
    """\
    Deserializer for TM/XML topic maps.
    """
    def __init__(self):
        super(TMXMLDeserializer, self).__init__()

    def _do_parse(self, source):
        """\
        
        """
        content_handler = TMXMLContentHandler()
        content_handler.map_handler = self.handler
        content_handler.doc_iri = source.iri
        parser = sax.make_parser()
        parser.setFeature(sax.handler.feature_namespaces, True)
        parser.setContentHandler(content_handler)
        parser.parse(as_inputsource(source))
