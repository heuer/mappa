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
