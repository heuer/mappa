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
This module provides an utility class which can be used to abbreviate IRIs.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:version:      $Rev: 167 $ - $Date: 2009-06-26 14:13:53 +0200 (Fr, 26 Jun 2009) $
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
