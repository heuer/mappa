# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
CTM test cases.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
from mappaext.cxtm.cxtm_test import create_invalid_cxtm_cases, create_valid_cxtm_cases
from mio.ctm import create_deserializer

_EXCLUDED = [
    'topic-identifier-unicode.ctm'  # Due to limitations of the re.module
]

def test_cxtm_valid():
    for test in create_valid_cxtm_cases(create_deserializer, 'ctm', 'ctm', exclude=_EXCLUDED):
        yield test


def test_cxtm_invalid():
    for test in create_invalid_cxtm_cases(create_deserializer, 'ctm', 'ctm'):
        yield test


if __name__ == '__main__':
    import nose
    nose.core.runmodule()
