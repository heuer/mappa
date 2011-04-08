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
Utility functions that operate on iterables.

.. Warning::

    This module does not belong to the public API.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD License
"""
__all__ = ['all', 'exists', 'no', 'one_of', 'product']

from itertools import ifilter, ifilterfalse
# pylint: disable-msg=E0611, W0611, W0141, W0622
try:
    from itertools import product
except ImportError:
    def product(*args):
        # product('ABCD', 'xy') --> Ax Ay Bx By Cx Cy Dx Dy
        pools = map(tuple, args)
        result = [[]]
        for pool in pools:
            result = [x+[y] for x in result for y in pool]
        for prod in result:
            yield tuple(prod)


def one_of(iterable):
    """\
    Returns one element from the iterable or ``None``.
    """
    for i in iterable:
        return i
    return None

# Remove unused var warning for 'elem'
# pylint: disable-msg=W0612

def all(seq, pred=None):
    """\
    Returns ``True`` if pred(x) is true for every element in the iterable.
    """
    for elem in ifilterfalse(pred, seq):
        return False
    return True

def exists(seq, pred=None):
    """\
    Returns ``True`` if pred(x) is true for at least one element in the iterable.
    """
    for elem in ifilter(pred, seq):
        return True
    return False

def no(seq, pred=None):
    """\
    Returns ``True`` if pred(x) is false for every element in the iterable.
    """
    for elem in ifilter(pred, seq):
        return False
    return True
