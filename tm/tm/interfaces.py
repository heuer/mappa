# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
Interfaces for the PyTM package; mainly for documentation purposes.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
from tm.proto import Interface, Attribute

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

