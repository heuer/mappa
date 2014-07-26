# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
A ``TopicMapWriter`` implementation that serializes a topic map into
`JSON Topic Maps (JTM) <http://www.cerny-online.com/jtm/>`_ representation.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
from mappaext.jtm import jtmwriter


def create_writer(out, base, version=1.1, prettify=False,
                  export_iids=True, omit_loners=False, prefixes=None, **kw):
    """\
    
    """
    if version and version not in (1.0, 1.1):
        raise IOError('JTM version "%s" is not supported' % str(version))
    writer = jtmwriter.JTMTopicMapWriter(out, base, version=version or 1.1, prefixes=prefixes)
    writer.prettify = prettify
    writer.export_iids = export_iids
    writer.omit_loners = omit_loners
    return writer
