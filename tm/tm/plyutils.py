# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
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


def _make_parser_for_sdist(module):
    """\
    Prepare PLY parser modules for source distribution.
    """
    import re
    make_parser(module)
    filename = os.path.join(_get_tablocation(module), 'parser_parsetab.py')
    with open(filename, 'rb') as f:
        s = f.read()
    s = re.sub(ur"(\d\s*,)('[^']+',\s*').*?(parser.py')", ur"\1\2\3", s)
    with open(filename, 'wb') as f:
        f.write(s)


def _get_tablocation(module):
    """\
    Returns the absolute path of the specified module.
    """
    return os.path.dirname(module.__file__)
