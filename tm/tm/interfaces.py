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
Interfaces for the PyTM package; mainly for documentation purposes.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:version:      $Rev: 279 $ - $Date: 2009-11-29 18:35:34 +0100 (So, 29 Nov 2009) $
:license:      BSD license
"""
from tm._proto import Interface, Attribute

# Get rid of missing 'self' as first arg errors
#pylint: disable-msg=E0213

class ISource(Interface):
    """\
    Represents a source to read a topic map from.
    """
    iri = Attribute("""\
    The base IRI which should be used to resolve IRIs of the source against.
    
    This attribute is read-only.
    """)
    byte_stream = Attribute("""\
    Returns the byte stream or ``None`` if no byte stream is provided.
    
    This attribute is read-only.
    """)
    character_stream = Attribute("""\
    Returns the character stream or ``None`` if no character stream is provided.
    
    This attribute is read-only.
    """)
    encoding = Attribute("""\
    Returns the encoding of the source or ``None`` if no encoding is provided.
    
    This attribute is read-only.
    """)

class IDeserializer(Interface):
    """\
    
    """
    def parse(source):
        """\
        Parses the `source`.
        """
    handler = Attribute("""\
    Sets / returns the ``mio.handler.MapHandler`` instance this deserializer
    operates on.
    """)
    subordinate = Attribute("""\
    Sets / returns if this deserializer is utilized by another deserializer.
    
    If ``subordinate`` is ``True``, the deserializer MUST NOT call
    ``MapHandler.startTopicMap()`` and ``MapHandler.endTopicMap``.
    """)
    context = Attribute("""\
    Keeps track of imported topic maps.
    """)

