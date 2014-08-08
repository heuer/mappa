# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
Topic Maps standard PSIs.

This module provides the standard PSIs used in Topic Maps. If you need one 
of the standard PSIs, you should use this module, rather than the `TM`
namespace provided by the ``tm.voc`` module to avoid typos. By convention,
the hyphen (``-``) in the PSIs is replaced by an underscore character (``_``)

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
from tm.voc import TM

__all__ = ()  # Avoid to expose something that pollutes the namespace, i.e. `type`

ctm = TM['ctm']
xtm = TM['xtm']

ctm_integer = TM['ctm-integer']

del TM
