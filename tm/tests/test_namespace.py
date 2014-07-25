# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
Tests against Namespace.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
from nose.tools import eq_
from tm import Namespace


def test_namespace_string():
    iri = 'http://www.example.org/bla'
    ns = Namespace(iri)
    eq_(iri, ns)


if __name__ == '__main__':
    import nose
    nose.core.runmodule()
