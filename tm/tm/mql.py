# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
Experimental module to provide common things for query languages.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
__all__ = ['QueryError', 'InvalidQueryError']


class QueryError(Exception):
    pass


class InvalidQueryError(QueryError):
    pass


class SyntaxQueryError(QueryError):
    pass
