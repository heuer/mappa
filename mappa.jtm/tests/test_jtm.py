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
from StringIO import StringIO
from nose.tools import ok_
from tm.voc import XSD
from mappaext.cxtm.cxtm_test import create_writer_cxtm_cases
from mio.jtm import create_deserializer
from mappaext.jtm import create_writer

def fail(msg):
    raise AssertionError(msg)

def create_jtm10_writer(out, base):
    return create_writer(out, base, version=1.0)

def create_jtm11_writer(out, base):
    writer = create_writer(out, base, version=1.1)
    writer.add_prefix('_', base)
    return writer

def test_jtm_10_writer():
    for test in create_writer_cxtm_cases(create_jtm10_writer, create_deserializer, 'jtm', 'jtm'):
        yield test

def test_jtm_11_writer():
    for test in create_writer_cxtm_cases(create_jtm11_writer, create_deserializer, 'jtm', 'jtm'):
        yield test
    for test in create_writer_cxtm_cases(create_jtm11_writer, create_deserializer, 'jtm11', 'jtm'):
        yield test

def test_add_prefix11():
    iri = 'http://www.semagia.com/'
    writer = create_jtm11_writer(StringIO(), iri)
    writer.add_prefix('x', iri)
    ok_('x' in writer.prefixes)
    ok_(iri == writer.prefixes['x'])

def test_prefixes_keyword_arg():
    iri = 'http://www.semagia.com/'
    writer = writer = create_writer(StringIO(), iri, version=1.1, prefixes={'x': iri})
    ok_('x' in writer.prefixes)
    ok_(iri == writer.prefixes['x'])

def test_add_prefix10():
    iri = 'http://www.semagia.com/'
    writer = create_jtm10_writer(StringIO(), iri)
    try:
        writer.add_prefix('x', iri)
        fail('Expected an error for registering a prefix in JTM 1.0')
    except ValueError:
        pass

def test_add_xsd_prefix():
    iri = 'http://www.semagia.com/'
    writer = create_jtm11_writer(StringIO(), iri)
    writer.add_prefix('Xsd', XSD)
    writer.add_prefix('xsd', XSD)
    writer.add_prefix('XSD', XSD)

def test_add_xsd_prefix_invalid():
    iri = 'http://www.semagia.com/'
    writer = create_jtm11_writer(StringIO(), iri)
    try:
        writer.add_prefix('Xsd', iri)
        fail('The prefix "xsd" is reserved')
    except ValueError:
        pass


if __name__ == '__main__':
    import nose
    nose.core.runmodule()
