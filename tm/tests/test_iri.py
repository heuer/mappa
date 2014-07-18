# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
Tests against the ``tm.irilib``.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
from nose.tools import eq_
from tm.irilib import normalize, resolve_iri



def test_mark_wilhelm_kuester():
    # Test against issue #15.
    # http://code.google.com/p/mappa/issues/detail?id=15
    iri = 'http://psi.ontopedia.net/Marc_Wilhelm_K%c3%bcster'
    eq_('http://psi.ontopedia.net/Marc_Wilhelm_K%C3%BCster', normalize(iri))


def test_tilde():
    reference = "http://www.semagia.com/home/~lars"
    eq_(reference, normalize("http://www.semagia.com/home/%7Elars"))
    eq_(reference, normalize("http://www.semagia.com/home/%7elars"))


def test_RFC_3986__5_4_1_Normal_Examples():
    iris = [
            ("g:h", "g:h"),
            ("g", "http://a/b/c/g"),
            ("./g", "http://a/b/c/g"),
            ("/g", "http://a/g"),
            ('//g', 'http://g'),
            # Moved into sadlyfail for the time being
            #("?y", "http://a/b/c/d;p?y"),
            ("g?y", "http://a/b/c/g?y"),
            ("#s", "http://a/b/c/d;p?q#s"),
            ("g#s", "http://a/b/c/g#s"),
            ("g?y#s", "http://a/b/c/g?y#s"),
            (";x", "http://a/b/c/;x"),
            ("g;x", "http://a/b/c/g;x"),
            ("g;x?y#s", "http://a/b/c/g;x?y#s"),
            ("", "http://a/b/c/d;p?q"),
            (".", "http://a/b/c/"),
            ("./", "http://a/b/c/"),
            ("..", "http://a/b/"),
            ("../", "http://a/b/"),
            ("../g", "http://a/b/g"),
            ("../..", "http://a/"),
            ("../../", "http://a/"),
            ("../../g", "http://a/g")
    ]
    base = 'http://a/b/c/d;p?q'
    for ref, expected in iris:
        result = resolve_iri(base, ref)
        eq_(expected, result, 'Expected: "%s", got: "%s" ("%s" against "%s")' % (expected, result, ref, base))


def test_sadlyfailing_RFC_3986__5_4_1_Normal_Examples():
    # Collects tests which fail but shoudln't
    iris = [
            ("?y", "http://a/b/c/d;p?y"),
    ]
    base = 'http://a/b/c/d;p?q'
    for ref, expected in iris:
        result = resolve_iri(base, ref)
        eq_(expected, result, 'Expected: "%s", got: "%s" ("%s" against "%s")' % (expected, result, ref, base))


def test_RFC_3986__5_4_2_Abnormal_Examples():
    iris = [
            ("../../../g", "http://a/g"),
            ("../../../../g", "http://a/g"),
            ("/./g", "http://a/g"),
            ("/../g", "http://a/g"),
            ("g.", "http://a/b/c/g."),
            (".g", "http://a/b/c/.g"),
            ("g..", "http://a/b/c/g.."),
            ("..g", "http://a/b/c/..g"),
            ("./../g", "http://a/b/g"),
            ("./g/.", "http://a/b/c/g/"),
            ("g/./h", "http://a/b/c/g/h"),
            ("g/../h", "http://a/b/c/h"),
            ("g;x=1/./y", "http://a/b/c/g;x=1/y"),
            ("g;x=1/../y", "http://a/b/c/y"),
            ("g?y/./x", "http://a/b/c/g?y/./x"),
            ("g?y/../x", "http://a/b/c/g?y/../x"),
            ("g#s/./x", "http://a/b/c/g#s/./x"),
            ("g#s/../x", "http://a/b/c/g#s/../x"),
            ("http:g", "http:g")
    ]
    base = "http://a/b/c/d;p?q"
    for ref, expected in iris:
        result = resolve_iri(base, ref)
        eq_(expected, result, 'Expected: "%s", got: "%s" ("%s" against "%s")' % (expected, result, ref, base))


def test_RFC_3986__6_2_2_Syntax_Based_Normalization():
    eq_("http://a/b/c/%7Bfoo%7D", normalize("hTTp://a/./b/../b/%63/%7bfoo%7d"))


def test_RFC_3986__6_2_3_Scheme_Based_Normalization():
    eq_("mailto:Joe@example.com", normalize("mailto:Joe@Example.COM"))


def test_form_encoded():
    eq_('http://www.example.org/test%20me/', normalize('http://www.example.org/test+me/'))


def test_preserve_empty():
    # According to RFC 3986 an empty fragment / query has to be kept and
    # must not be stripped away from the address.
    ref = 'http://www.semagia.com/x?'
    eq_(ref, normalize(ref))
    ref = 'http://www.semagia.com/x#'
    eq_(ref, normalize(ref))


def test_normalize_default_port():
    normalized = 'http://www.semagia.com/'
    eq_(normalized, normalize('http://www.semagia.com:80'))
    eq_(normalized, normalize('http://www.semagia.com:80/'))
    eq_(normalized, normalize('http://www.semagia.com:/'))


def test_normalize_scheme():
    eq_('http://www.semagia.com/', normalize('HTtp://www.semagia.com/'))
    eq_('http://www.semagia.com/', normalize('HTTP://www.semagia.com/'))
    eq_('mailto:john@example.org', normalize('mAILTO:john@example.org'))
    eq_('mailto:Joe@example.org', normalize('mAILTO:Joe@example.org'))


def test_normalize_userinfo():
    iris = [
            "http://lars:@semagia.com/",
            "http://lars:xyz@semagia.com/",
            "http://lars:80@semagia.com/",
            "http://lars:xyz@semagia.com:8080/",
    ]
    for iri in iris:
        eq_(iri, normalize(iri))
    eq_("http://lars:@semagia.com/", normalize("http://lars:@semagia.com:/"))
    eq_("http://lars:xyz@semagia.com/", normalize("http://lars:xyz@semagia.com:80/"))
    eq_("http://lars:@semagia.com/", normalize("http://lars:@semagia.com:"))


def test_windows_normalization():
    eq_('file:///E:/somewhere/bla.ctm', normalize('file:///E|/somewhere/bla.ctm'))
    eq_('file://localhost/E:/somewhere/bla.ctm', normalize('file://localhost/E|/somewhere/bla.ctm'))


if __name__ == '__main__':
    import nose
    nose.core.runmodule()
