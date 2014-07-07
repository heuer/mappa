# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
Some utility functions to check (internal) model constraints.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD License
"""
from mappa.utils import is_topic
from mappa import ModelConstraintViolation


def check_not_none(obj):
    """\
    Raises a ValueError iff `obj` is None.
    """
    if obj is None:
        raise ValueError('The argument must not be None')


def check_same_topicmap(first, second):
    """\
    Raises a ``ModelConstraintViolation`` iff `first` and `second` do not belong
    to the same topic map instance. 
    """
    if first.tm != second.tm:
        raise ModelConstraintViolation('The Topic Maps constructs do not belong to the same topic map')


def check_reification_allowed(reifiable, new_reifier):
    """\
    Checks if the reification of `reifiable` through `reifier` is allowed.
    """
    reifier = reifiable.reifier
    if reifier == new_reifier or not new_reifier:
        return # Setting the reifier to the same value or to None causes no problems
    if new_reifier.reified:
        raise ModelConstraintViolation('The topic reifies another Topic Maps construct.', reporter=reifiable)
