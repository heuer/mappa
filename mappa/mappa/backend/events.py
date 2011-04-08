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
This module defines a simple event dispatcher / handling mechanism and the
Mappa standard events (altough the events may not be available / used in every 
implementation).

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD License
"""
from operator import itemgetter
from collections import defaultdict

class EventDispatcher(object):
    """\
    
    """
    def __init__(self):
        self._handlers = defaultdict(set)

    def subscribe(self, event_type, handler):
        """\
        Subscribes the `handler` to the specified `event_type`.
        """
        self._handlers[event_type].add(handler)

    def dispatch(self, event):
        """\
        Dispatches the specified `event` to the subscribed handlers.
        """
        for handler in self._handlers.get(type(event), ()):
            handler(event)

class EventMultiplier(object):
    """\
    This class subscribes itself to several `Add*` and `Remove*` events
    and uses the same `EventDispatcher` to generate additional `Add*` / `Remove*`
    events.
    """
    def __init__(self, dispatcher):
        """\
        Subscribes itself to the ``dispatcher`` which is a 
        `mappa.backend.event.EventDispatcher` instance (a topic map in most cases).
        """
        self._dispatcher = dispatcher
        self.subscribe(dispatcher)

    def subscribe(self, dispatcher):
        # Subscribe to every Topic Maps construct which has children
        dispatcher.subscribe(AddTopic, self._add_topic)
        dispatcher.subscribe(RemoveTopic, self._remove_topic)
        dispatcher.subscribe(AddAssociation, self._add_assoc)
        dispatcher.subscribe(RemoveAssociation, self._remove_assoc)
        dispatcher.subscribe(AddName, self._add_name)
        dispatcher.subscribe(RemoveName, self._remove_name)

    def _add_topic(self, evt):
        """\
        Called if a topic is added and generates `AddOccurrence` /
        `AddName` events for each occurrence / name.
        """
        topic = evt.new
        dispatcher = self._dispatcher
        for occ in topic.occurrences:
            dispatcher.dispatch(AddOccurrence(topic, occ))
        for name in topic.names:
            dispatcher.dispatch(AddName(topic, name))

    def _remove_topic(self, evt):
        """\
        Called if a topic is removed and generates `RemoveOccurrence` /
        `RemoveName` events for each occurrence / name.
        """
        topic = evt.old
        dispatcher = self._dispatcher
        for occ in topic.occurrences:
            dispatcher.dispatch(RemoveOccurrence(topic, occ))
        for name in topic.names:
            dispatcher.dispatch(RemoveName(topic, name))

    def _add_assoc(self, evt):
        """\
        Called if an association is added and generates `AddRole` events for 
        each role.
        """
        assoc = evt.new
        dispatcher = self._dispatcher
        for role in assoc:
            dispatcher.dispatch(AddRole(assoc, role))

    def _remove_assoc(self, evt):
        """\
        Called if an association is removed and generates `RemoveRole` events for 
        each role.
        """
        assoc = evt.old
        dispatcher = self._dispatcher
        for role in assoc:
            dispatcher.dispatch(RemoveRole(assoc, role))

    def _add_name(self, evt):
        """\
        Called if a name is added and generates `AddVariant` events for 
        each variant.
        """
        name = evt.new
        dispatcher = self._dispatcher
        for var in name:
            dispatcher.dispatch(AddVariant(name, var))

    def _remove_name(self, evt):
        """\
        Called if a name is removed and generates `RemoveVariant` events for 
        each variant.
        """
        name = evt.old
        dispatcher = self._dispatcher
        for var in name:
            dispatcher.dispatch(RemoveVariant(name, var))


class Event(tuple):
    """\
    Base class for all events. This class is not meant to be used directly.
    """
    __slots__ = ()

    def __new__(cls, source, old, new):
        return tuple.__new__(cls, (source, old, new))

    source = property(itemgetter(0))
    old = property(itemgetter(1))
    new = property(itemgetter(2))

class AddEvent(Event):
    def __new__(cls, source, new):
        return Event.__new__(cls, source, None, new)

class RemoveEvent(Event):
    def __new__(cls, source, old):
        return Event.__new__(cls, source, old, None)

class ChangeEvent(Event):
    def __new__(cls, source, old, new):
        return Event.__new__(cls, source, old, new)

class AddTopic(AddEvent): pass
class RemoveTopic(RemoveEvent): pass
class AddAssociation(AddEvent): pass
class RemoveAssociation(RemoveEvent): pass
class AddRole(AddEvent): pass
class RemoveRole(RemoveEvent): pass
class AddOccurrence(AddEvent): pass
class RemoveOccurrence(RemoveEvent): pass
class AddName(AddEvent): pass
class RemoveName(RemoveEvent): pass
class AddVariant(AddEvent): pass
class RemoveVariant(RemoveEvent): pass
class AddItemIdentifier(AddEvent): pass
class RemoveItemIdentifier(RemoveEvent): pass
class AddSubjectIdentifier(AddEvent): pass
class RemoveSubjectIdentifier(RemoveEvent): pass
class AddSubjectLocator(AddEvent): pass
class RemoveSubjectLocator(RemoveEvent): pass
class AddType(AddEvent): pass
class RemoveType(RemoveEvent): pass

class SetType(ChangeEvent): pass
class SetReifier(ChangeEvent): pass
class SetScope(ChangeEvent): pass
class SetValue(ChangeEvent): pass
