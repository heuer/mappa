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
Provides Topic Maps sources.

.. Warning::

    This module does not belong to the public API, use::
    
        from tm.mio import Source

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
try:
    from operator import attrgetter
except ImportError:
    def attrgetter(attr):
        return lambda x: getattr(x, attr)
from StringIO import StringIO
from urllib import pathname2url
from tm import irilib

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
                raise Exception('An IRI is required if "data" is specified')
        if not iri:
            raise Exception('Base IRI information is missing')
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
