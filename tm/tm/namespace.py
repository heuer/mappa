# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
This module provides an utility class which can be used to abbreviate IRIs.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""


class Namespace(unicode):
    """\
    The namespace class.
    
    >>> TMDM = Namespace('http://psi.topicmaps.org/iso13250/model/')
    >>> TMDM
    u'http://psi.topicmaps.org/iso13250/model/'
    >>> TMDM[u'type-instance']
    u'http://psi.topicmaps.org/iso13250/model/type-instance'
    >>> XSD = Namespace('http://www.w3.org/2001/XMLSchema#')
    >>> XSD.string
    u'http://www.w3.org/2001/XMLSchema#string'
    >>> XSD['string']
    u'http://www.w3.org/2001/XMLSchema#string'
    """
    __slots__ = ()

    def __new__(cls, value):
        if value is None:
            raise ValueError()
        if isinstance(value, Namespace):
            return value
        return unicode.__new__(cls, value)
    
    def __getattr__(self, name):
        return self.__getitem__(name)
    
    def __getitem__(self, key):
        return u'%s%s' % (self, key)


if __name__ == '__main__':
    import doctest
    doctest.testmod()
