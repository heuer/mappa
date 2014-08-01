# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
Tests against the "back-to-tolog" stylesheet.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD License
"""
import os
import io
import json
import glob
from nose.tools import eq_
from mql import tolog
from mql.tolog import xsl


_IGNORE = (
    'fold-type-assoc.tl',
    'tolog-tut-2-4_2.tl',
    'topic-types.tl',
    'topic-types2.tl',
    'fold-scope-name.tl',
    'fold-scope-occ.tl',
    'create-dyn-occ3.tl',
)

def fail(msg): raise AssertionError(msg)


def test_tolog_plus():
    base_dir = os.path.abspath('./xsltests/')
    with open(os.path.join(base_dir, 'query2optimizers.json'), 'rb') as f:
        query2optimizers = json.load(f)
    tolog_dir = os.path.abspath(os.path.join(base_dir, './in/'))
    found_files = set([os.path.basename(fn) for fn in glob.glob(tolog_dir + '/*.tl')])
    baseline_dir = os.path.join(base_dir, './baseline/')
    for fn in query2optimizers:
        if fn in _IGNORE:
            continue
        found_files.remove(fn)
        optimizers = ['query-c14n']
        optimizers.extend(query2optimizers[fn])
        filename = os.path.join(tolog_dir, fn)
        f = open(filename, 'rb')
        # 1. Apply optimizers and return tolog+
        tl = tolog.convert_to_tolog_plus(f, optimizers=optimizers)
        # 2. Parse created tolog+
        try:
            tree = tolog.parse_to_etree(tl, iri='http://www.example.org/mql-tolog/', tolog_plus=True)
        except Exception, ex:
            fail('Error: %r in %s' % (ex, tl))
        # 3. Apply optimizers to the newly parsed query
        res = xsl.apply_transformations(tree, optimizers)
        out = io.BytesIO()
        res.write_c14n(out)
        expected = io.open(os.path.join(baseline_dir, fn + '.c14n'), encoding='utf-8').read()
        yield eq_, expected, out.getvalue(), 't+: %s\n%s' % (fn, tl)
    for fn in _IGNORE:
        found_files.remove(fn)
    if found_files:
        raise Exception('Found more files in the directory: %r' % found_files)


def test_tolog():
    base_dir = os.path.abspath('./xsltests/')
    with open(os.path.join(base_dir, 'query2optimizers.json'), 'rb') as f:
        query2optimizers = json.load(f)
    tolog_dir = os.path.abspath(os.path.join(base_dir, './in/'))
    found_files = set([os.path.basename(fn) for fn in glob.glob(tolog_dir + '/*.tl')])
    baseline_dir = os.path.join(base_dir, './baseline/')
    for fn in query2optimizers:
        if fn in _IGNORE:
            continue
        found_files.remove(fn)
        optimizers = ['query-c14n']
        optimizers.extend(query2optimizers[fn])
        filename = os.path.join(tolog_dir, fn)
        f = open(filename, 'rb')
        # 1. Apply optimizers and return tolog
        tl = tolog.convert_to_tolog(f, optimizers=optimizers)
        # 2. Parse created tolog+
        try:
            tree = tolog.parse_to_etree(tl, iri='http://www.example.org/mql-tolog/', tolog_plus=False)
        except Exception, ex:
            fail('Error: %r in %s' % (ex, tl))
        # 3. Apply optimizers to the newly parsed query
        res = xsl.apply_transformations(tree, optimizers)
        out = io.BytesIO()
        res.write_c14n(out)
        expected = io.open(os.path.join(baseline_dir, fn + '.c14n'), encoding='utf-8').read()
        yield eq_, expected, out.getvalue(), 't: %s' % fn
    for fn in _IGNORE:
        found_files.remove(fn)
    if found_files:
        raise Exception('Found more files in the directory: %r' % found_files)


if __name__ == '__main__':
    import nose
    nose.core.runmodule()
