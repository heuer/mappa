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


:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD License
"""
from mappa import irilib
from mappa import IdentityViolation
from mappa.utils import is_topic
from mappa._internal.constraints import check_reification_allowed
from mappa.backend.event import *

class IdentityManager(object):
    """\

    """
    def __init__(self, dispatcher):
        """\
        Initializes the instance with `dispatcher`.
        
        The `dispatcher` is a `mappa.backend.event.EventDispatcher` instance, 
        (a topic map in most cases) used to subscribe the handlers of this class.
        """
        self._iid2tmc = {}
        self._sid2topic = {}
        self._slo2topic = {}
        self._id2tmc = {}
        self.subscribe(dispatcher)

    def subscribe(self, dispatcher):
        """\
        Subscribes `dispatcher`.
        
        The `dispatcher` is a `mappa.backend.event.EventDispatcher` instance, 
        (a topic map in most cases) used to subscribe the handlers of this class.
        """
        dispatcher.subscribe(AddTopic, self.add_topic)
        dispatcher.subscribe(AddAssociation, self.add_tmc)
        dispatcher.subscribe(AddRole, self.add_tmc)
        dispatcher.subscribe(AddOccurrence, self.add_tmc)
        dispatcher.subscribe(AddName, self.add_tmc)
        dispatcher.subscribe(AddVariant, self.add_tmc)
        dispatcher.subscribe(RemoveTopic, self.remove_topic)
        dispatcher.subscribe(RemoveAssociation, self.remove_tmc)
        dispatcher.subscribe(RemoveRole, self.remove_tmc)
        dispatcher.subscribe(RemoveOccurrence, self.remove_tmc)
        dispatcher.subscribe(RemoveName, self.remove_tmc)
        dispatcher.subscribe(RemoveVariant, self.remove_tmc)
        
        dispatcher.subscribe(AddItemIdentifier, self.add_iid)
        dispatcher.subscribe(AddSubjectIdentifier, self.add_sid)
        dispatcher.subscribe(AddSubjectLocator, self.add_slo)
        dispatcher.subscribe(RemoveItemIdentifier, self.remove_iid)
        dispatcher.subscribe(RemoveSubjectIdentifier, self.remove_sid)
        dispatcher.subscribe(RemoveSubjectLocator, self.remove_slo)
        #TODO: Move this into the reifiable Topic Maps construct _set_reifier?
        dispatcher.subscribe(SetReifier, self._set_reifier)

    def _set_reifier(self, evt):
        check_reification_allowed(evt.source, evt.new)

    def add_tmc(self, evt, is_topic=False):
        tmc = evt.new
        for iid in tmc.iids:
            self._add_iid(tmc, iid, is_topic)
        self._id2tmc[tmc.id] = tmc

    def add_topic(self, evt):
        self.add_tmc(evt, True)
        topic = evt.new
        for sid in topic.sids:
            self._add_sid(topic, sid)
        for slo in topic.slos:
            self._add_slo(topic, slo)

    def remove_tmc(self, evt):
        tmc = evt.old
        for iid in tmc.iids:
            self._remove_iid(iid)
        del self._id2tmc[tmc.id]

    def remove_topic(self, evt):
        self.remove_tmc(evt)
        topic = evt.old
        for sid in topic.sids:
            self._remove_sid(sid)
        for slo in topic.slos:
            self._remove_slo(slo)

    def add_iid(self, evt):
        self._add_iid(evt.source, evt.new, is_topic(evt.source))

    def _add_iid(self, src, iid, a_topic):
        existing = self._iid2tmc.get(iid, None)
        if existing and src != existing:
            raise IdentityViolation('A Topic Maps construct with the same item identifier "%s" exists' % iid, src, existing)
        if a_topic:
            existing = self._sid2topic.get(iid)
            if existing and existing != src:
                raise IdentityViolation('A topic with the same subject identifier "%s" exists' % iid, src, existing)
        self._iid2tmc[iid] = src            

    def add_sid(self, evt):
        self._add_sid(evt.source, evt.new)

    def _add_sid(self, topic, sid):
        existing = self._sid2topic.get(sid, None)
        if existing and topic != existing:
            raise IdentityViolation('A topic with the same subject identifier exists', topic, existing)
        existing = self._iid2tmc.get(sid)
        if existing and is_topic(existing) and topic != existing:
            raise IdentityViolation('A topic with the same item identifier exists', topic, existing)
        self._sid2topic[sid] = topic

    def add_slo(self, evt):
        self._add_slo(evt.source, evt.new)

    def _add_slo(self, topic, slo):
        existing = self._slo2topic.get(slo, None)
        if existing and topic != existing:
            raise IdentityViolation('A topic with the same subject locator exists', topic, existing)
        self._slo2topic[slo] = topic

    def remove_iid(self, evt):
        self._remove_iid(evt.old)

    def _remove_iid(self, iid):
        del self._iid2tmc[iid]

    def remove_sid(self, evt):
        self._remove_sid(evt.old)

    def _remove_sid(self, sid):
        del self._sid2topic[sid]

    def remove_slo(self, evt):
        self._remove_slo(evt.old)

    def _remove_slo(self, slo):
        del self._slo2topic[slo]

    def construct_by_id(self, id):
        return self._id2tmc.get(id)

    def construct_by_iid(self, iid):
        return self._iid2tmc.get(irilib.normalize(iid))

    def topic_by_sid(self, sid):
        return self._sid2topic.get(irilib.normalize(sid))

    def topic_by_slo(self, slo):
        return self._slo2topic.get(irilib.normalize(slo))
