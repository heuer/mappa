# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
Linear Topic Maps Notation (LTM) 1.3 lexer.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
import re
from tm.mio import MIOException

directives = {
    'PREFIX': 'DIR_PREFIX',
    'VERSION': 'DIR_VERSION',
    'TOPICMAP': 'DIR_TOPICMAP',
    'MERGEMAP': 'DIR_MERGEMAP',
    'INCLUDE': 'DIR_INCLUDE',
    'BASEURI': 'DIR_BASEURI',
    }

tokens = tuple(directives.values()) + (
    # Identifiers
    'IDENT',
    'QNAME',

    # Literals
    'STRING', 'DATA',

    # Delimiters [ ] { } ( ) , ; : ~ = @ / %
    'LBRACK', 'RBRACK',
    'LCURLY', 'RCURLY',
    'LPAREN', 'RPAREN',
    'COMMA', 'SEMI', 'COLON', 'TILDE', 'EQ', 'AT', 'SLASH', 'PERCENT',
)

t_IDENT = r'[a-zA-Z_][\-\.\w]*'
t_LBRACK = r'\['
t_RBRACK = r'\]'
t_LCURLY = r'{'
t_RCURLY = r'}'
t_LPAREN = r'\('
t_RPAREN = r'\)'
t_COLON = r':'
t_COMMA = r','
t_SEMI = r';'
t_TILDE = r'~'
t_EQ = r'='
t_AT = r'@'
t_SLASH = r'/'
t_PERCENT = r'%'

def t_error(t):
    raise MIOException('Unexpected token "%r"' % t)

def t_newline(t):
    r'[\r\n]+'
    t.lineno += len(t.value)

def t_ws(t):    # Disable unsused arg msg: pylint: disable-msg=W0613
    r'[\t ]+'
    pass

def t_comment(t):
    r'/\*([^*]|\*[^/])*\*/'
    t.lineno += t.value.count('\n')

def t_QNAME(t):
    t.value = t.value.split(':')
    return t

t_QNAME.__doc__ = r':'.join([t_IDENT, t_IDENT]) # Disable redefine __doc__ msg: pylint: disable-msg=W0622

def t_STRING(t):
    r'"([^"]|"{2})*"'
    val = t.value[1:-1].replace('""', '"')
    if not isinstance(val, unicode):
        val = unicode(val, 'utf-8')
    t.value = unescape_unicode(val)
    t.lineno += t.value.count('\n')
    return t

def t_DATA(t):
    r'\[\[([^\]]|\](?!\]))*\]\]'
    t.value = unescape_unicode(t.value[2:-2])
    t.lineno += t.value.count('\n')
    return t

def t_directive(t):
    r'\#[A-Z]+'
    t.type = directives.get(t.value[1:])
    if not t.type:
        raise MIOException('Unknown directive "%s"' % t.value)
    return t


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
                    buff.append(u'\\u')
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