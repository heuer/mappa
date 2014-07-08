# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
Tests against the XTM writers.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
from mappaext.cxtm.cxtm_test import create_writer_cxtm_cases
from mio.xtm import create_deserializer
from mappaext import xtm
from mappa.xtm1utils import convert_to_tmdm


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
                "resourcedata.xtm",
                "subjectindref.xtm",
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
    for test in create_writer_cxtm_cases(create_xtm10_writer, create_deserializer, 'xtm1', 'xtm', post_process=convert_to_tmdm,
                                         exclude=_EXCLUDE_XTM_10):
        yield test


def test_xtm_20_writer():
    for test in create_writer_cxtm_cases(create_xtm20_writer, create_deserializer, 'xtm1', 'xtm', post_process=convert_to_tmdm,
                                         exclude=_EXCLUDE_XTM_10):
        yield test
    for test in create_writer_cxtm_cases(create_xtm20_writer, create_deserializer, 'xtm2', 'xtm',
                                         exclude=_EXCLUDE_XTM_20):
        yield test


def test_xtm_21_writer():
    for test in create_writer_cxtm_cases(create_xtm21_writer, create_deserializer, 'xtm1', 'xtm', post_process=convert_to_tmdm):
        yield test
    for test in create_writer_cxtm_cases(create_xtm21_writer, create_deserializer, 'xtm2', 'xtm'):
        yield test
    for test in create_writer_cxtm_cases(create_xtm21_writer, create_deserializer, 'xtm21', 'xtm'):
        yield test


if __name__ == '__main__':
    import nose
    nose.core.runmodule()
