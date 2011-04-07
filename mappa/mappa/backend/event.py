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
#     * Neither the name 'Semagia' nor the name 'Mappa' nor the names of the
#       contributors may be used to endorse or promote products derived from 
#       this software without specific prior written permission.
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
This module defines a simple event dispatcher / handling mechanism and the
Mappa standard events (altough the events may not be available / used in every 
implementation).

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD License
"""

class EventDispatcher(object):
    """\
    
    """
    def __init__(self):
        self._handlers = {}

    def subscribe(self, event_type, handler):
        """\
        Subscribes the `handler` to the specified `event_type`.
        """
        handle = self._handlers.get(event_type, None)
        if handle is None:
            handle = [handler]
        else:
            handle.append(handler)
        self._handlers[event_type] = handle

    def dispatch(self, event):
        """\
        Dispatches the specified `event` to the subscribed handlers.
        """
        handlers = self._handlers.get(type(event), None)
        if handlers is None:
            return
        for handler in handlers:
            handler(event)

    def __getstate__(self):
        d = self.__dict__.copy()
        del d['_handlers']
        return d


class Event(object):
    """\
    Base class for all events. This class is not meant to be used directly.
    """
    def __init__(self, source, old, new):
        self.source = source
        self.old = old
        self.new = new

class AddTMC(Event):
    def __init__(self, source, tmc):
        Event.__init__(self, source, None, tmc)
        
class RemoveTMC(Event):
    def __init__(self, source, tmc):
        Event.__init__(self, source, tmc, None)

class AddTopic(AddTMC): pass

class RemoveTopic(RemoveTMC): pass

class AddAssociation(AddTMC): pass

class RemoveAssociation(RemoveTMC): pass

class AddRole(AddTMC): pass

class RemoveRole(RemoveTMC): pass

class AddOccurrence(AddTMC): pass

class RemoveOccurrence(RemoveTMC): pass

class AddName(AddTMC): pass

class RemoveName(RemoveTMC): pass

class AddVariant(AddTMC): pass

class RemoveVariant(RemoveTMC): pass

class AddItentity(Event):
    def __init__(self, source, identity):
        Event.__init__(self, source, None, identity)

class RemoveItentity(Event):
    def __init__(self, source, identity):
        Event.__init__(self, source, identity, None)

class AddItemIdentifier(AddItentity):
    """\
    Event fired if an item identifier is added to a Topic Maps construct.
    """
    pass

class RemoveItemIdentifier(RemoveItentity):
    """\
    Event fired if an item identifier is removed from a Topic Maps construct.
    """
    pass

class AddSubjectIdentifier(AddItentity):
    """\
    Event fired if a subject identifier is added to a topic.
    """
class RemoveSubjectIdentifier(RemoveItentity):
    """\
    Event fired if a subject identifier is removed from a topic.
    """

class AddSubjectLocator(AddItentity): pass

class RemoveSubjectLocator(RemoveItentity): pass

class AddType(Event):
    def __init__(self, source, type):
        Event.__init__(self, source, None, type)

class RemoveType(Event):
    def __init__(self, source, type):
        Event.__init__(self, source, type, None)

class SetType(Event):
    def __init__(self, source, old_value, new_value):
        Event.__init__(self, source, old_value, new_value)

class SetReifier(Event):
    def __init__(self, source, old_value, new_value):
        Event.__init__(self, source, old_value, new_value)

class SetScope(Event):
    def __init__(self, source, old_value, new_value):
        Event.__init__(self, source, old_value, new_value)

class SetValue(Event):
    def __init__(self, source, old_value, new_value):
        Event.__init__(self, source, old_value, new_value)
