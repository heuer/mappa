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
from mappaext.cxtm.cxtm_test import create_writer_cxtm_cases
from mio.xtm import create_deserializer
from mappaext import xtm

def create_xtm10_writer(out, base):
    return xtm.create_writer(out, base, prettify=True, version=1.0)

def create_xtm20_writer(out, base):
    return xtm.create_writer(out, base, prettify=True, version=2.0)

def create_xtm21_writer(out, base):
    return xtm.create_writer(out, base, prettify=True, version=2.1)

def test_xtm_10_writer():
    for test in create_writer_cxtm_cases(create_xtm10_writer, create_deserializer, 'xtm1', 'xtm',
                                         exclude=['reification-bug-1.xtm', 'reification-bug-2.xtm',
                                                  'tm-reifier.xtm', 'instanceof-equiv.xtm',
                                                  'association-reifier.xtm']):
        yield test

def test_xtm_20_writer():
    for test in create_writer_cxtm_cases(create_xtm20_writer, create_deserializer, 'xtm2', 'xtm'):
        yield test

def test_xtm_21_writer():
    for test in create_writer_cxtm_cases(create_xtm21_writer, create_deserializer, 'xtm21', 'xtm'):
        yield test


if __name__ == '__main__':
    import nose
    nose.core.runmodule()
