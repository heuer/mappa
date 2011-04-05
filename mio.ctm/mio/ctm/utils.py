# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2011 -- Lars Heuer - Semagia <http://www.semagia.com/>.
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
#     * Neither the project name nor the names of the contributors may be 
#       used to endorse or promote products derived from this software 
#       without specific prior written permission.
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
CTM utility functions.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
from tm import XSD

CTM_INTEGER = u'http://psi.topicmaps.org/iso13250/ctm-integer'

def is_native_datatype(iri):
    """\
    Returns if the provided datatype is supported by CTM natively (the value
    can be represented without quotes).
    """
    return iri in (XSD.decimal, XSD.integer, XSD.date, XSD.dateTime, CTM_INTEGER)

def is_keyword(ident):
    """\
    Returns if the provided identifier is a CTM keyword.
    """
    return ident in (u'isa', u'ako', u'def', u'end')

def is_valid_id_start(c):
    u"""\
    Returns if the provided character is a valid CTM identifier start char.
    
    >>> is_valid_id_start('_')
    True
    >>> is_valid_id_start('A')
    True
    >>> is_valid_id_start('.')
    False
    >>> is_valid_id_start('a')
    True
    >>> is_valid_id_start(u'ü')
    True
    >>> is_valid_id_start(u'ä')
    True
    >>> is_valid_id_start('-')
    False
    >>> is_valid_id_start('0')
    False
    """
    return c == u'_' \
            or u'A' <= c <= u'Z' \
            or u'a' <= c <= u'z' \
            or u'\u00C0' <= c <= u'\u00D6' \
            or u'\u00D8' <= c <= u'\u00F6' \
            or u'\u00F8' <= c <= u'\u02FF' \
            or u'\u0370' <= c <= u'\u037D' \
            or u'\u037F' <= c <= u'\u1FFF' \
            or u'\u200C' <= c <= u'\u200D' \
            or u'\u2070' <= c <= u'\u218F' \
            or u'\u2C00' <= c <= u'\u2FEF' \
            or u'\u3001' <= c <= u'\uD7FF' \
            or u'\uF900' <= c <= u'\uFDCF' \
            or u'\uFDF0' <= c <= u'\uFFFD' \
            or u'\u10000' <= c <= u'\uEFFFF'

def is_valid_localid_start(c):
    """\
    Returns if the provided character is valid start of the local part of 
    a CTM QName.
    
    >>> is_valid_localid_start('0')
    True
    >>> is_valid_localid_start('.')
    False
    >>> is_valid_localid_start('-')
    False
    >>> is_valid_localid_start(u'ü')
    True
    """
    return c.isdigit() or is_valid_id_start(c)

def is_valid_id_part(c):
    u"""\
    Returns if the provided character is a valid CTM part char.
    
    >>> is_valid_id_part('-')
    True
    >>> is_valid_id_part('.')
    True
    >>> is_valid_id_part('0')
    True
    >>> is_valid_id_part('a')
    True
    >>> is_valid_id_part(u'ä')
    True
    >>> is_valid_id_part(u'ö')
    True
    >>> is_valid_id_part(u'ü')
    True
    >>> is_valid_id_part(u'_')
    True
    """
    return is_valid_id_start(c) \
            or u'0' <= c <= u'9' \
            or c in u'.-\u00B7' \
            or u'\u0300' <= c <= u'\u036F' \
            or u'\u203F' <= c <= u'\u2040'

def is_valid_id(ident):
    u"""\
    Returns if the provided identifier is a valid CTM identifier.
    
    >>> is_valid_id('ident')
    True
    >>> is_valid_id('ident.')
    False
    >>> is_valid_id('-ident')
    False
    >>> is_valid_id('_ident')
    True
    >>> is_valid_id('ident.ifier')
    True
    >>> is_valid_id('2ident.ifier')
    False
    >>> is_valid_id('a1976-09-19')
    True
    >>> is_valid_id('.isa')
    False
    >>> is_valid_id('isa')
    True
    >>> is_valid_id(u'öüä')
    True
    """
    if not ident or ident[-1] == u'.' or not is_valid_id_start(ident[0]):
        return False
    for c in ident:
        if not is_valid_id_part(c):
            return False
    return True

def is_valid_local_part(ident):
    u"""\
    Returns if the identifier is a valid local part of a CTM QName.
    
    >>> is_valid_local_part('1976-09-19')
    True
    >>> is_valid_local_part('1976-09-19.')
    False
    >>> is_valid_local_part('-semagia')
    False
    >>> is_valid_local_part('.semagia')
    False
    >>> is_valid_local_part('1semagia')
    True
    >>> is_valid_local_part('.1semagia')
    False
    """
    if not ident or ident[-1] == u'.' or not is_valid_localid_start(ident[0]):
        return False
    for c in ident:
        if not is_valid_id_part(c):
            return False
    return True

def is_valid_iri_part(c):
    """\
    Returns if the provided character is valid within an ``<IRI>``.
    
    >>> is_valid_iri_part(' ')
    False
    >>> is_valid_iri_part('a')
    True
    >>> is_valid_iri_part('"')
    False
    >>> is_valid_iri_part(')')
    True
    """
    return c not in u' \n\r\t\f<>"`{}\\'

def is_valid_iri(iri):
    """\
    Returns if the provided IRI is valid acc. to CTM's rules for IRIs.
    
    `iri`
        An IRI (without ``<`` ``>`` delimiters)
    """
    if not iri:
        return False
    for c in iri:
        if not is_valid_iri_part(c):
            return False
    return True


_QUOT = {u't': u'\t', u'n': u'\n', u'r': u'\r', u'\\': u'\\', u'"': u'"'}

def unescape_string(s):
    """\
    Unescapes a CTM string.
    
    `s`
        The string to unescape.
    """
    backslash = s.find(u'\\')
    if backslash < 0:
        return s
    buff = []
    pos = 0
    length = len(s)
    while backslash != -1:
        buff.append(s[pos:backslash])
        if backslash +1 >= length:
            raise ValueError('Invalid escape syntax: in "%s"' % s)
        c = s[backslash+1]
        if c in _QUOT:
            buff.append(_QUOT[c])
            pos = backslash + 2
        elif c == u'u': #uxxxx
            if backslash + 5 >= length:
                raise ValueError('Incomplete Unicode escape sequence in: "%s"' % s)
            try:
                xx = s[backslash + 2 : backslash + 6]
                buff.append(unichr(int(xx, 16)))
                pos = backslash + 6
            except ValueError:
                raise ValueError('Illegal Unicode escape sequence "\\u%s" in "%s"' % (xx, s))
        elif c == u'U': #Uxxxxxx
            if backslash + 7 >= length:
                raise ValueError('Incomplete Unicode escape sequence in: "%s"' % s)
            try:
                xx = s[backslash + 2 : backslash + 8]
                buff.append(unichr(int(xx, 16)))
                pos = backslash + 8
            except ValueError:
                raise ValueError('Illegal Unicode escape sequence "\\U%s" in "%s"' % (xx, s))
        backslash = s.find(u'\\', pos)
    buff.append(s[pos:])
    return u''.join(buff)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
