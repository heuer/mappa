# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
Literal Utilities.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
from __future__ import absolute_import
import re
from decimal import Decimal, InvalidOperation
from tm import XSD

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
        res = str(Decimal(val.strip()))
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
