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
import json
import glob
from nose.tools import ok_, eq_
from mql.tolog import parse_to_etree, xsl


def test_get_transformator():
    def check(name):
        ok_(xsl.get_transformator(name) is not None)
    for n in xsl.get_transformator_names():
        yield check, n


_IGNORE = (
    'fold-type-assoc.tl',
)


def test_transformation():
    base_dir = os.path.abspath('./xsltests/')
    with open(os.path.join(base_dir, 'query2optimizers.json'), 'rb') as f:
        query2optimizers = json.load(f)
    tolog_dir = os.path.abspath(os.path.join(base_dir, './in/'))
    found_files = set([os.path.basename(fn) for fn in glob.glob(tolog_dir + '/*.tl')])
    baseline_dir = os.path.join(base_dir, './baseline/')
    for fn in query2optimizers:
        found_files.remove(fn)
        optimizers = ['query-c14n']
        optimizers.extend(query2optimizers[fn])
        filename = os.path.join(tolog_dir, fn)
        tree = parse_to_etree(open(filename, 'rb'))
        res = xsl.apply_transformations(tree, optimizers)
        out = io.BytesIO()
        res.write_c14n(out)
        expected = io.open(os.path.join(baseline_dir, fn + '.c14n'), encoding='utf-8').read()
        yield eq_, expected, out.getvalue()
    for fn in _IGNORE:
        found_files.remove(fn)
    if found_files:
        raise Exception('Found more files in the directory: %r' % found_files)



if __name__ == '__main__':
    import nose
    nose.core.runmodule()
