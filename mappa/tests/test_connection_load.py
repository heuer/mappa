# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
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
