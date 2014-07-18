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
from nose.tools import ok_, eq_
from tm.mio import syntax


def _syntaxes():
    for name in dir(syntax):
        if isinstance(getattr(syntax, name), syntax.Syntax):
            yield getattr(syntax, name)


def test_discovery_by_extension():
    ok_(syntax.XTM is syntax.syntax_for_extension('xtm'))
    ok_(syntax.XTM is syntax.syntax_for_extension('.xtm'))
    ok_(syntax.XTM is syntax.syntax_for_extension('xTm'))
    ok_(syntax.XTM is syntax.syntax_for_extension('.XTm'))
    ok_(syntax.CTM is syntax.syntax_for_extension('ctm'))
    ok_(syntax.CTM is syntax.syntax_for_extension('.ctm'))
    ok_(syntax.CTM is syntax.syntax_for_extension('.tmcl'))
    ok_(syntax.LTM is syntax.syntax_for_extension('ltm'))
    ok_(syntax.LTM is syntax.syntax_for_extension('.ltm'))
    ok_(syntax.CXTM is syntax.syntax_for_extension('cxtm'))
    ok_(syntax.CXTM is syntax.syntax_for_extension('.cxtm'))


def test_discovery_by_mimetype():
    ok_(syntax.XTM is syntax.syntax_for_mimetype(syntax.XTM.mimetypes[0]))
    ok_(syntax.CTM is syntax.syntax_for_mimetype(syntax.CTM.mimetypes[0]))
    ok_(syntax.LTM is syntax.syntax_for_mimetype(syntax.LTM.mimetypes[0]))
    ok_(syntax.CXTM is syntax.syntax_for_mimetype(syntax.CXTM.mimetypes[0]))


def test_discovery_by_name():
    for syn in _syntaxes():
        print syn
        ok_(syn is syntax.syntax_for_name(syn.name))
        ok_(syn is syntax.syntax_for_name(syn.name.upper()))
        ok_(syn is syntax.syntax_for_name(syn.name.lower()))


if __name__ == '__main__':
    import nose
    nose.core.runmodule()
