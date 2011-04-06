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


:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
from mappaext.cxtm.cxtm_test import create_writer_cxtm_cases
from mio.xtm import create_deserializer
from mappaext import xtm

def create_xtm10_writer(out, base):
    return xtm.create_writer(out, base, prettify=True, version=1.0)

def create_xtm20_writer(out, base):
    return xtm.create_writer(out, base, prettify=True, version=2.0)

def create_xtm21_writer(out, base):
    return xtm.create_writer(out, base, prettify=True, version=2.1)

# Excluding these tms since they cause problems with iids
 # Either the writer adds an iid or it exports not enough iids
_EXCLUDE_XTM_10 = [
                "eliots-xtm-test.xtm",
                "association-reifier.xtm",
                "association-untyped.xtm",
                "bug-53.xtm",
                "bug-55.xtm",
                "bug-56.xtm",
                "bug-57.xtm",
                "bug660.xtm",
                "instanceof-equiv.xtm",
                "itemid-association.xtm",
                "itemid-name.xtm",
                "itemid-occurrence.xtm",
                "itemid-tm.xtm",
                "itemid-variant.xtm",
                "merge-indicator.xtm",
                "merge-itemid.xtm",
                "merge-subject.xtm",
                "merge-subjid.xtm",
                "merge-subjloc.xtm",
                "merge-three-way.xtm",
                "merge-topicref.xtm",
                "mergemap-xmlbase.xtm",
                "mergemap.xtm",
                "mergemap2.xtm",
                "name-duplicate-merge.xtm",
                "name-scope-duplicate-merged.xtm",
                "occurrence-scope-duplicate-merged.xtm",
                "occurrences.xtm",
                "reification-bug-1.xtm",
                "reification-bug-2.xtm",
                "resourcedata.xtm",
                "subjectindref.xtm",
                "tm-reifier.xtm",
                "topic-as-subj-ind-1.xtm",
                "topic-as-subj-ind-2.xtm",
                "whitespace.xtm",
                "xmlbase-empty-base.xtm",
                "xmlbase-problem.xtm",
                "xmlbase-problem2.xtm",
                "xmlbase.xtm",
                'indirectsubjind.xtm',
                'badref.xtm',
                ]

_EXCLUDE_XTM_20 = [
    'topic-type.xtm',
    'topic-type-duplicate.xtm',
    'name-type.xtm',
    'name-type-scope.xtm',
    'mergemap.xtm',
    'mergemap-tm-reifier.xtm',
    'mergemap-merge.xtm',
    'mergemap-loop.xtm',
    'mergemap-itemid.xtm',
    'merge-itemid-with-types.xtm',
    ]

def test_xtm_10_writer():
    for test in create_writer_cxtm_cases(create_xtm10_writer, create_deserializer, 'xtm1', 'xtm',
                                         exclude=_EXCLUDE_XTM_10):
        yield test

def test_xtm_20_writer():
    for test in create_writer_cxtm_cases(create_xtm20_writer, create_deserializer, 'xtm2', 'xtm',
                                         exclude=_EXCLUDE_XTM_20):
        yield test

def test_xtm_21_writer():
    for test in create_writer_cxtm_cases(create_xtm21_writer, create_deserializer, 'xtm1', 'xtm',
                                         exclude=['tm-reifier.xtm',  'instanceof-equiv.xtm',
                                                  'association-reifier.xtm', 'reification-bug-1.xtm',
                                                  'reification-bug-2.xtm']):
        yield test
    for test in create_writer_cxtm_cases(create_xtm21_writer, create_deserializer, 'xtm2', 'xtm'):
        yield test
    for test in create_writer_cxtm_cases(create_xtm21_writer, create_deserializer, 'xtm21', 'xtm'):
        yield test


if __name__ == '__main__':
    import nose
    nose.core.runmodule()
