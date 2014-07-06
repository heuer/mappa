# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
PyTM MIO package.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
from operator import attrgetter
import warnings
from StringIO import StringIO
from urllib import pathname2url
from xml.sax import SAXException
from tm.mio import syntax 
from tm import irilib

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
# Exceptions
#
class MIOException(SAXException, Exception):
    """\
    Common MIO exception which is thrown if an irrevocable error occurs.
    """
    pass

class MIOParseException(MIOException):
    """\
    MIO exception that provides optional line/column information.
    """
    def __init__(self, msg, exception=None, line=-1, column=-1):
        MIOException.__init__(self, msg, exception)
        self._line = line
        self._column = column

    def __str__(self):
        return 'MIOParseException at line "%s", column "%s": %s' % (self._line != -1 and self._line or '?', self._line != -1 and self._column or '?', self.getMessage())

    line = property(lambda self: self._line, doc='Returns the line number where the error occurred or -1 if the line is unknown')
    column = property(lambda self: self._column, doc='Returns the column number where the error occurred or -1 if the column is unknown')


class Source(object):
    """\
    Represents an immutable source to read a topic map from.
    
    A `Source` is similar to an `xml.sax.InputSource` except that it is 
    immutable.
    """
    def __init__(self, iri=None, file=None, data=None, encoding=None): #pylint: disable-msg=W0622
        """\
        
        `iri`
            Either an IRI from which a topic map should be read from or
            the base IRI if i.e. source is represented by ``data``.
        `file`
            A file object. If the `iri` is not provided, the base IRI is 
            constructed from the ``file.name``.
        `data`
            A string object. If this is used, the `iri` argument is required.
        `encoding`
            A string which represents the encoding.
        """
        warnings.warn('Deprecated, use tm.Source', DeprecationWarning)
        self._stream = None
        self._encoding = encoding
        if file:
            self._stream = file
            iri = iri or 'file:' + pathname2url(file.name)
        elif data:
            if hasattr(data, 'read'):
                self._stream = data
            else:
                if isinstance(data, unicode):
                    data = data.encode('utf-8')
                self._stream = StringIO(data)
            if not iri:
                raise ValueError('An IRI is required if "data" is specified')
        if not iri:
            raise ValueError('Base IRI information is missing')
        self._iri = irilib.normalize(iri)

    iri = property(attrgetter('_iri'))
    """\
    The base IRI which should be used to resolve IRIs of the source against.
    """
    stream = property(attrgetter('_stream'))
    """\
    Returns the byte stream or ``None`` if no byte stream is provided.
    """
    encoding = property(attrgetter('_encoding'))
    """\
    Returns the encoding of the source or ``None`` if no encoding is provided.
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
        return None
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
