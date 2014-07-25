# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
CTM utility functions.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
import re
from tm import XSD
from .lexer import VARIABLE

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
    """\
    Returns if the provided character is a valid CTM identifier start char.
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
            or u'\U00010000' <= c <= u'\U000EFFFF'


def is_valid_localid_start(c):
    """\
    Returns if the provided character is valid start of the local part of 
    a CTM QName.
    """
    return c.isdigit() or is_valid_id_start(c)


def is_valid_id_part(c):
    """\
    Returns if the provided character is a valid CTM part char.
    """
    return is_valid_id_start(c) \
            or u'0' <= c <= u'9' \
            or c in u'.-\u00B7' \
            or u'\u0300' <= c <= u'\u036F' \
            or u'\u203F' <= c <= u'\u2040'


def is_valid_id(ident):
    """\
    Returns if the provided identifier is a valid CTM identifier.
    """
    if not ident or ident[-1] == u'.' or not is_valid_id_start(ident[0]):
        return False
    for c in ident:
        if not is_valid_id_part(c):
            return False
    return True


def is_valid_local_part(ident):
    """\
    Returns if the identifier is a valid local part of a CTM QName.
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


_CHARS_TO_QUOT = {u't': u'\t', u'n': u'\n', u'r': u'\r', u'\\': u'\\', u'"': u'"'}


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
        if backslash + 1 >= length:
            raise ValueError('Invalid escape syntax: in "%s"' % s)
        c = s[backslash+1]
        if c in _CHARS_TO_QUOT:
            buff.append(_CHARS_TO_QUOT[c])
            pos = backslash + 2
        elif c == u'u':  # uxxxx
            if backslash + 5 >= length:
                raise ValueError('Incomplete Unicode escape sequence in: "%s"' % s)
            try:
                xx = s[backslash + 2:backslash + 6]
                buff.append(unichr(int(xx, 16)))
                pos = backslash + 6
            except ValueError:
                raise ValueError('Illegal Unicode escape sequence "\\u%s" in "%s"' % (xx, s))
        elif c == u'U':  # Uxxxxxx
            if backslash + 7 >= length:
                raise ValueError('Incomplete Unicode escape sequence in: "%s"' % s)
            try:
                xx = s[backslash + 2:backslash + 8]
                buff.append(unichr(int(xx, 16)))
                pos = backslash + 8
            except ValueError:
                raise ValueError('Illegal Unicode escape sequence "\\U%s" in "%s"' % (xx, s))
        backslash = s.find(u'\\', pos)
    buff.append(s[pos:])
    return u''.join(buff)


_FIND_VARS = re.compile(VARIABLE).finditer

def find_variables(data, omit_dollar=False):
    """\
    Returns all CTM variables from the provided data.

    `data`
        A string
    `omit_dollar`
        Indicates if the dollar sign (``$``) should be omitted (default: ``False``)
    """
    for m in _FIND_VARS(data):
        yield m.group()[1:] if omit_dollar else m.group()
   

if __name__ == '__main__':
    import doctest
    doctest.testmod()
