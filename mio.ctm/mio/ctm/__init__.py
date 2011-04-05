# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2011 -- Lars Heuer - Semagia <http://www.semagia.com/>.
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
#     * Neither the project name nor the names of the contributors may be 
#       used to endorse or promote products derived from this software 
#       without specific prior written permission.
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
Compact Topic Maps Syntax (CTM) 1.0.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
import re
from StringIO import StringIO
import codecs
from urllib import urlopen
from tm.mio import MIOException
from tm.mio.deserializer import Deserializer, Context
from tm import plyutils
# pylint: disable-msg=E0611
from .environment import Environment 
from .contenthandler import MainContentHandler
from .miohandler import CTMHandler

__all__ = ['create_deserializer', 'CTMHandler']

def create_deserializer(version=1.0, context=None, included_by=None, **kw): # pylint: disable-msg=W0613
    """\
    
    """
    if not version in (None, 1.0):
        raise MIOException('Unsupported version "%s"' % version)
    return CTMDeserializer(context=context, included_by=included_by, **kw)

_ENCODING = re.compile(r'^%encoding\s*"([^"]+)"', re.UNICODE).match

class CTMDeserializer(Deserializer):
    """\
    
    """
    
    version = '1.0'
    
    def __init__(self, context=None, included_by=None, wildcardcounter=0, **kw):
        """\
        
        `context`
            The context
        `included_by`
            A set of IRIs indicating the files this CTM source was included from.
        """
        super(CTMDeserializer, self).__init__()
        self.context = context or Context()
        self._included_by = included_by
        self.environment = None
        self._wildcard_counter = wildcardcounter

    def _do_parse(self, source):
        """\
        
        """
        # pylint: disable-msg=E0611, F0401
        from mio.ctm import lexer
        from mio.ctm import parser
        parser = plyutils.make_parser(parser)
        env = Environment(handler=self.handler, iri=source.iri,
                          subordinate=self.subordinate, included_by=self._included_by,
                          context=self.context, wildcard_counter=self._wildcard_counter)
        parser.content_handler = MainContentHandler(env)
        self.environment = env
        data = source.stream
        if not data:
            try:
                data = urlopen(source.iri)
            except IOError:
                raise MIOException('Cannot read from "%s"' % source.iri)
        parser.parse(self._reader(data, source.encoding), lexer=plyutils.make_lexer(lexer))
        self.wildcard_counter = self.environment.wildcard_counter

    def _reader(self, fileobj, encoding=None):
        found_bom = False
        encoding = encoding or 'utf-8'
        line = fileobj.readline()
        if line.startswith(codecs.BOM_UTF8):
            found_bom = True
            encoding = 'utf-8'
            line = line[3:] # Skip BOM
        m = _ENCODING(line)
        if m:
            encoding = m.group(1)
            if found_bom and encoding.lower() != 'utf-8':
                raise MIOException('Found BOM, but encoding directive declares "%s"' % encoding)
        return codecs.getreader(encoding)(StringIO(''.join([line, fileobj.read()]))).read()
