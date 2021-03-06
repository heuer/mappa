# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
Linear Topic Maps Notation (LTM) 1.3.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
from __future__ import absolute_import
import re
import io
import codecs
from urllib import urlopen
from tm.mio import MIOException
from tm.mio.deserializer import Deserializer, Context
from tm import plyutils
from .runtime import LTMContext
from . import lexer as lexer_mod, parser as parser_mod

__all__ = ['create_deserializer']


def create_deserializer(legacy=False, **kw):
    """\
    
    """
    return LTMDeserializer(legacy=legacy)

_ENCODING = re.compile(r'^@"([^"]+)"').match

class LTMDeserializer(Deserializer):
    """\
    
    """
    
    version = u'1.3'
    
    def __init__(self, legacy=False, context=None, included_by=None):
        """\
        
        `legacy`
            Indicates if the parser should add an item identifier and subject 
            identifier iff a topic reifies a construct. (default: ``False``)
        `context`
            The context
        `included_by`
            A set of IRIs indicating the files this LTM source was included from.
        """
        super(LTMDeserializer, self).__init__()
        self.legacy = legacy
        self._context = context or Context()
        self._included_by = included_by or set()

    def _do_parse(self, source):
        """\
        
        """
        parser = plyutils.make_parser(parser_mod)
        parser.context = LTMContext(handler=self.handler, 
                                    iri=source.iri, 
                                    subordinate=self.subordinate, 
                                    legacy=self.legacy,
                                    included_by = self._included_by,
                                    context=self._context)
        data = source.stream
        if not data:
            try:
                data = urlopen(source.iri)
            except IOError:
                raise MIOException('Cannot read from ' + source.iri)
        parser.parse(self._reader(data, source.encoding), lexer=_make_lexer())

    def _reader(self, fileobj, encoding=None):
        found_bom = False
        encoding = encoding or 'iso-8859-1'
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
        return codecs.getreader(encoding)(io.BytesIO(''.join([line, fileobj.read()]))).read()


def _make_lexer():
    return plyutils.make_lexer(lexer_mod)


def _make_parser(debug=False):
    return plyutils.make_parser(parser_mod, debug=debug)
