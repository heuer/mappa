# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
Mappa's internal utilities.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD License
"""
from itertools import chain
from uuid import uuid4
from tm.xmlutils import is_ncname

def random_id():
    return uuid4().int

def topic_id(base, topic):
    """\
    Returns an identifier for the provided topic.
    """
    ident = None
    for loc in chain(topic.iids, topic.sids):
        if not loc.startswith(base) or not '#' in loc:
            continue
        ident = loc[loc.index('#')+1:]
        if ident.startswith('t-'):
            ident = None
            continue
        break
    if not ident:
        ident = topic.id
    if ident and is_ncname(unicode(ident)):
        return ident
    return 't-%s' % topic.id

def is_slo(string):
    """\
    Returns if the string represents a subject locator.
    Subject locators start with "="
    """
    return string[0] == '='

def strip_slo_prefix(string):
    """\
    
    """
    return string[1:].strip()

def is_uri(string):
    """\
    Returns if the string represents a URI.
    
    Note that this function just checks if a colon ``:`` is present.
    """
    return ':' in string

def make_locator(base, frag):
    from mappa import irilib
    return irilib.resolve_iri(base, '#' + frag)
