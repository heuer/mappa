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
PyTM MIO package.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:version:      $Rev: 393 $ - $Date: 2011-01-10 11:52:54 +0100 (Mo, 10 Jan 2011) $
:license:      BSD license
"""
import warnings
from tm.mio._exceptions import MIOException, MIOParseException
from tm.mio import syntax 
from tm.mio._source import Source

__all__ = ('SUBJECT_IDENTIFIER', 'SUBJECT_LOCATOR', 'ITEM_IDENTIFIER',
           'MIOException', 'MIOParseException', 'Source', 'create_deserializer')

#pylint: disable-msg=W0105

ITEM_IDENTIFIER = 1
"""\
Constant for an item identifier reference.
"""

SUBJECT_IDENTIFIER = 2
"""\
Constant for a subject identifier reference.
"""

SUBJECT_LOCATOR = 3
"""\
Constant for a subject locator reference.
"""

#
# Deserializer registration / discovery
#

# Syntax -> factory mapping
_DESERIALIZERS = {}

def register_deserializer(module, syn, warn=True):
    """\
    Registers a deserializer factory.
    
    `module`
        A module which provides a 'create_deserializer' function to create instances of
        ``IDeserializer``.
    `syn`
        Syntax instance.
    """
    if _DESERIALIZERS.get(syn):
        if warn:
            warnings.warn('The deserializer "%r" was replaced by "%r"' % (_DESERIALIZERS.get(syn), module))
    _DESERIALIZERS[syn] = module

_ENTRY_POINT = 'mio.reader'

# Register all deserializers
import pkg_resources

def _register_all(warn=True):
    for ep in pkg_resources.iter_entry_points(_ENTRY_POINT):
        syntax_ = syntax.syntax_for_name(ep.name)
        if not syntax_:
            warnings.warn('Cannot register reader "%s (%s)". Syntax unknown' % (ep.name, ep.module_name))
            continue
        register_deserializer(ep.module_name, syntax_, warn)

_register_all()

def _get_deserializer(syn):
    deser = _DESERIALIZERS.get(syn)
    if not deser:
        _register_all(warn=False)
    return _DESERIALIZERS.get(syn)

def create_deserializer(format=None, mimetype=None, extension=None, **kw):
    """\
    
    `format`
        Either a ``tm.mio.syntax.Syntax`` instance or a syntax name.
    `mimetype`
        MIME type
    `extension`
        A file extension (optionally with a leading dot ``.``)
    """
    syntax_ = _find_syntax(format, mimetype, extension)
    if not syntax_:
        raise MIOException('Unknown syntax for format="%s", mimetype="%s", extension="%s"' % (format, mimetype, extension))
    name = _get_deserializer(syntax_)
    if name:
        factory = __import__(name, globals(), globals(), ['__name__'])
        return factory.create_deserializer(**kw)
    return None


def _find_syntax(format=None, mimetype=None, extension=None):
    """\
    Tries to find a syntax instance by the provided indicators in the 
    following order:
    
        * Return syntax by the `format`
        * Return syntax by `mimetype`
        * Return syntax by `extension`
    
    `format`
        Either a syntax name like "xtm" or a syntax instance.
    `mimetype`
        A string representing a MIME type
    `extension`
        A file extension.
    """
    if format:
        if isinstance(format, basestring):
            return syntax.syntax_for_name(format)
        else:
            assert isinstance(format, syntax.Syntax)
            return format
    elif mimetype:
        return syntax.syntax_for_mimetype(mimetype)
    elif extension:
        return syntax.syntax_for_extension(extension)
    return None
