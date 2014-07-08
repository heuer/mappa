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
from mappaext.cxtm.cxtm_test import create_invalid_cxtm_cases, \
    create_valid_cxtm_cases
from mio.jtm import create_deserializer


def test_cxtm_valid_10():
    for test in create_valid_cxtm_cases(create_deserializer, 'jtm', 'jtm'):
        yield test


def test_cxtm_invalid_10():
    for test in create_invalid_cxtm_cases(create_deserializer, 'jtm', 'jtm'):
        yield test


def test_cxtm_valid_11():
    for test in create_valid_cxtm_cases(create_deserializer, 'jtm11', 'jtm'):
        yield test


def test_cxtm_invalid_11():
    for test in create_invalid_cxtm_cases(create_deserializer, 'jtm11', 'jtm'):
        yield test


if __name__ == '__main__':
    import nose
    nose.core.runmodule()
