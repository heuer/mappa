# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
TMDM standard PSIs.

This module provides the standard PSIs used in the TMDM. If you need one 
of the standard PSIs, you should use this module, rather than the `TMDM`
namespace provided by the ``tm.voc`` module to avoid typos. By convention,
the hyphen (``-``) in the PSIs is replaced by an underscore character (``_``)

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
from tm.voc import TMDM

__all__ = () # Avoid to expose something that pollutes the namespace, i.e. `type`

#pylint: disable-msg=W0622

topic_name = TMDM[u'topic-name']

sort = TMDM[u'sort']

type_instance = TMDM[u'type-instance']
type = TMDM[u'type']
instance = TMDM[u'instance']

supertype_subtype = TMDM[u'supertype-subtype']
supertype = TMDM[u'supertype']
subtype = TMDM[u'subtype']

del TMDM
