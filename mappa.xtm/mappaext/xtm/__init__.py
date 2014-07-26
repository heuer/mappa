# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\


:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
from __future__ import absolute_import
from . import xtm1, xtm2


def create_writer(out, base, version=None, prettify=False, export_iids=True, **kw):
    """\
    
    """
    cls = None
    if version in (None, 2.0, 2.1):
        cls = xtm2.XTM2TopicMapWriter
    elif version == 1.0:
        cls = xtm1.XTM10TopicMapWriter
    else:
        raise IOError('XTM version "%s" is not supported' % str(version)) 
    writer = cls(out, base, version=version)
    writer.prettify = prettify
    writer.export_iids = export_iids
    return writer
