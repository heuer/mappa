# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
Tests against mio.rdf.mapping.MappingHandler.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
from nose.tools import ok_
from tm import mio
from mio.rdf.mapping import MappingHandler


def fail(msg): raise AssertionError(msg)


def test_mapping_handler():
    mh = MappingHandler()
    ok_(not mh.mapping)
    mh.start()
    name_pred = 'http://www.example.org/name'
    mh.handleName(name_pred)
    ok_(name_pred in mh.mapping)
    occ_pred = 'http://www.example.org/occ'
    mh.handleOccurrence(occ_pred)
    ok_(occ_pred in mh.mapping)
    assoc_pred = 'http://www.example.org/assoc'
    mh.handleAssociation(assoc_pred, 'http://www.example.org/subject', 'http://www.example.org/object', None, None)
    ok_(assoc_pred in mh.mapping)
    isa_pred = 'http://www.example.org/isa'
    mh.handleInstanceOf(isa_pred)
    ok_(isa_pred in mh.mapping)
    isa_pred_scoped = 'http://www.example.org/isa-scoped'
    mh.handleInstanceOf(isa_pred_scoped, ['http://www.example.org/theme'])
    ok_(isa_pred_scoped in mh.mapping)
    ako_pred = 'http://www.example.org/ako'
    mh.handleSubtypeOf(ako_pred)
    ok_(ako_pred in mh.mapping)
    iid_pred = 'http://www.example.org/iid'
    mh.handleItemIdentifier(iid_pred)
    ok_(iid_pred in mh.mapping)
    sid_pred = 'http://www.example.org/sid'
    mh.handleSubjectIdentifier(sid_pred)
    ok_(sid_pred in mh.mapping)
    slo_pred = 'http://www.example.org/slo'
    mh.handleSubjectLocator(slo_pred)
    ok_(slo_pred in mh.mapping)
    mh.end()


def test_illegal_association_subject():
    mh = MappingHandler()
    mh.start()
    try:
        mh.handleAssociation('http://www.example.org/pred', None, 'http://www.example.org/object')
        fail('Excpected an exception for subject_role == None')
    except mio.MIOException:
        pass


def test_illegal_association_object():
    mh = MappingHandler()
    mh.start()
    try:
        mh.handleAssociation('http://www.example.org/pred', 'http://www.example.org/subject', None)
        fail('Excpected an exception for object_role == None')
    except mio.MIOException:
        pass

    
if __name__ == '__main__':
    import nose
    nose.core.runmodule()
