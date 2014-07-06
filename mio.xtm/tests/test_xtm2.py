# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\


:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
from mappaext.cxtm.cxtm_test import create_invalid_cxtm_cases, create_valid_cxtm_cases
from mio.xtm import create_deserializer

_EXCLUDED_INVALID_TESTS = (
    'id-invalid.xtm', # This should be detected by the XML parser, but expat accepts it
)

def test_cxtm_invalid_xtm_20():
    for test in create_invalid_cxtm_cases(create_deserializer, 'xtm2', 'xtm', _EXCLUDED_INVALID_TESTS):
        yield test

def test_cxtm_valid_xtm_20():
    for test in create_valid_cxtm_cases(create_deserializer, 'xtm2', 'xtm'):
        yield test

def test_cxtm_invalid_xtm_21():
    for test in create_invalid_cxtm_cases(create_deserializer, 'xtm21', 'xtm', _EXCLUDED_INVALID_TESTS):
        yield test

def test_cxtm_valid_xtm_21():
    for test in create_valid_cxtm_cases(create_deserializer, 'xtm21', 'xtm'):
        yield test


if __name__ == '__main__':
    import nose
    nose.core.runmodule()
