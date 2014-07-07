# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
Constants and functions that may be useful to operate upon IRIs.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
from urlparse import urljoin


def resolve_iri(base, reference):
    """\
    Resolves the specified `reference` against the `base`.
    """
    if base[-1] == '#' and reference[0] != '#':
        return urljoin(base[:-1], '#' + reference)
    return urljoin(base, reference)

# All registered rootless schemes
ROOTLESS_SCHEMES = (
                    'urn',          # RFC 2141
                    'mailto',       # RFC 2368
                    'mid', 'cid',   # RFC 2392
                    'data',         # RFC 2397
                    'service',      # RFC 2609
                    'tel', 'fax', 'modem',  # RFC 2806
                    'sip',          # RFC 3261
                    'h323',         # RFC 3508
                    'pres',         # RFC 3859
                    'im',           # RFC 3860
                    'tag',          # RFC 4151
                    'dns',          # RFC 4501
                   )
