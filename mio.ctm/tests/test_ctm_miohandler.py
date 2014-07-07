# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
Tests against the CTM 1.0 MIOHandler

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
from nose.tools import eq_, ok_
from StringIO import StringIO
import codecs
import mappa
from mappa.miohandler import MappaMapHandler
from mappaext.cxtm.cxtm_test import find_valid_cxtm_cases, get_baseline
from mappaext.cxtm import create_writer
from tm import Source
from tm.mio import MIOException, SUBJECT_IDENTIFIER
from mio.ctm import create_deserializer, CTMHandler
from mio import xtm


def fail(msg):
    raise AssertionError(msg)


def check_handler(deserializer_factory, filename):
    src = Source(file=open(filename))
    # 1. Generate CTM 1.0 via CTMHandler
    out = StringIO()
    deser = deserializer_factory()
    handler = CTMHandler(out)
    handler.add_prefix(u'_', src.iri + u'#')
    deser.handler = handler
    try:
        deser.parse(src)
    except MIOException, ex:
        fail('failed: %s.\nError: %s' % (filename, ex))            
    # 2. Read the generated CTM
    conn = mappa.connect()
    tm = conn.create(u'http://www.semagia.com/test-ctm-handler')
    deser = create_deserializer()
    deser.handler = MappaMapHandler(tm)
    new_src = Source(data=out.getvalue(), iri=src.iri)
    try:
        deser.parse(new_src)
    except MIOException, ex:
        fail('failed: %s.\nError: %s\nGenerated CTM: %s' % (filename, ex, out.getvalue()))
    # 3. Generate the CXTM
    f = codecs.open(get_baseline(filename), encoding='utf-8')
    expected = f.read()
    f.close()
    result = StringIO()
    c14n = create_writer(result, src.iri)
    c14n.write(tm)
    res = unicode(result.getvalue(), 'utf-8')
    if expected != res:
        fail('failed: %s.\nExpected: %s\nGot: %s\nGenerated CTM: %s' % (filename, expected, res, out.getvalue()))


def test_ctm():
    excluded = ['occurrence-string-multiline2.ctm', 'tm-reifier2.ctm']
    for filename in find_valid_cxtm_cases('ctm', 'ctm', exclude=excluded):
        yield check_handler, create_deserializer, filename

_EXCLUDE_XTM = [
                # Constructs != topic which have an iid
                "association-duplicate-iid.xtm",
                "association-duplicate-iid2.xtm",
                "association-duplicate-iid3.xtm",
                "association-duplicate-reified2.xtm",
                "association-duplicate-reified3.xtm",
                "association-duplicate-reified4.xtm",
                "itemid-association.xtm",
                "itemid-name.xtm",
                "itemid-occurrence.xtm",
                "itemid-role.xtm",
                "itemid-tm.xtm",
                "itemid-variant.xtm",
                "mergemap-itemid.xtm",
                "name-duplicate-iid.xtm",
                "name-duplicate-reified3.xtm",
                "name-duplicate-reified4.xtm",
                "occurrence-duplicate-iid.xtm",
                "occurrence-duplicate-iid2.xtm",
                "role-duplicate-iid.xtm",
                "role-duplicate-iid2.xtm",
                "variant-duplicate-iid.xtm"
    ]


def test_xtm_20():
    for filename in find_valid_cxtm_cases('xtm2', 'xtm', exclude=_EXCLUDE_XTM):
        yield check_handler, xtm.create_deserializer, filename


def test_xtm_21():
    for filename in find_valid_cxtm_cases('xtm21', 'xtm', exclude=_EXCLUDE_XTM):
        yield check_handler, xtm.create_deserializer, filename


class TestPrefixes:

    def make_handler(self, out=None):
        if out == None:
            out = StringIO()
        return CTMHandler(out)

    def test_registering(self):
        handler = self.make_handler()
        eq_(0, len(handler.prefixes))
        prefix, iri = 'base', 'http://www.semagia.com/base'
        handler.add_prefix(prefix, iri)
        prefixes = handler.prefixes
        eq_(1, len(prefixes))
        eq_(iri, prefixes[prefix])
        new_iri = iri + '/something-different'
        prefixes[prefix] = new_iri
        eq_(new_iri, prefixes[prefix])
        # The IRI must not have changed at the handler
        eq_(iri, handler.prefixes[prefix])
        handler.remove_prefix(prefix)
        ok_(prefix not in handler.prefixes)
        handler.add_prefix(prefix, iri)
        eq_(iri, handler.prefixes[prefix])
        handler.add_prefix(prefix, iri)
        eq_(iri, handler.prefixes[prefix])
        handler.add_prefix(prefix, new_iri)
        eq_(new_iri, handler.prefixes[prefix])

    def test_registering_illegal(self):
        handler = self.make_handler()
        try:
            handler.add_prefix('.aaa', 'http://www.semagia.com/')
            fail('Expected an exception, illegal CTM identifier as prefix')
        except ValueError:
            pass
        try:
            handler.add_prefix('', 'http://www.semagia.com/')
            fail('Expected an exception, illegal CTM identifier as prefix')
        except ValueError:
            pass
        try:
            handler.add_prefix(None, 'http://www.semagia.com/')
            fail('Expected an exception, illegal CTM identifier as prefix')
        except ValueError:
            pass
        try:
            handler.add_prefix('a', '')
            fail('Expected an exception, illegal CTM IRI')
        except ValueError:
            pass
        try:
            handler.add_prefix('a', None)
            fail('Expected an exception, illegal CTM IRI')
        except ValueError:
            pass
        try:
            handler.add_prefix('a', 'http://www.{semagia}.com/')
            fail('Expected an exception, illegal CTM IRI')
        except ValueError:
            pass

    def test_illegal_removal(self):
        out = StringIO()
        handler = self.make_handler(out)
        prefix, iri = 'base', 'http://www.semagia.com/base'
        handler.add_prefix(prefix, iri)
        handler.startTopicMap()
        try:
            handler.remove_prefix(prefix)
            fail('A prefix must not be removable once it is serialized')
        except MIOException:
            pass

    def test_illegal_add(self):
        out = StringIO()
        handler = self.make_handler(out)
        prefix, iri = 'base', 'http://www.semagia.com/base'
        handler.add_prefix(prefix, iri)
        handler.startTopicMap()
        # Legal: Reusing the prefix with the same IRI is allowed
        handler.add_prefix(prefix, iri)
        new_iri = iri + '/something-different'
        try:
            handler.add_prefix(prefix, new_iri)
            fail('A prefix must not be modifiable once it is serialized')
        except MIOException:
            pass
        out = StringIO()
        handler = self.make_handler(out)
        handler.startTopicMap()
        handler.startTopic((SUBJECT_IDENTIFIER, 'http://psi.semagia.com/bla'))
        try:
            handler.add_prefix(prefix, iri)
            fail("Within a topic, adding a prefix shouldn't be allowed")
        except MIOException:
            pass

    def test_legal_add_within_stream(self):
        out = StringIO()
        handler = self.make_handler(out)
        prefix, iri = 'base', 'http://www.semagia.com/base'
        handler.add_prefix(prefix, iri)
        handler.startTopicMap()
        prefix2, iri2 = 'p2', 'http://www.semagia.com/something-different'
        handler.add_prefix(prefix2, iri2)
        handler.endTopicMap()
        ok_('%%prefix %s <%s>' % (prefix, iri) in out.getvalue())
        ok_('%%prefix %s <%s>' % (prefix2, iri2) in out.getvalue())


class TestAdditionalInfo:

    def test_author(self):
        out = StringIO()
        handler = CTMHandler(out)
        ok_(handler.author is None)
        handler.author = 'Lars'
        eq_(u'Lars', handler.author)
        handler.startTopicMap()
        handler.endTopicMap()
        ok_("Author:   Lars" in out.getvalue())

    def test_title(self):
        out = StringIO()
        handler = CTMHandler(out)
        ok_(handler.title is None)
        handler.title = u'Test'
        eq_(u'Test', handler.title)
        handler.startTopicMap()
        handler.endTopicMap()
        ok_(u'''#
# ====
# Test
# ====
#
''' in out.getvalue())


if __name__ == '__main__':
    import nose
    nose.core.runmodule()
