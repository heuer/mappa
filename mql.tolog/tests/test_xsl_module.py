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
import os
import io
from nose.tools import ok_
from mql.tolog import parse_to_etree, xsl


def test_get_transformator():
    def check(name):
        ok_(xsl.get_transformator(name) is not None)
    for n in xsl.get_transformator_names():
        yield check, n


def test_transformation():
    tolog_dir = os.path.abspath('./xsltests/in/')
    for f in os.listdir(tolog_dir):
        filename = os.path.join(tolog_dir, f)
        tree = parse_to_etree(open(filename, 'rb'))
        out = io.BytesIO()
        tree.write_c14n(out)
        print out.getvalue()
        #raise out.getvalue()


if __name__ == '__main__':
    import nose
    nose.core.runmodule()
