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
Utility function to remove duplicates.

.. Note::

    Do not import this module, use::
    
        from mappa import utils
        
        utils.remove_duplicates(tm)


:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD License
"""
from itertools import imap
from mappa._internal.mergeutils import move_variants, handle_existing

def remove_duplicates(tm):
    """\
    Removes any duplicate from the topic map specified by ``tm``.
    
    `tm`
        The topic map to remove duplicates from.
    """
    for topic in tm.topics:
        remove_duplicates_from_topic(topic)
    ti_idx = tm.index.type_instance
    for assoc_type in ti_idx.association_types():
        _remove_duplicate_associations(ti_idx.associations(assoc_type))

def remove_duplicates_from_topic(topic):
    """\
    Removes duplicates from the specified ``topic``.
    
    `topic`
        The topic to remove duplicates from.
    """
    _remove_duplicates_from_iterable(topic.occurrences)
    _remove_duplicate_names(topic.names)

def _remove_duplicates_from_iterable(iterable):
    sigs = {}
    for sig, e in _signature_construct(iterable):
        existing = sigs.get(sig)
        if existing:
            handle_existing(e, existing)
            e.remove()
        else:
            sigs[sig] = e

def _remove_duplicate_names(names):
    sigs = {}
    for sig, name in _signature_construct(names):
        _remove_duplicates_from_name(name)
        existing = sigs.get(sig)
        if existing:
            handle_existing(name, existing)
            move_variants(name, existing)
            name.remove()
        else:
            sigs[sig] = name

def _remove_duplicates_from_name(name):
    """\
    Removes duplicate variants from the specified name.
    """
    _remove_duplicates_from_iterable(name.variants)


def _remove_duplicate_associations(assocs):
    sigs = {}
    for assoc in tuple(assocs):
        _remove_duplicates_from_association(assoc)
        sig = assoc.__sig__()
        existing = sigs.get(sig)
        if existing:
            assoc.remove()
        else:
            sigs[sig] = assoc

def _remove_duplicates_from_association(assoc):
    """\
    
    """
    _remove_duplicates_from_iterable(assoc.roles)

def _signature_construct(iterable):
    def sig_construct_pair(c):
        return c.__sig__(), c
    return imap(sig_construct_pair, tuple(iterable))
