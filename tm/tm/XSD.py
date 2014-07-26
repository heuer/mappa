# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
XML Schema Datatypes Part 2 standard PSIs.

This module provides the standard PSIs for XSD. If you need one 
of the standard PSIs, you should use this module, rather than the `XSD`
namespace provided by the `tm.voc` module to avoid typos. By convention,
the hyphen (``-``) in the PSIs is replaced by an underscore character (``_``)

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
from tm.voc import XSD

__all__ = () # Avoid to expose something that pollutes the namespace

anyType = XSD.anyType
anySimpleType = XSD.anySimpleType

duration = XSD.duration
dateTime = XSD.dateTime
time = XSD.time
date = XSD.date
gYearMonth = XSD.gYearMonth
gYear = XSD.gYear
gMonthDay = XSD.gMonthDay
gDay = XSD.gDay
gMonth = XSD.gMonth
boolean = XSD.boolean
base64Binary = XSD.base64Binary
hexBinary = XSD.hexBinary
float = XSD.float
decimal = XSD.decimal
double = XSD.double
anyURI = XSD.anyURI
QName = XSD.QName
NOTATION = XSD.NOTATION
string = XSD.string
# Things derived from xs:decimal
integer = XSD.integer
nonPositiveInteger = XSD.nonPositiveInteger
long = XSD.long
nonNegativeInteger = XSD.nonNegativeInteger
negativeInteger = XSD.negativeInteger
int = XSD.int
unsignedLong = XSD.unsignedLong
positiveInteger = XSD.positiveInteger
short = XSD.short
unsignedInt = XSD.unsignedInt
byte = XSD.byte
unsignedShort = XSD.unsignedShort
unsignedByte = XSD.unsignedByte
# Things derived from xs:string
normalizedString = XSD.normalizedString
token = XSD.token
language = XSD.language
Name = XSD.Name
NMTOKEN = XSD.NMTOKEN
NCName = XSD.NCName
NMTOKENS = XSD.NMTOKENS
ID = XSD.ID
IDREF = XSD.IDREF
ENTITY = XSD.ENTITY
IDREFS = XSD.IDREFS
ENTITIES = XSD.ENTITIES

del XSD
