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
`TM/XML <http://www.ontopia.net/topicmaps/tmxml.html>`_ topic maps support.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:version:      $Rev: 169 $ - $Date: 2009-06-26 14:44:17 +0200 (Fr, 26 Jun 2009) $
:license:      BSD license
"""
import xml.sax.handler as sax_handler
import xml.sax as sax
from tm.mio.deserializer import Deserializer
from tm.xmlutils import as_inputsource

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
        from mio.tmxml.handler import TMXMLContentHandler
        content_handler = TMXMLContentHandler()
        content_handler.map_handler = self.handler
        content_handler.doc_iri = source.iri
        parser = sax.make_parser()
        parser.setFeature(sax.handler.feature_namespaces, True)
        parser.setContentHandler(content_handler)
        parser.parse(as_inputsource(source))
