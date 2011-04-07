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
Tests against mio.rdf.mapping.MappingHandler.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
from nose.tools import ok_
from mio.rdf.mapping import MappingHandler

def test_mapping_handler():
    mh = MappingHandler()
    ok_(not mh.mapping)
    mh.start()
    name_pred = 'http://www.example.org/name'
    mh.handleName(name_pred, None, None)
    ok_(name_pred in mh.mapping)
    occ_pred = 'http://www.example.org/occ'
    mh.handleOccurrence(occ_pred, None, None)
    ok_(occ_pred in mh.mapping)
    assoc_pred = 'http://www.example.org/assoc'
    mh.handleAssociation(assoc_pred, 'http://www.example.org/subject', 'http://www.example.org/object', None, None)
    ok_(assoc_pred in mh.mapping)
    isa_pred = 'http://www.example.org/isa'
    mh.handleInstanceOf(isa_pred, None)
    ok_(isa_pred in mh.mapping)
    isa_pred_scoped = 'http://www.example.org/isa-scoped'
    mh.handleInstanceOf(isa_pred_scoped, ['http://www.example.org/theme'])
    ok_(isa_pred_scoped in mh.mapping)
    ako_pred = 'http://www.example.org/ako'
    mh.handleSubtypeOf(ako_pred, None)
    ok_(ako_pred in mh.mapping)
    iid_pred = 'http://www.example.org/iid'
    mh.handleItemIdentifier(iid_pred)
    ok_(iid_pred in mh.mapping)
    sid_pred = 'http://www.example.org/sid'
    mh.handleSubjectIdentifier(sid_pred)
    ok_(sid_pred in mh.mapping)
    slo_pred = 'http://www.example.org/slo'
    mh.handleSubjectLocator(slo_pred)
    ok_(slo_pred in mh.mapping)
    mh.end()


if __name__ == '__main__':
    import nose
    nose.core.runmodule()
