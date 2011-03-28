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
Tests against the XSD module.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:version:      $Rev: 167 $ - $Date: 2009-06-26 14:13:53 +0200 (Fr, 26 Jun 2009) $
:license:      BSD license
"""
from unittest import TestCase
from tm import XSD

class TestXSD(TestCase):
    
    def test_xsd(self):
        # Tests if the module XSD has an attribute which is equal
        # to a fragment identifier from XSD Part 2.
        # This test is used to check if typos in the XSD module exist
        def exists_and_equals(frag):
            self.assert_(hasattr(XSD, frag))
            self.assertEqual(getattr(XSD, frag), 'http://www.w3.org/2001/XMLSchema#' + frag)

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
        
    def test_number_of_datatypes(self):
        # XML Schema Datatypes Part 2 provides currently 46 datatypes
        self.assertEqual(46, len([name for name in dir(XSD) if name[:2] != '__']))


if __name__ == '__main__':
    from test import test_support
    test_support.run_unittest(TestXSD)

