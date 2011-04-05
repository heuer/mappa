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

if __name__ == '__main__':
    import nose
    nose.core.runmodule()
