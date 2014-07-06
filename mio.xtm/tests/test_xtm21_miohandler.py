# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
Tests against the XTM 2.1 MIOHandler

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:version:      $Rev: 168 $ - $Date: 2009-06-26 14:22:56 +0200 (Fr, 26 Jun 2009) $
:license:      BSD license
"""
from StringIO import StringIO
import codecs
import mappa
from mappa.miohandler import MappaMapHandler
from mappaext.cxtm.cxtm_test import find_valid_cxtm_cases, get_baseline
from mappaext.cxtm import create_writer
from tm import Source
from mio.xtm import create_deserializer, XTM21Handler

def fail(msg):
    raise AssertionError(msg)

def check_handler(deserializer_factory, filename):
    src = Source(file=open(filename))
    # 1. Generate XTM 2.1 via XTM21Handler
    out = StringIO()
    deser = deserializer_factory()
    deser.handler = XTM21Handler(fileobj=out, prettify=True)
    deser.parse(src)
    # 2. Read the generated XTM 2.1
    tm = mappa.connect().create('http://www.semagia.com/test-xtm-handler')
    deser = create_deserializer()
    deser.handler = MappaMapHandler(tm)
    new_src = Source(data=out.getvalue(), iri=src.iri)
    try:
        deser.parse(new_src)
    except Exception, ex:
        fail('failed: %s.\nError: %s\nGenerated XTM 2.1: %s' % (filename, ex, out.getvalue()))
    # 3. Generate the CXTM
    f = codecs.open(get_baseline(filename), encoding='utf-8')
    expected = f.read()
    f.close()
    result = StringIO()
    c14n = create_writer(result, src.iri)
    c14n.write(tm)
    res = unicode(result.getvalue(), 'utf-8')
    if expected != res:
        fail('failed: %s.\nExpected: %s\nGot: %s\nGenerated XTM 2.1: %s' % (filename, expected, res, out.getvalue()))

def test_ctm():
    exclude = ["occurrence-string-multiline2.ctm",
               "string-escape.ctm",
               # Topic is serialized in advance of the tm reifier
               "tm-reifier2.ctm",
               ]
    try:
        from mio import ctm
        for filename in find_valid_cxtm_cases('ctm', 'ctm', exclude=exclude):
            yield check_handler, ctm.create_deserializer, filename
    except ImportError:
        pass

def test_jtm():
    exclude = [
               ]
    try:
        from mio import jtm
        for filename in find_valid_cxtm_cases('jtm', 'jtm', exclude=exclude):
            yield check_handler, jtm.create_deserializer, filename
        for filename in find_valid_cxtm_cases('jtm11', 'jtm', exclude=exclude):
            yield check_handler, jtm.create_deserializer, filename
    except ImportError:
        pass

def test_xtm_20():
    for filename in find_valid_cxtm_cases('xtm2', 'xtm'):
        yield check_handler, create_deserializer, filename

def test_xtm_21():
    for filename in find_valid_cxtm_cases('xtm21', 'xtm'):
        yield check_handler, create_deserializer, filename


if __name__ == '__main__':
    import nose
    nose.core.runmodule()
