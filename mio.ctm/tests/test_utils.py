# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2011 -- Lars Heuer - Semagia <http://www.semagia.com/>.
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
Tests against mio.ctm.utils

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
from nose.tools import eq_
from mio.ctm.utils import *

def test_is_native_datatype():
    eq_(False, is_native_datatype(XSD.string))
    eq_(True, is_native_datatype(XSD.integer))
    eq_(True, is_native_datatype('http://www.w3.org/2001/XMLSchema#dateTime'))
    eq_(True, is_native_datatype('http://psi.topicmaps.org/iso13250/ctm-integer'))

def test_keyword_valid():
    eq_(True, is_keyword('isa'))
    eq_(True, is_keyword('ako'))
    eq_(True, is_keyword('def'))
    eq_(True, is_keyword('end'))
    eq_(True, is_keyword(u'end'))

def test_keyword_invalid():
    eq_(False, is_keyword('isa '))
    eq_(False, is_keyword('ISA'))

def test_iri_valid():
    data = ('http://www.semagia.com/',)
    for iri in data:
        eq_(True, is_valid_iri(iri))

def test_iri_invalid():
    data = ('<http://www.semagia.com/>', 'http://{www.semagia.com/}',
            'http:// www.semagia.com/',)
    for iri in data:
        eq_(False, is_valid_iri(iri))

def test_valid_id_start():
    data = ('_', 'A', 'a', u'ü', u'ä')
    for c in data:
        eq_(True, is_valid_id_start(c))

def test_invalid_id_start():
    data = ('0', '-', '.')
    for c in data:
        eq_(False, is_valid_id_start(c))

def test_valid_localid_start():
    data = ('0', u'ü',)
    for c in data:
        eq_(True, is_valid_localid_start(c))

def test_invalid_localid_start():
    data = ('.', '-')
    for c in data:
        eq_(False, is_valid_localid_start(c))

def test_valid_id_part():
    data = ('-', '.', '0', 'a', u'ä', u'ö', u'ü', u'_')
    for c in data:
        eq_(True, is_valid_id_part(c))

def test_invalid_id_part():
    data = (' ',)
    for c in data:
        eq_(False, is_valid_id_part(c))

def test_valid_id():
    data = ('ident', '_ident', 'ident.ifier', 'a1976-09-19', 'isa', u'öüä')
    for c in data:
        eq_(True, is_valid_id(c))

def test_invalid_id():
    data = ('ident.', '-ident', '2ident.ifier', '.isa')
    for c in data:
        eq_(False, is_valid_id(c))

def test_valid_local_part():
    data = ('1976-09-19', '1semagia')
    for c in data:
        eq_(True, is_valid_local_part(c))

def test_invalid_local_part():
    data = ('1976-09-19.', '-semagia', '.semagia', '.1semagia')
    for c in data:
        eq_(False, is_valid_local_part(c))

def test_valid_iri_part():
    data = ('a', ')')
    for c in data:
        eq_(True, is_valid_iri_part(c))

def test_invalid_iri_part():
    data = (' ', '"')
    for c in data:
        eq_(False, is_valid_iri_part(c))

if __name__ == '__main__':
    import nose
    nose.core.runmodule()
