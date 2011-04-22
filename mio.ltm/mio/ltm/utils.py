# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2009 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# Redistribution and use in source and binary forms, with or without
# modification, are permitted provided that the following conditions are
# met:
#
#     * Redistributions of source code must retain the above copyright
#       notice, this list of conditions and the following disclaimer.
#
#     * Redistributions in binary form must reproduce the above
#       copyright notice, this list of conditions and the following
#       disclaimer in the documentation and/or other materials provided
#       with the distribution.
#
#     * Neither the name of the project nor the names of the contributors 
#       may be used to endorse or promote products derived from this 
#       software without specific prior written permission.
#
# THIS SOFTWARE IS PROVIDED BY THE COPYRIGHT HOLDERS AND CONTRIBUTORS
# "AS IS" AND ANY EXPRESS OR IMPLIED WARRANTIES, INCLUDING, BUT NOT
# LIMITED TO, THE IMPLIED WARRANTIES OF MERCHANTABILITY AND FITNESS FOR
# A PARTICULAR PURPOSE ARE DISCLAIMED. IN NO EVENT SHALL THE COPYRIGHT
# OWNER OR CONTRIBUTORS BE LIABLE FOR ANY DIRECT, INDIRECT, INCIDENTAL,
# SPECIAL, EXEMPLARY, OR CONSEQUENTIAL DAMAGES (INCLUDING, BUT NOT
# LIMITED TO, PROCUREMENT OF SUBSTITUTE GOODS OR SERVICES; LOSS OF USE,
# DATA, OR PROFITS; OR BUSINESS INTERRUPTION) HOWEVER CAUSED AND ON ANY
# THEORY OF LIABILITY, WHETHER IN CONTRACT, STRICT LIABILITY, OR TORT
# (INCLUDING NEGLIGENCE OR OTHERWISE) ARISING IN ANY WAY OUT OF THE USE
# OF THIS SOFTWARE, EVEN IF ADVISED OF THE POSSIBILITY OF SUCH DAMAGE.
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

