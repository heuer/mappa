# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
Provides an abstract deserializer which may be useful for concrete 
implementations.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
from operator import attrgetter
from tm.mio import MIOException
from tm.mio.handler import simplify


class Context(object):
    """\
    Provides information about IRIs which have been read. 
    The context is used to detect cycles in mergemap directives and to avoid
    loading a source twice.
    """
    def __init__(self):
        """\
        Creates a new context with an emtpy set of loaded IRIs.
        """
        self._loaded = set()

    def add_loaded(self, iri):
        """\
        Adds the specified IRI to the loaded IRIs.
        """
        self._loaded.add(iri)

    def _get_loaded(self):
        return frozenset(self._loaded)

    loaded = property(_get_loaded)


class Deserializer(object):
    """\
    Deserializer that is meant to be subclassed by concrete implementations.
    
    This class automatically simplyfies the ``MapHandler`` and handles
    the common use case where a deserializer acts as subdeserializer.
    
    Implementation which are derived this class MUST implement the
    `_do_parse(source)` method and MAY implement `_after_set_handler(handler)`
    and `_after_set_subordinate(subordinate)`.
    """
    def __init__(self):
        self._subordinate = False
        self._handler = None
        self.context = Context()
        self._properties = {}

    def set_property(self, name, value):
        self._properties[name] = value

    def get_property(self, name):
        return self._properties.get(name)

    def _set_handler(self, handler):
        self._handler = simplify(handler)
        self._after_set_handler(self._handler)

    def _after_set_handler(self, handler):
        """\
        Notification that the map handler has been set. The specified ``handler``
        is already "simplified" (instance of ``tm.mio.handler.SimpleMapHandler``). 
        This method does nothing by default.
        """
        pass

    def _set_subordinate(self, value):
        self._subordinate = value
        self._after_set_subordinate(self._subordinate)

    def _after_set_subordinate(self, subordinate):
        """\
        Notification that the "subordinate" state has been changed.
        This method does nothing by default.
        """
        pass

    def _do_parse(self, source):
        """\
        Parses the specified ``source``.
        
        Must be overridden by the concrete deserializer implementation. The
        implementation MUST NOT issue a ``startTopicMap`` and ``endTopicMap``
        notification. 
        """
        raise NotImplementedError()

    def parse(self, source):
        """\
        Parses the specified ``source``.
        """
        if not self._handler:
            raise MIOException('No handler defined')
        if not self._subordinate:
            self.handler.startTopicMap()
        try:
            self._do_parse(source)
        finally:
            if not self._subordinate:
                self._handler.endTopicMap()
            self._handler = None

    handler = property(attrgetter('_handler'), _set_handler)
    subordinate = property(attrgetter('_subordinate'), _set_subordinate)
