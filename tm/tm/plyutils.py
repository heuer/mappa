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
Utilities for lexers / parsers using `Ply <http://www.dabeaz.com/ply/>`_

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
from __future__ import absolute_import
import os
import sys
import ply.yacc as yacc
import ply.lex as lex
# Work-around for parsers which create a big parsetab file
# Import would result in:
#   java.lang.ClassFormatError: Invalid method Code length <number-here>
_yacc_pickle = sys.platform[:4] == 'java'
del sys
# For some reason pylint thinks that ply.lex and ply.yacc do not exist
# pylint: disable-msg=F0401, E0611

def make_lexer(module, debug=False, optimize=True):
    """\
    Returns a lexer. The lexer table is called ``<module.__name__>_lextab`` 
    and placed into the same directory as the ``module``.
    """
    return lex.lex(module=module, debug=debug, optimize=optimize,
                   outputdir=_get_tablocation(module), 
                   lextab='%s_lextab' % module.__name__)

if _yacc_pickle:
    def make_parser(module, debug=False, optimize=True):
        """\
        Returns a parser. The parser table is called ``<module.__name__>_parsetab`` 
        and placed into the same directory as the ``module``.
        """
        return yacc.yacc(module=module, debug=debug, optimize=optimize,
                         picklefile='%s/%s_parsetab.p' % (_get_tablocation(module), module.__name__))
else:
    def make_parser(module, debug=False, optimize=True):
        """\
        Returns a parser. The parser table is called ``<module.__name__>_parsetab`` 
        and placed into the same directory as the ``module``.
        """
        return yacc.yacc(module=module, debug=debug, optimize=optimize,
                         outputdir=_get_tablocation(module),
                         tabmodule='%s_parsetab' % module.__name__)

def _get_tablocation(module):
    """\
    Returns the absolute path of the specified module.
    """
    return os.path.dirname(module.__file__)
