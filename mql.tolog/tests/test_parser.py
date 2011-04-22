# -*- coding: utf-8 -*-
#
# Copyright (c) 2010 - 2011 -- Lars Heuer - Semagia <http://www.semagia.com/>.
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
Tests against the parser.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD License
"""
from tm.mql import InvalidQueryError
import mql.tolog as tolog
from mql.tolog.handler import NoopParserHandler

def parse(data, handler=None):
    tolog.parse(data, handler or NoopParserHandler())

def fail(msg):
    raise AssertionError(msg)

def test_duplicate_prefixes_invalid():
    def check(data):
        try:
            parse(data)
            fail('Expected an error since x is bound to different IRIs')
        except InvalidQueryError:
            pass
    data = ('''using x for i"http://www.semagia.com/test"
using x for i"http://www.example.org/"
''',
            '''%prefix x <http://www.semagia.com/>
%prefix x <http://www.example.org/>
''',
            '''using x for i"http://www.semagia.com/test"
%prefix x <http://www.semagia.com/>''',
            )
    for d in data:
        yield check, d

def test_duplicate_prefixes():
    data = ('''%prefix x <http://www.semagia.com/>
%prefix x <http://www.semagia.com/>
''',
            # Probably rejected by Ontopia
            '''using x for i"http://www.semagia.com/test"
using x for i"http://www.semagia.com/test"
''',
            )
    for d in data:
        yield parse, d


if __name__ == '__main__':
    import nose
    nose.core.runmodule()

