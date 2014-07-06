# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
This module provides the unescaping of Unicode escape sequences.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
import re

_ESC_UNICODE = re.compile(r'\\u([0-9A-Fa-f]{4,6})')

def unescape_unicode(s):
    """\
    Unescapes a LTM string.
    
    `s`
        The string to unescape.
    """
    match = _ESC_UNICODE.search(s)
    if not match:
        return s
    buff = []
    pos = 0
    while match:
        buff.append(s[pos:match.start()])
        start = match.start(1)
        end = match.end()
        pos = end
        unicode_value = None
        to_add = ''
        try: 
            xx = match.group(1)
            unicode_value = int(xx, 16)
        except ValueError:
            try:
                xx = xx[:-1]
                if len(xx) < 4:
                    raise ValueError()
                unicode_value = int(xx, 16)
                to_add = s[end-1]
            except ValueError:
                try:
                    xx = xx[:-1]
                    if len(xx) < 4:
                        raise ValueError()
                    unicode_value = int(xx, 16)
                    to_add = s[end-2:end]
                except ValueError: # Invalid Unicode escape sequence
                    buff.append('\\u')
                    buff.append(s[start:end])
                    pos = match.end()-3
        if unicode_value is not None:
            if unicode_value < 65536:
                buff.append(unichr(unicode_value))
            else:
                high_surrogate = (unicode_value + 56557568) / 1024
                low_surrogate = unicode_value + 56613888 - 1024 * high_surrogate
                buff.append(unichr(high_surrogate))
                buff.append(unichr(low_surrogate))
            buff.append(to_add)
        match = _ESC_UNICODE.search(s, pos)
    buff.append(s[pos:])
    return unicode(''.join(buff))

