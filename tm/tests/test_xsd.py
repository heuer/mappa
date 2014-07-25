# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
Tests against the XSD module.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
from nose.tools import ok_, eq_
from tm import XSD


def test_xsd():
    # Tests if the module XSD has an attribute which is equal
    # to a fragment identifier from XSD Part 2.
    # This test is used to check if typos in the XSD module exist
    def exists_and_equals(frag):
        ok_(hasattr(XSD, frag))
        eq_(getattr(XSD, frag), 'http://www.w3.org/2001/XMLSchema#' + frag)

    exists_and_equals('anyType')
    exists_and_equals('anySimpleType')

    exists_and_equals('duration')
    exists_and_equals('dateTime')
    exists_and_equals('time')
    exists_and_equals('date')
    exists_and_equals('gYearMonth')
    exists_and_equals('gYear')
    exists_and_equals('gMonthDay')
    exists_and_equals('gDay')
    exists_and_equals('gMonth')
    exists_and_equals('boolean')
    exists_and_equals('base64Binary')
    exists_and_equals('hexBinary')
    exists_and_equals('float')
    exists_and_equals('decimal')
    exists_and_equals('double')
    exists_and_equals('anyURI')
    exists_and_equals('QName')
    exists_and_equals('NOTATION')
    # derived from xs:decimal
    exists_and_equals('integer')

    exists_and_equals('nonPositiveInteger')
    exists_and_equals('negativeInteger')

    exists_and_equals('long')
    exists_and_equals('int')
    exists_and_equals('short')
    exists_and_equals('byte')

    exists_and_equals('nonNegativeInteger')
    exists_and_equals('positiveInteger')

    exists_and_equals('unsignedLong')
    exists_and_equals('unsignedInt')
    exists_and_equals('unsignedShort')
    exists_and_equals('unsignedByte')

    # derived from xsd:string
    exists_and_equals('normalizedString')
    exists_and_equals('token')
    exists_and_equals('language')
    exists_and_equals('Name')
    exists_and_equals('NMTOKEN')
    exists_and_equals('NMTOKENS')

    # derived from xsd:Name
    exists_and_equals('NCName')
    exists_and_equals('ID')
    exists_and_equals('IDREF')
    exists_and_equals('IDREFS')
    exists_and_equals('ENTITY')
    exists_and_equals('ENTITIES')


def test_number_of_datatypes():
    # XML Schema Datatypes Part 2 provides currently 46 datatypes
    eq_(46, len([name for name in dir(XSD) if name[:2] != '__']))


if __name__ == '__main__':
    import nose
    nose.core.runmodule()

