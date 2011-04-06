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
`XTM 1.0`_ a.k.a. pre-TMDM utils.

These utilities are only needed if a XTM 1.0 topic map should be made `TMDM`_
compatible. Do not use them for new (TMDM compatible) topic maps.

.. _XTM 1.0: http://www.topicmaps.org/xtm/1.0/
.. _TMDM: http://www.isotopicmaps.org/sam/sam-model/

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD License
"""

def convert_to_tmdm(tm):
    """\
    Converts the XTM 1.0 reification mechanism and the XTM 1.0 PSIs to the
    TMDM equivalent.
    """
    convert_xtm10_psis(tm)
    convert_reification(tm)

def convert_xtm10_psis(tm):
    """\
    Converts XTM 1.0 PSIs to the TMDM equivalent.
    """
    from mappa import Namespace, voc, TMDM
    xtm10_base = Namespace(voc.XTM_10['core.xtm#'])
    mapping = {
               xtm10_base['class-instance']: TMDM.type_instance,
               xtm10_base['class']: TMDM.type,
               xtm10_base['instance']: TMDM.instance,
               xtm10_base['superclass-subclass']: TMDM.supertype_subtype,
               xtm10_base['superclass']: TMDM.supertype,
               xtm10_base['subclass']: TMDM.subtype,
               xtm10_base['sort']: TMDM.sort
               }
    for source, target in mapping.iteritems():
        topic = tm.topic_by_sid(source)
        if topic:
            topic.add_sid(target)
            topic.remove_sid(source)

def convert_reification(tm, remove_sid=True, remove_iid=True):
    """\
    Converts the XTM 1.0 reification mechanism (a topic with a subject identifier
    equals to a reifiable construct's item identifier makes the topic reify
    the Topic Maps construct) to TMDM.
    
    The reifing topic will become the ``reifier`` property of the reifiable
    construct.
    
    .. Note::
       This is an expensive operation and should be done only once per
       (XTM 1.0 deserialized) topic map.
    
    `remove_sid`
            Indicates if the subject identifier of the reifying topic should
            be removed (default: ``True``). In most cases the subject identifier
            can be removed because it was only created for reification
            purposes.
    `remove_iid`
            Indicates if the item identifier of the reified Topic Maps construct
            should be removed (default: ``True``)
    """
    for topic in tuple(tm.topics): # Expensive but needed for merging
        for loc in tuple(topic.sids):
            tmc = tm.construct(loc)
            if tmc and tmc != topic:
                if tmc.reifier:
                    tmc.reifier.merge(topic)
                else:
                    # If ``topic`` reifies something, a MCV is thrown
                    tmc.reifier = topic
                if remove_sid:
                    topic.remove_sid(loc)
                if remove_iid:
                    tmc.remove_iid(loc)
