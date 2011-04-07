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
RDF to Topic Maps (RTM) standard PSIs.

This module provides the standard PSIs used in RTM. If you need one 
of the standard PSIs, you should use this module, rather than the `RDF2TM`
namespace provided by the ``tm.voc`` module to avoid typos. By convention,
the hyphen (``-``) in the PSIs is replaced by an underscore character (``_``)

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
from tm.voc import RDF2TM

__all__ = () # Avoid to expose something that pollutes the namespace, i.e. `type`

#pylint: disable-msg=W0622

maps_to = RDF2TM['maps-to']
type = RDF2TM['type']
in_scope = RDF2TM['in-scope']
subject_role = RDF2TM['subject-role']
object_role = RDF2TM['object-role']
basename = RDF2TM['basename']
occurrence = RDF2TM['occurrence']
association = RDF2TM['association']
instance_of = RDF2TM['instance-of']
subject_identifier = RDF2TM['subject-identifier']
subject_locator = RDF2TM['subject-locator']
source_locator = RDF2TM['source-locator']

del RDF2TM
