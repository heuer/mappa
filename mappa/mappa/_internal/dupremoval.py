# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
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
