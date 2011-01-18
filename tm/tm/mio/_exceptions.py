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
MIO exceptions.

.. Warning::

    This module does not belong to the public API, use::
    
        from tm.mio import MIOException

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:version:      $Rev: 393 $ - $Date: 2011-01-10 11:52:54 +0100 (Mo, 10 Jan 2011) $
:license:      BSD license
"""
from xml.sax import SAXException

class MIOException(SAXException, Exception):
    """\
    Common MIO exception which is thrown if an irrevocable error occurs.
    """
    pass

class MIOParseException(MIOException):
    """\
    MIO exception that provides optional line/column information.
    """
    def __init__(self, msg, exception=None, line=-1, column=-1):
        MIOException.__init__(self, msg, exception)
        self._line = line
        self._column = column

    def __str__(self):
        return 'MIOParseException at line "%s", column "%s": %s' % (self._line != -1 and self._line or '?', self._line != -1 and self._column or '?', self.getMessage())

    line = property(lambda self: self._line, doc='Returns the line number where the error occurred or -1 if the line is unknown')
    column = property(lambda self: self._column, doc='Returns the column number where the error occurred or -1 if the column is unknown')
