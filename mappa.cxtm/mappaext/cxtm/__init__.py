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
from .cxtm1 import CXTMTopicMapWriter

def create_writer(out, base, version=None, **kw):
    """\
    
    """
    if version and version != 1.0:
        raise IOError('CXTM version "%s" is not supported' % str(version))
    return CXTMTopicMapWriter(out=out, base=base)
