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
Some utility functions to check (internal) model constraints.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD License
"""
from functools import wraps
from tm import irilib
from . import kind
from mappa.utils import is_topic
from mappa import ModelConstraintViolation, IdentityViolation

def check_not_none(obj):
    """\
    Raises a ValueError iff `obj` is None.
    """
    if obj is None:
        raise ValueError('The argument must not be None')

def check_same_topicmap(first, second):
    """\
    Raises a ``ModelConstraintViolation`` iff `first` and `second` do not belong
    to the same topic map instance. 
    """
    if first.tm != second.tm:
        raise ModelConstraintViolation('The Topic Maps constructs do not belong to the same topic map')

def check_reification_allowed(reifiable, new_reifier):
    """\
    Checks if the reification of `reifiable` through `reifier` is allowed.
    """
    reifier = reifiable.reifier
    if reifier == new_reifier or not new_reifier:
        return # Setting the reifier to the same value or to None causes no problems
    if new_reifier.reified:
        raise ModelConstraintViolation('The topic reifies another Topic Maps construct.', reporter=reifiable)

def _check_topic(tmc, topic, attr):
    if getattr(topic, 'kind', None) != kind.TOPIC:
        raise ModelConstraintViolation('The %s must be a topic' % attr)
    check_same_topic_map(tmc, topic)

def _not_none(obj, name):
    if obj is None:
        raise ModelConstraintViolation('The %s must not be None' % name)

def type_constraint(f):
    @wraps(f)
    def check(typed, type):
        _check_topic(typed, type, 'type')
        return f(typed, type)
    return check

def player_constraint(f):
    @wraps(f)
    def check(role, player):
        _check_topic(role, player, 'player')
        return f(role, player)
    return check

def scope_constraint(f):
    @wraps(f)
    def check(scoped, theme):
        _check_topic(scoped, theme, 'theme')
        return f(scoped, theme)
    return check

def iid_constraint(f):
    @wraps(f)
    def check(tmc, iid):
        _not_none(iid, 'item identifier')
        iid = irilib.normalize(iid)
        tm = tmc.tm
        existing = tm.construct_by_iid(iid)
        if existing:
            if tmc != existing:
                raise IdentityViolation('A Topic Maps construct with the same item identifier "%s" exists' % iid, tmc, existing)
            else:
                return
        if is_topic(tmc):
            existing = tm.topic_by_sid(iid)
            if existing:
                if existing != tmc:
                    raise IdentityViolation('A topic with the same subject identifier "%s" exists' % iid, tmc, existing)
                else:
                    return
        return f(tmc, iid)
    return check

def sid_constraint(f):
    @wraps(f)
    def check(topic, sid):
        _not_none(sid, 'subject identifier')
        sid = irilib.normalize(sid)
        tm = topic.tm
        existing = tm.topic_by_sid(sid)
        if existing:
            if topic != existing:
                raise IdentityViolation('A topic with the same subject identifier exists', topic, existing)
            else:
                return
        existing = tm.topic_by_iid(sid)
        if existing:
            if topic != existing:
                raise IdentityViolation('A topic with the same item identifier exists', topic, existing)
            else:
                return
        return f(topic, sid)
    return check

def slo_constraint(f):
    @wraps(f)
    def check(topic, slo):
        _not_none(slo, 'subject locator')
        slo = irilib.normalize(slo)
        existing = topic.tm.topic_by_slo(slo)
        if existing:
            if topic != existing:
                raise IdentityViolation('A topic with the same subject locator exists', topic, existing)
            else:
                return
        return f(topic, slo)
    return check

def reifier_constraint(f):
    @wraps(f)
    def check(reifiable, reifier):
        if reifier:
            _check_topic(reifiable, reifier, 'reifier')
        check_reification_allowed(reifiable, reifier)
        return f(reifiable, reifier)
    return check
