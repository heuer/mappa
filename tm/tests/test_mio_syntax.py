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
Tests against the mio.syntax module.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
from unittest import TestCase
from tm.mio import syntax

class TestMIOSyntax(TestCase):
    
    def _syntaxes(self):
        for name in dir(syntax):
            if isinstance(getattr(syntax, name), syntax.Syntax):
                yield getattr(syntax, name)
    
    def test_discovery_by_extension(self):
        self.assert_(syntax.XTM is syntax.syntax_for_extension('xtm'))
        self.assert_(syntax.XTM is syntax.syntax_for_extension('.xtm'))
        self.assert_(syntax.XTM is syntax.syntax_for_extension('xTm'))
        self.assert_(syntax.XTM is syntax.syntax_for_extension('.XTm'))
        self.assert_(syntax.CTM is syntax.syntax_for_extension('ctm'))
        self.assert_(syntax.CTM is syntax.syntax_for_extension('.ctm'))
        self.assert_(syntax.CTM is syntax.syntax_for_extension('.tmcl'))
        self.assert_(syntax.LTM is syntax.syntax_for_extension('ltm'))
        self.assert_(syntax.LTM is syntax.syntax_for_extension('.ltm'))
        self.assert_(syntax.CXTM is syntax.syntax_for_extension('cxtm'))
        self.assert_(syntax.CXTM is syntax.syntax_for_extension('.cxtm'))

    def test_discovery_by_mimetype(self):
        self.assert_(syntax.XTM is syntax.syntax_for_mimetype(syntax.XTM.mimetypes[0]))
        self.assert_(syntax.CTM is syntax.syntax_for_mimetype(syntax.CTM.mimetypes[0]))
        self.assert_(syntax.LTM is syntax.syntax_for_mimetype(syntax.LTM.mimetypes[0]))
        self.assert_(syntax.CXTM is syntax.syntax_for_mimetype(syntax.CXTM.mimetypes[0]))

    def test_discovery_by_name(self):
        for syn in self._syntaxes():
            print syn
            self.assert_(syn is syntax.syntax_for_name(syn.name))
            self.assert_(syn is syntax.syntax_for_name(syn.name.upper()))
            self.assert_(syn is syntax.syntax_for_name(syn.name.lower()))

if __name__ == '__main__':
    import nose
    nose.core.runmodule()
