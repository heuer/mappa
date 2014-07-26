# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
Tests the (internal) duplicate removal module.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD License
"""
from . mappa_test import MappaTestCase, len_
from mappa._internal import dupremoval

class TestDuplicateRemoval(MappaTestCase):
    
    def test_removal_name(self):
        name = self.create_name()
        theme = self.create_topic()
        v1 = name.create_variant(value='Semagia', scope=[theme])
        v2 = name.create_variant(value='Semagia', scope=[theme])
        if len_(name.variants) == 1:
            return # Assuming that the backend has detected the duplicates
        self.assertEqual(2, len_(name.variants))
        dupremoval._remove_duplicates_from_name(name)
        self.assertEqual(1, len_(name.variants))


if __name__ == '__main__':
    import nose
    nose.core.runmodule()
