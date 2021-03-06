# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
Compact Topic Maps Syntax (CTM) 1.0.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
import re
import io
import codecs
from urllib import urlopen
from tm.mio import MIOException
from tm.mio.deserializer import Deserializer, Context
from tm import plyutils
from .environment import Environment
from .contenthandler import MainContentHandler
from .miohandler import CTMHandler
from . import lexer as lexer_mod, parser as parser_mod

__all__ = ['create_deserializer', 'CTMHandler']


def create_deserializer(version=1.0, context=None, included_by=None, **kw): # pylint: disable-msg=W0613
    """\
    
    """
    if not version in (None, 1.0):
        raise MIOException('Unsupported version "%s"' % version)
    return CTMDeserializer(context=context, included_by=included_by, **kw)


def _make_parser():
    return plyutils.make_parser(parser_mod)


def _make_lexer():
    return plyutils.make_lexer(lexer_mod)


_ENCODING = re.compile(ur'^%encoding\s*"([^"]+)"').match


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
        parser = _make_parser()
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
        parser.parse(self._reader(data, source.encoding), lexer=_make_lexer())
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
        return codecs.getreader(encoding)(io.BytesIO(''.join([line, fileobj.read()]))).read()
