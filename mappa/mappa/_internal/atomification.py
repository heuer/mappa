# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
Implementation independent default atomification algorithms.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD License
"""
from mappa import ANY, UCS, TMDM
from mappa.utils import is_name, nice_identifier, topic_for
from mappa._internal.it import one_of


def atomify_topic(topic, ctx=ANY):
    """\
    Defaut algorithm to atomify a topic.
    """
    name_type = topic.tm.topic(sid=TMDM.topic_name) or ANY
    name = None
    names_by = topic.names_by
    if ctx in (ANY, UCS):
        name = one_of(names_by(type=name_type, scope=UCS))
    elif name_type is not ANY:
        name = one_of(names_by(type=name_type, scope=ctx))
    if not name:
        name = one_of(names_by(type=ANY, scope=ctx)) \
                 or one_of(names_by(type=ANY, scope=UCS)) \
                 or nice_identifier(topic) \
                 or one_of(topic.names) # Random name
    if name:
        if is_name(name):
            return name.value
        return name  # Got a string
    return object.__str__(topic)


def atomify_association(assoc):
    """\
    Atomifies either the `assoc` reifier or the assoc type.
    """
    return atomify_topic(topic_for(assoc), assoc.scope)


def atomify_name(name):
    """\
    Returns the name value.
    """
    return name.value


def atomify_dataobject(do):
    """\
    Default algorithm to atomify occurrences and variants.
    """
    try:
        return do.__pyvalue__()
    except AttributeError:
        return do.value
