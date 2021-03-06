# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
Tests against the XTM content handler.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:version:      $Rev: 402 $ - $Date: 2011-01-14 16:30:38 +0100 (Fr, 14 Jan 2011) $
:license:      BSD license
"""
from nose.tools import ok_
from xml import sax
import io
from tm.mio.handler import MapHandler
from mio.xtm import XTMContentHandler
from mio.xtm.xtm1 import XTM10ContentHandler
from mio.xtm.xtm2 import XTM2ContentHandler


def _parse(source):
    ch = XTMContentHandler()
    ch.map_handler = MapHandler()
    ch.doc_iri = 'http://www.semagia.com/'
    parser = sax.make_parser()
    parser.setFeature(sax.handler.feature_namespaces, True)
    parser.setContentHandler(ch)
    parser.parse(io.StringIO(source))
    return ch._content_handler


def test_xtm10_detection():
    ch = _parse(u'<topicMap xmlns="http://www.topicmaps.org/xtm/1.0/"></topicMap>')
    ok_(isinstance(ch, XTM10ContentHandler))


def test_xtm10_detection2():
    ch = _parse(u'<topicMap></topicMap>')
    ok_(isinstance(ch, XTM10ContentHandler))


def test_xtm20_detection1():
    ch = _parse(u'<topicMap version="2.0"></topicMap>')
    ok_(isinstance(ch, XTM2ContentHandler))


def test_xtm20_detection2():
    ch = _parse(u'<topicMap xmlns="http://www.topicmaps.org/xtm/" version="2.0"></topicMap>')
    ok_(isinstance(ch, XTM2ContentHandler))


def test_xtm21_detection1():
    ch = _parse(u'<topicMap version="2.1"></topicMap>')
    ok_(isinstance(ch, XTM2ContentHandler))


def test_xtm21_detection2():
    ch = _parse(u'<topicMap xmlns="http://www.topicmaps.org/xtm/" version="2.1"></topicMap>')
    ok_(isinstance(ch, XTM2ContentHandler))


if __name__ == '__main__':
    import nose
    nose.core.runmodule()
