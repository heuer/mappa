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
Provides constants for commonly known syntaxes and discovery of syntaxes.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
try:
    from operator import itemgetter
except ImportError: # Python < 2.4
    def itemgetter(item):
        return lambda x: x[item]

_SYNTAXES = {}

class Syntax(tuple):
    """\
    Immutable class which holds syntax properties.
    
    Using one of the constants provided by the module is preferred over 
    creating an instance of this class.
    """
    def __new__(cls, name, mime_types, extensions):
        """\
        Creates a new syntax instance an registeres it within the global
        syntaxes or returns an existing instance.
        """
        inst = _SYNTAXES.get(name.lower(), None)
        if not inst:
            if isinstance(mime_types, basestring):
                mime_types = mime_types,
            if isinstance(extensions, basestring):
                extensions = extensions,
            inst = tuple.__new__(cls, (name,  mime_types, extensions))
            _SYNTAXES[name.lower()] = inst
        return inst

    name = property(itemgetter(0))
    mimetypes = property(itemgetter(1))
    extensions = property(itemgetter(2))

# AsTMa= syntax.
ASTMA = Syntax('AsTMa', ('application/x-tm+astma', 'text/plain'), ('atm', 'astma'))

# Binary Topic Maps (BTM).
BTM = Syntax('BTM', 'application/x-tm+btm', 'btm')

# Compact Topic Maps syntax (CTM).
CTM = Syntax('CTM', ('application/x-tm+ctm', 'text/plain'), 'ctm')

# Canonical XML Topic Maps (CXTM).
CXTM = Syntax('CXTM', ('application/x-tm+cxtm', 'application/xml'), 'cxtm')

# JSON Topic Maps (JTM).
JTM = Syntax('JTM', ('application/x-tm+jtm', 'application/json'), 'jtm')

# Linear Topic Maps notation (LTM).
LTM = Syntax('LTM', ('application/x-ltm', 'text/plain'), 'ltm')

# XML Topic Maps (XTM).
XTM = Syntax('XTM', ('application/x-tm+xtm', 'application/xml'), 'xtm')

# TM/XML Topic Maps.
TMXML = Syntax('TM/XML', ('application/x-tmxml', 'application/xml'), ('tmx', 'xml'))

# XFML (eXchangeable Faceted Metadata Language).
XFML = Syntax('XFML', ('application/xfml+xml', 'application/xml'), 'xfml')

# Snello Topic Maps syntax (STM).
SNELLO = Syntax('Snello', ('application/x-tm+snello', 'text/plain'), ('stm', 'snello'))

# RDF/XML.
RDFXML = Syntax('RDF/XML', ('application/rdf+xml', 'application/xml'), 
                ('rdf', 'xml', 'rdfs', 'owl'))

# RDF N3 syntax.
N3 = Syntax('N3', 'text/rdf+n3', 'n3')

# RDF N-Triples syntax.
NTRIPLES = Syntax('N-Triples', 'text/plain', 'nt')

# RDF Turtle syntax.
TURTLE = Syntax('Turtle', 'application/x-turtle', 'ttl')

# RDF TriX syntax.
TRIX = Syntax('TriX', 'application/trix', ('trix', 'xml'))

# RDF TriG syntax.
TRIG = Syntax('TriG', 'application/x-trig', 'trig')

def syntax_for_extension(ext, default=None):
    """\
    Returns a syntax for the given file extension.
    
    If no syntax matches the specified extension, ``default``
    is returned (which is ``None`` if not specified)
    
    `ext`
        A file extension (with an optional leading dot (``.``))
    """
    if ext[0] == '.':
        ext = ext[1:]
    ext = ext.lower()
    for syntax in _SYNTAXES.values():
        if ext in syntax.extensions:
            return syntax
    return default

def syntax_for_mimetype(mt, default=None):
    """\
    Returns a syntax for the given MIME type.
    
    If no syntax matches the specified MIME type, ``default``
    is returned (which is ``None`` if not specified)
    
    `mt`
        A MIME type.
    """
    for syntax in _SYNTAXES.values():
        if mt in syntax.mimetypes:
            return syntax
    return default

def syntax_for_name(name, default=None):
    """\
    Returns a syntax for the given MIME type.
    
    If no syntax matches the specified MIME type, ``default``
    is returned (which is ``None`` if not specified)
    
    `name`
        The name of the syntax.
    """
    return _SYNTAXES.get(name.lower(), default)
