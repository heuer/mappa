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
#     * Neither the name 'Semagia' nor the name 'Mappa' nor the names of the
#       contributors may be used to endorse or promote products derived from 
#       this software without specific prior written permission.
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
Tests against the topic map connection.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD License
"""
from mappa import TMDM
from . mappa_test import MappaTestCase, len_

class TestConnectionLoad(MappaTestCase):

    def test_load_xtm_postprocess(self):
        self._conn.loads('''\
<topicMap
   xmlns="http://www.topicmaps.org/xtm/1.0/"
   xmlns:xlink="http://www.w3.org/1999/xlink">
  <association>
    <instanceOf>
      <subjectIndicatorRef xlink:href='http://www.topicmaps.org/xtm/1.0/core.xtm#class-instance'/>
    </instanceOf>
    <member>
      <roleSpec>
      <subjectIndicatorRef xlink:href='http://www.topicmaps.org/xtm/1.0/core.xtm#class'/>
      </roleSpec>
      <topicRef xlink:href='#country'/>
    </member>
    <member>
      <roleSpec>
      <subjectIndicatorRef xlink:href='http://www.topicmaps.org/xtm/1.0/core.xtm#instance'/>
      </roleSpec>
      <topicRef xlink:href='#norway'/>
    </member>
  </association>
</topicMap>
''', into=self.base, format='xtm')
        self.assert_(1, len_(self._tm.associations))
        topic = self._tm.topic_by_sid(TMDM.type_instance)
        self.assert_(topic)
        self.assert_(1, len_(topic.sids))
        topic = self._tm.topic_by_sid(TMDM.type)
        self.assert_(topic)
        self.assert_(1, len_(topic.sids))
        topic = self._tm.topic_by_sid(TMDM.instance)
        self.assert_(topic)
        self.assert_(1, len_(topic.sids))


if __name__ == '__main__':
    import nose
    nose.core.runmodule()
