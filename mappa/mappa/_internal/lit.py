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
Module for literal / value handling.

.. Warning::

    This module does not belong to the public API.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD License
"""
import re
import base64
try:
    from decimal import Decimal
except ImportError:
    # Fallback for Py < 2.4
    Decimal = float
try:
    long
except NameError:
    # Fallback for Py >= 3.0
    long = int
    unicode = str
from tm.literalutils import normalize_literal
from operator import itemgetter
from datetime import date, time, datetime
from time import strptime
from mappa import XSD, irilib
from mappa._internal import kind

__all__ = ['Literal']

class Literal(tuple):
    """\
    Immutable representation of a value of a dedicated datatype.

    >>> lit = Literal('000.1', XSD.decimal)
    >>> lit.value
    u'0.1'
    >>> lit.datatype
    u'http://www.w3.org/2001/XMLSchema#decimal'
    >>> lit = Literal("Semagia")
    >>> lit.value
    u'Semagia'
    >>> lit.datatype
    u'http://www.w3.org/2001/XMLSchema#string'
    >>> lit.value = "Something"
    Traceback (most recent call last):
    ...
    AttributeError: can't set attribute
    >>> lit.datatype = "http://www.w3.org/2001/XMLSchema#int"
    Traceback (most recent call last):
    ...
    AttributeError: can't set attribute
    """
    _kind = kind.LITERAL
    __slots__ = ()

    def __new__(cls, value, datatype=None):
        if isinstance(value, Literal):
            return value
        if datatype is None:
            value, datatype = _value_datatype(value)
        if XSD.anyURI == datatype:
            return tuple.__new__(cls, (unicode(irilib.normalize(value)), unicode(datatype)))
        try:
            value, datatype = normalize_literal(value, datatype)
            return tuple.__new__(cls, (unicode(value), unicode(datatype)))
        except UnicodeDecodeError:
            return tuple.__new__(cls, (value, unicode(datatype)))

    def __pyvalue__(self):
        return _pyvalue(self[0], self[1])

    def __int__(self):
        return int(self[0])

    def __float__(self):
        return float(self[0])

    def __long__(self):
        return long(self[0])

    def __unicode__(self):
        return self[0]

    def __str__(self):
        return self[0]

    def __repr__(self):
        return '[Literal value="%s", datatype="%s"]' % self

    value = property(itemgetter(0))
    datatype = property(itemgetter(1))


def _str_to_date(val):
    """\
    Returns a datetime.date instance from the specified string.
    """
    d = strptime(val, '%Y-%m-%d')
    return date(d.tm_year, d.tm_mon, d.tm_mday)

_MSEC = re.compile(r'\.(\d+)')

def _str_to_time(val):
    """\
    Returns a datetime.time instance from the specified string
    """
    msec = 0
    match = _MSEC.search(val)
    if match:
        msec = int(match.group(1))
        val = _MSEC.sub('', val)
    try:
        t = strptime(val, '%H:%M:%S')
    except ValueError:
        try:
            t = strptime(val, '%H:%M:%SZ')
        except ValueError:
            t = strptime(val, '%H:%M:%S%Z')
    return time(t.tm_hour, t.tm_min, t.tm_sec, msec)

def _str_to_dateTime(val):
    """\
    Returns a datetime.datetime instance from a string.
    """
    d, t = val.split('T')
    return datetime.combine(_str_to_date(d), _str_to_time(t))


# XSD -> Python mapping
_XSD2Py = {
          XSD.time:               _str_to_time,
          XSD.date:               _str_to_date,
          XSD.dateTime:           _str_to_dateTime,
          XSD.string:             None,
          XSD.normalizedString:   None,
          XSD.token:              None,
          XSD.language:           None,
          XSD.boolean:            lambda v: v.lower() in ('1', 'true'),
          XSD.decimal:            Decimal,
          XSD.integer:            int,
          XSD.nonPositiveInteger: int,
          XSD.long:               long,
          XSD.nonNegativeInteger: int,
          XSD.negativeInteger:    int,
          XSD.int:                long,
          XSD.unsignedLong:       long,
          XSD.positiveInteger:    int,
          XSD.short:              int,
          XSD.unsignedInt:        long,
          XSD.byte:               int,
          XSD.unsignedShort:      int,
          XSD.unsignedByte:       int,
          XSD.float:              float,
          XSD.double:             float,
          XSD.base64Binary:       base64.decodestring,
          XSD.anyURI:             unicode
          }

def _value_datatype(value):
    """\
    Creates a value/datatype tuple from a Python object.
    
    >>> _value_datatype(4)
    (u'4', u'http://www.w3.org/2001/XMLSchema#integer')
    >>> _value_datatype('Semagia')
    (u'Semagia', u'http://www.w3.org/2001/XMLSchema#string')
    >>> _value_datatype(u'Semagia')
    (u'Semagia', u'http://www.w3.org/2001/XMLSchema#string')
    >>> _value_datatype(42.0)
    (u'42.0', u'http://www.w3.org/2001/XMLSchema#float')
    >>> _value_datatype(42l)
    (u'42', u'http://www.w3.org/2001/XMLSchema#long')
    >>> _value_datatype(True)
    (u'true', u'http://www.w3.org/2001/XMLSchema#boolean')
    >>> _value_datatype(False)
    (u'false', u'http://www.w3.org/2001/XMLSchema#boolean')
    >>> _value_datatype(('Semagia', 'http://www.semagia.com/nonExistingDatatype'))
    (u'Semagia', u'http://www.semagia.com/nonExistingDatatype')
    >>> _value_datatype(object())
    Traceback (most recent call last):
    ...
    TypeError: The datatype cannot be detected
    """
    if isinstance(value, (list, tuple)):
        assert len(value) == 2
        val, dt = value
    elif isinstance(value, basestring):
        val = value
        dt = XSD.string
    elif value is False or value is True:   # isinstance(value, bool) does not work for Jython
        val = ('false', 'true')[value]
        dt = XSD.boolean
    elif isinstance(value, int):
        val = value
        dt = XSD.integer
    elif isinstance(value, float):
        val = value
        dt = XSD.float
    elif isinstance(value, Decimal):
        val = value
        dt = XSD.decimal
    elif isinstance(value, long):
        val = value
        dt = XSD.long
    elif isinstance(value, datetime):  # Must be checked before date!
        val = value.isoformat()
        dt = XSD.dateTime
    elif isinstance(value, date):
        val = value.isoformat()
        dt = XSD.date
    elif isinstance(value, time):
        val = value.isoformat()
        dt = XSD.time
    else:
        raise TypeError('The datatype cannot be detected')
    try:
        return unicode(val), unicode(dt)
    except: # pylint: disable-msg=W0702
        return str(val), unicode(dt)


def _pyvalue(value, datatype):
    """\
    Converts a value/datatype tuple into a Python object.
    
    >>> _pyvalue('true', XSD.boolean)
    True
    >>> _pyvalue('1', XSD.boolean)
    True
    >>> _pyvalue('false', XSD.boolean)
    False
    >>> _pyvalue('0', XSD.boolean)
    False
    >>> _pyvalue('42', XSD.integer)
    42
    >>> _pyvalue('42.0', XSD.float)
    42.0
    >>> _pyvalue('42', XSD.long)
    42L
    >>> _pyvalue('1976-09-19', XSD.date)
    datetime.date(1976, 9, 19)
    >>> _pyvalue('1976-09-19T01:02:03', XSD.dateTime)
    datetime.datetime(1976, 9, 19, 1, 2, 3)
    >>> _pyvalue('1976-09-19T01:02:03.4', XSD.dateTime)
    datetime.datetime(1976, 9, 19, 1, 2, 3, 4)
    >>> _pyvalue('2002-10-10T17:00:00Z', XSD.dateTime)
    datetime.datetime(2002, 10, 10, 17, 0)
    >>> _pyvalue('01:02:03.4', XSD.time)
    datetime.time(1, 2, 3, 4)
    >>> _pyvalue('01:02:03', XSD.time)
    datetime.time(1, 2, 3)
    >>> _pyvalue('Semagia', XSD.string)
    'Semagia'
    >>> _pyvalue(u'Semagia', XSD.string)
    u'Semagia'
    >>> _pyvalue('http://www.semagia.com/', XSD.anyURI)
    u'http://www.semagia.com/'
    """
    try:
        converter = _XSD2Py[datatype]
        if converter is None:
            return value
        return converter(value)
    except KeyError:
        pass
    except ValueError:
        pass
    raise TypeError('Cannot convert value "%s" with datatype "%s" into a Python object' % (str(value), str(datatype)))


if __name__ == '__main__':
    import doctest
    doctest.testmod()
