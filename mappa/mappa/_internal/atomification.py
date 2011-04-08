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
