# -*- coding: utf-8 -*-
#
# Copyright (c) 2011 -- Lars Heuer - Semagia <http://www.semagia.com/>.
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
Literal Utilities.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:version:      $Rev: 279 $ - $Date: 2009-11-29 18:35:34 +0100 (So, 29 Nov 2009) $
:license:      BSD license
"""
import re
from tm import XSD
try:
    from decimal import Decimal, InvalidOperation
except ImportError: # Python < 2.4
    Decimal = float
    InvalidOperation = ValueError

def normalize_literal(value, datatype):
    """\
    Normalizes the `value` if a normalization function exists for the
    provided `datatype`

    >>> normalize_literal('0001', XSD.integer)
    ('1', u'http://www.w3.org/2001/XMLSchema#integer')
    >>> normalize_literal('0001', 'http://psi.example.org/datatype')
    ('0001', 'http://psi.example.org/datatype')
    >>> normalize_literal('1', XSD.boolean)
    ('true', u'http://www.w3.org/2001/XMLSchema#boolean')
    >>> normalize_literal('.001', XSD.decimal)
    ('0.001', u'http://www.w3.org/2001/XMLSchema#decimal')
    """
    normalizer = _DATATYPE2NORMALIZER.get(datatype)
    if normalizer:
        return normalizer(value), datatype
    return value, datatype

_TRAILING_ZEROS_PATTERN = re.compile(r'[0-9](0+)$')

def normalize_decimal(val):
    """\
    Returns the canonical representation of a xsd:decimal value.
    
    >>> normalize_decimal('-.03')
    '-0.03'
    >>> normalize_decimal('+.03')
    '0.03'
    >>> normalize_decimal('+.0')
    '0.0'
    >>> normalize_decimal('-.0')
    '0.0'
    >>> normalize_decimal('0')
    '0.0'
    >>> normalize_decimal('.0')
    '0.0'
    >>> normalize_decimal('0.')
    '0.0'
    >>> normalize_decimal('0001.')
    '1.0'
    >>> normalize_decimal('0001')
    '1.0'
    >>> normalize_decimal('-001')
    '-1.0'
    >>> normalize_decimal('1.00000')
    '1.0'
    >>> normalize_decimal('123.4')
    '123.4'
    >>> normalize_decimal('123.400000000')
    '123.4'
    >>> normalize_decimal('123.000000400000000')
    '123.0000004'
    >>> normalize_decimal('0000123.4')
    '123.4'
    >>> normalize_decimal('0000.0')
    '0.0'
    >>> normalize_decimal('+0000.0')
    '0.0'
    >>> normalize_decimal('-0000.0')
    '0.0'
    >>> normalize_decimal('-123.4')
    '-123.4'
    >>> normalize_decimal(' -123.4    ')
    '-123.4'
    >>> normalize_decimal('-123.A')
    Traceback (most recent call last):
    ...
    ValueError: Illegal xsd:decimal: "-123.A"
    >>> normalize_decimal('A')
    Traceback (most recent call last):
    ...
    ValueError: Illegal xsd:decimal: "A"
    >>> normalize_decimal('A.b')
    Traceback (most recent call last):
    ...
    ValueError: Illegal xsd:decimal: "A.b"
    """
    try:
        res = str(Decimal(val))
    except InvalidOperation:
        raise ValueError('Illegal xsd:decimal: "%s"' % val)
    dot_idx = res.find('.')
    if dot_idx == -1:
        res = res + '.0'
    else:
        int_part, frac_part = res.split('.')
        m = _TRAILING_ZEROS_PATTERN.search(frac_part)
        if m:
            res = int_part + '.' + frac_part[:m.start(1)]
    if res == '-0.0':
        res = '0.0'
    return res

def normalize_boolean(val):
    """\
    Returns the canonical representation of a xsd:boolean value.
    
    >>> normalize_boolean('0')
    'false'
    >>> normalize_boolean('1')
    'true'
    >>> normalize_boolean('true')
    'true'
    >>> normalize_boolean('    true    ')
    'true'
    >>> normalize_boolean('false')
    'false'
    >>> normalize_boolean('')
    Traceback (most recent call last):
    ...
    ValueError: Illegal xsd:boolean: ""
    >>> normalize_boolean('2')
    Traceback (most recent call last):
    ...
    ValueError: Illegal xsd:boolean: "2"
    """
    v = val.strip()
    if v in ('0', 'false'):
        return 'false'
    if v in ('1', 'true'):
        return 'true'
    raise ValueError('Illegal xsd:boolean: "%s"' % val)

def normalize_integer(val):
    """\
    Returns the canonical representation of a xsd:integer value.
    
    >>> normalize_integer('-0')
    '0'
    >>> normalize_integer('00000')
    '0'
    >>> normalize_integer('+0')
    '0'
    >>> normalize_integer('-000100')
    '-100'
    >>> normalize_integer('+000100')
    '100'
    >>> normalize_integer(' +000100 ')
    '100'
    >>> normalize_integer('100')
    '100'
    >>> normalize_integer('')
    Traceback (most recent call last):
    ...
    ValueError: Illegal xsd:integer: ""
    """
    try:
        return str(int(val))
    except ValueError:
        raise ValueError('Illegal xsd:integer: "%s"' % val)

_DATATYPE2NORMALIZER = {
    XSD.decimal: normalize_decimal,
    XSD.integer: normalize_integer,
    XSD.boolean: normalize_boolean,
}

if __name__ == '__main__':
    import doctest
    doctest.testmod()
