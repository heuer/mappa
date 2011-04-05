# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2009 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#
#     * Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
#     * Neither the name of the project nor the names of the contributors 
#       may be used to endorse or promote products derived from this 
#       software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
#
"""\
Tests against the ``tm.irilib``.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
from unittest import TestCase
from tm.irilib import normalize, resolve_iri

class TestIRI(TestCase):
    
    def test_mark_wilhelm_kuester(self):
        # Test against issue #15.
        # http://code.google.com/p/mappa/issues/detail?id=15
        iri = 'http://psi.ontopedia.net/Marc_Wilhelm_K%c3%bcster'
        self.assertEqual('http://psi.ontopedia.net/Marc_Wilhelm_K%C3%BCster', normalize(iri))

    def test_tilde(self):
        reference = "http://www.semagia.com/home/~lars"
        self.assertEquals(reference, normalize("http://www.semagia.com/home/%7Elars"))
        self.assertEquals(reference, normalize("http://www.semagia.com/home/%7elars"))

    def test_RFC_3986__5_4_1_Normal_Examples(self):
        iris = [
                ("g:h", "g:h"),
                ("g", "http://a/b/c/g"),
                ("./g", "http://a/b/c/g"),
                ("/g", "http://a/g"),
                # Original: //g -> http://g
                # Changed to avoid problems with trailing slash normalizations
                ("//g/x", "http://g/x"),
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
            self.assertEqual(expected, result, 'Expected: "%s", got: "%s" ("%s" against "%s")' % (expected, result, ref, base))

    def test_sadlyfailing_RFC_3986__5_4_1_Normal_Examples(self):
        # Collects tests which fail but shoudln't
        iris = [
                ("?y", "http://a/b/c/d;p?y"),
        ]
        base = 'http://a/b/c/d;p?q'
        for ref, expected in iris:
            result = resolve_iri(base, ref)
            self.assertEqual(expected, result, 'Expected: "%s", got: "%s" ("%s" against "%s")' % (expected, result, ref, base))

    def test_RFC_3986__5_4_2_Abnormal_Examples(self):
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
            self.assertEqual(expected, result, 'Expected: "%s", got: "%s" ("%s" against "%s")' % (expected, result, ref, base))

    def test_RFC_3986__6_2_2_Syntax_Based_Normalization(self):
        self.assertEquals("http://a/b/c/%7Bfoo%7D", normalize("hTTp://a/./b/../b/%63/%7bfoo%7d"))

    def test_RFC_3986__6_2_3_Scheme_Based_Normalization(self):
        self.assertEquals("mailto:Joe@example.com", normalize("mailto:Joe@Example.COM"))

    def test_form_encoded(self):
        self.assertEqual('http://www.example.org/test%20me/', normalize('http://www.example.org/test+me/'))

    def test_preserve_empty(self):
        # According to RFC 3986 an empty fragment / query has to be kept and
        # must not be stripped away from the address.
        ref = 'http://www.semagia.com/x?'
        self.assertEqual(ref, normalize(ref))
        ref = 'http://www.semagia.com/x#'
        self.assertEqual(ref, normalize(ref))

    def test_normalize_default_port(self):
        normalized = 'http://www.semagia.com/'
        self.assertEqual(normalized, normalize('http://www.semagia.com:80'))
        self.assertEqual(normalized, normalize('http://www.semagia.com:80/'))
        self.assertEqual(normalized, normalize('http://www.semagia.com:/'))

    def test_normalize_scheme(self):
        self.assertEqual('http://www.semagia.com/', normalize('HTtp://www.semagia.com/'))
        self.assertEqual('http://www.semagia.com/', normalize('HTTP://www.semagia.com/'))
        self.assertEqual('mailto:john@example.org', normalize('mAILTO:john@example.org'))
        self.assertEqual('mailto:Joe@example.org', normalize('mAILTO:Joe@example.org'))

    def test_normalize_userinfo(self):
        iris = [
                "http://lars:@semagia.com/",
                "http://lars:xyz@semagia.com/",
                "http://lars:80@semagia.com/",
                "http://lars:xyz@semagia.com:8080/",
        ]
        for iri in iris:
            self.assertEqual(iri, normalize(iri))
        self.assertEquals("http://lars:@semagia.com/", normalize("http://lars:@semagia.com:/"))
        self.assertEquals("http://lars:xyz@semagia.com/", normalize("http://lars:xyz@semagia.com:80/"))
        self.assertEquals("http://lars:@semagia.com/", normalize("http://lars:@semagia.com:"))

if __name__ == '__main__':
    from test import test_support
    test_support.run_unittest(TestIRI)
