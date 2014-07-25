# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
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
