# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
Tests against the mql.tolog.xsl module

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD License
"""
from nose.tools import ok_
from mql.tolog import xsl


def test_get_transformator():
    def check(name):
        ok_(xsl.get_transformator(name) is not None)
    for n in xsl.get_transformator_names():
        yield check, n


if __name__ == '__main__':
    import nose
    nose.core.runmodule()

