# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
This module defines predicates to gather information from Topic Maps constructs.

Those predicates take as input typically one value and produce ``1..n`` values.

.. Note::

    These predicates may raise an ``AttributeError`` if they get an unexpected
    input.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD License
"""
from operator import attrgetter

# pylint: disable-msg=W0105

cid = attrgetter('id')
"""\
Returns the internal identifier of a Topic Maps construct.
"""

topicmap = attrgetter('tm')
"""\
Returns the topic map of a Topic Maps construct.
"""

topics = attrgetter('topics')
"""\
Returns the topics of a topic map.
"""

associations = attrgetter('associations')
"""\
Returns the associations of a topic map.
"""

parent = attrgetter('parent')
"""\
Returns the parent of a Topic Maps construct
"""

reifier = attrgetter('reifier')
"""\
Returns the reifier of a reifiable Topic Maps construct.
"""

reified = attrgetter('reified')
"""\
Returns the Topic Maps construct which is reified by the input topic.
"""

player = attrgetter('player')
"""\
Returns the player of a role

::
    >>> # Collect all role players in an asscociation
    >>> players = map(player, assoc)
"""

type_ = attrgetter('type')
"""\
Returns the type of a typed Topic Maps construct.

::
    >>> # Collect all role types in an association
    >>> role_types = map(type_, assoc)
"""

types = attrgetter('types')
"""\
Returns the types of a topic.
"""

value = attrgetter('value')
"""\
Returns the value of the a name, an occurrence, or a variant.
"""

datatype = attrgetter('datatype')
"""\
Returns the datatype of the occurrence or variant.
"""

occurrences = attrgetter('occurrences')
"""\
Returns the occurrences of a topic.
"""

names = attrgetter('names')
"""\
Returns the names of a topic.
"""

variants = attrgetter('variants')
"""\
Returns the variants of a name.
"""

roles = attrgetter('roles')
"""\
Returns the roles of an association.
"""

roles_played = attrgetter('roles_played')
"""\
Returns the roles played by the specified topic.
"""

item_identifiers = attrgetter('iids')
"""\
Returns the item identifiers of a Topic Maps construct.
"""

subject_identifiers = attrgetter('sids')
"""\
Returns the subject identifiers of a topic.
"""

subject_locators = attrgetter('slos')
"""\
Returns the subject locators of a topic.
"""

scope = attrgetter('scope')
"""\
Returns the scope of a scoped Topic Maps construct.
"""
