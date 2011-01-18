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
Tests the Java -> Python MIO compatibility.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:version:      $Rev: 167 $ - $Date: 2009-06-26 14:13:53 +0200 (Fr, 26 Jun 2009) $
:license:      BSD license
"""
from unittest import TestCase
from tm import mio
from tm.mio import handler
from com.semagia.mio import IRef
from com.semagia.mio.helpers import Ref

class TestFromJava(TestCase):

    def _create_identity(self, ref):
        """\
        Returns a (kind, iri) tuple from the IRef
        """
        return handler._create_identity(ref)

    def test_create_sid(self):
        iri = 'http://www.semagia.com/'
        kind, iri_ = self._create_identity(Ref.createSubjectIdentifier(iri))
        self.assertEqual(iri, iri_)
        self.assertEqual(mio.SUBJECT_IDENTIFIER, kind)

    def test_create_slo(self):
        iri = 'http://www.semagia.com/'
        kind, iri_ = self._create_identity(Ref.createSubjectLocator(iri))
        self.assertEqual(iri, iri_)
        self.assertEqual(mio.SUBJECT_LOCATOR, kind)

    def test_create_iid(self):
        iri = 'http://www.semagia.com/'
        kind, iri_ = self._create_identity(Ref.createItemIdentifier(iri))
        self.assertEqual(iri, iri_)
        self.assertEqual(mio.ITEM_IDENTIFIER, kind)

if __name__ == '__main__':
    from test import test_support
    test_support.run_unittest(TestFromJava)
