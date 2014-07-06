# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
RDF to Topic Maps (RTM) standard PSIs.

This module provides the standard PSIs used in RTM. If you need one 
of the standard PSIs, you should use this module, rather than the `RDF2TM`
namespace provided by the ``tm.voc`` module to avoid typos. By convention,
the hyphen (``-``) in the PSIs is replaced by an underscore character (``_``)

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
from tm.voc import RDF2TM

__all__ = () # Avoid to expose something that pollutes the namespace, i.e. `type`

#pylint: disable-msg=W0622

maps_to = RDF2TM['maps-to']
type = RDF2TM['type']
in_scope = RDF2TM['in-scope']
subject_role = RDF2TM['subject-role']
object_role = RDF2TM['object-role']
basename = RDF2TM['basename']
occurrence = RDF2TM['occurrence']
association = RDF2TM['association']
instance_of = RDF2TM['instance-of']
subject_identifier = RDF2TM['subject-identifier']
subject_locator = RDF2TM['subject-locator']
source_locator = RDF2TM['source-locator']

del RDF2TM
