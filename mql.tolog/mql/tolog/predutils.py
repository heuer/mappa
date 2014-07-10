# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
Helper functions for the ``mql.tolog.predicates`` module.

This module provides functions for common tasks like filtering columns and
invoking a function for each element in one column and store the result in 
another column.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD License
"""
from operator import itemgetter
from itertools import tee, chain, ifilter, imap

__all__ = ['fill_column',
           'filter_column', 'filter_columns', 
           'produce_column', 'produce_columns', 
           ]

_first = itemgetter(0)
_second = itemgetter(1)

def fill_column(res, idx, iterable):
    """\
    Fills the column specified by its index `idx` with the `iterable`.
    """
    res[idx] = iterable
    return res

def filter_column(res, idx, pred):
    """\
    Filters the column indicated by ``idx`` by invoking ``pred`` for each
    element.
    
    Only those elements are kept where ``pred`` returns ``True``.
    """
    res[idx] = ifilter(pred, res[idx])
    return res

def filter_columns(res, idx1, idx2, pred):
    """\
    Filters the columns specified by `idx1` and `idx2` by invoking ``pred`` for
    every element in column ``idx1`` and ``idx2``.
    
    `pred`
        A predicate. The predicate is invoked with a tuple ``(x, y)`` where
        ``x`` is a value from the ``idx1`` column, and ``y`` is a value from
        the column specified by ``idx2``.
    """
    # Generator expr. does not work here: ((a, b) for a ... for b in....)
    # generates "ValueError: generator already executing" errors
    iter1, iter2 = tee(ifilter(pred, [(a, b) for a in res[idx1] for b in res[idx2]]))
    res[idx1] = imap(_first, iter1)
    res[idx2] = imap(_second, iter2)
    return res

def produce_column(res, idx1, idx2, func):
    """\
    Fills the column specified by `idx1` with values produced by
    invoking `func` for every element in the column specified by `idx2`.
    
    `func`
        A function which is invoked for every element in column ``idx2``.
    """
    res[idx1] = chain(*imap(func, res[idx2]))
    return res

def produce_columns(res, idx1, idx2, iterable, func):
    """\
    Fills column `idx1` and `idx2` by invoking `func` for every element in
    `iterable`.
    
    If the `func` returns a result, the current element in `iterable` is 
    part of column ``idx1`` and the result of the function is part of the 
    column ``idx2``.
    """
    iter1, iter2 = tee(((a, b) for a in iterable for b in func(a)))
    res[idx1] = imap(_first, iter1)
    res[idx2] = imap(_second, iter2)
    return res
