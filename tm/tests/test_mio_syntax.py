# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
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
