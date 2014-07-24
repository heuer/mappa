# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
Tests mql.tolog.handler.SAXMediator.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD License
"""
import os
import io
import json
import glob
from nose.tools import eq_
from tm import xmlutils
from mql.tolog import parse_query, handler, convert_to_tolog_plus


_IGNORE = (
    'fold-type-assoc.tl',
    'tolog-tut-2-4_2.tl',
)


class NoopQueryHandler(handler.XMLParserHandler):
    """\

    """
    def __init__(self):
        self.ch = xmlutils.ETreeContentHandler()
        super(NoopQueryHandler, self).__init__(xmlutils.SAXSimpleXMLWriter(self.ch))

    query = property(lambda self: self.ch.etree)


def test_mediator():
    base_dir = os.path.abspath('./xsltests/')
    with open(os.path.join(base_dir, 'query2optimizers.json'), 'rb') as f:
        query2optimizers = json.load(f)
    tolog_dir = os.path.abspath(os.path.join(base_dir, './in/'))
    found_files = set([os.path.basename(fn) for fn in glob.glob(tolog_dir + '/*.tl')])
    baseline_dir = os.path.join(base_dir, './baseline/')
    for fn in query2optimizers:
        optimizers = ['query-c14n']
        optimizers.extend(query2optimizers[fn])
        filename = os.path.join(tolog_dir, fn)
        tolog_plus = convert_to_tolog_plus(open(filename, 'rb'), hints=True, optimizers=optimizers)
        with io.open(os.path.join(baseline_dir, fn), 'wb') as f_tplus:
            f_tplus.write(tolog_plus)
        if fn in _IGNORE:
            continue
        found_files.remove(fn)
        qh = NoopQueryHandler()
        q = parse_query(io.open(filename, 'rb'), qh, optimizers=optimizers)
        out = io.BytesIO()
        q.write_c14n(out)
        expected = io.open(os.path.join(baseline_dir, fn + '.c14n'), encoding='utf-8').read()
        yield eq_, expected, out.getvalue()
    for fn in _IGNORE:
        found_files.remove(fn)
    if found_files:
        raise Exception('Found more files in the directory: %r' % found_files)



if __name__ == '__main__':
    import nose
    nose.core.runmodule()
