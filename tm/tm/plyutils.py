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
import tm.ply.yacc as yacc
import tm.ply.lex as lex
# Work-around for parsers which create a big parsetab file
# Import would result in:
#   java.lang.ClassFormatError: Invalid method Code length <number-here>
_yacc_pickle = sys.platform[:4] == 'java'
del sys


def make_lexer(module, debug=False, optimize=True):
    """\
    Returns a lexer. The lexer table is called ``<module.__name__>_lextab`` 
    and placed into the same directory as the ``module``.
    """
    return lex.lex(module=module, debug=debug, optimize=optimize,
                   outputdir=_get_tablocation(module), 
                   lextab='%s_lextab' % module.__name__)


def make_parser(module, debug=False, optimize=True):
    """\
    Returns a parser. The parser table is called ``<module.__name__>_parsetab``
    and placed into the same directory as the ``module``.
    """
    return yacc.yacc(module=module, debug=debug, optimize=optimize,
                     outputdir=_get_tablocation(module),
                     tabmodule='%s_parsetab' % module.__name__)


def make_parser_pickled(module, debug=False, optimize=True):
    """\
    Returns a parser. The parser table is called ``<module.__name__>_parsetab.pickled``
    and placed into the same directory as the ``module``.
    """
    return yacc.yacc(module=module, debug=debug, optimize=optimize,
                     picklefile='%s/%s_parsetab.pickled' % (_get_tablocation(module), module.__name__))


if _yacc_pickle:
    make_parser = make_parser_pickled


def _make_parser_for_sdist(module):
    """\
    Prepare PLY parser modules for source distribution.
    """
    #TODO: Delete previously generated parsetab
    make_parser(module)
    make_parser_pickled(module)


def _get_tablocation(module):
    """\
    Returns the absolute path of the specified module.
    """
    return os.path.dirname(module.__file__)
