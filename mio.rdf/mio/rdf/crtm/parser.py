# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2011 -- Lars Heuer - Semagia <http://www.semagia.com/>.
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
#     * Neither the project name nor the names of the contributors may be 
#       used to endorse or promote products derived from this software 
#       without specific prior written permission.
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
Compact RTM (CRTM) parser.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
from tm import mio
from .lexer import tokens #pylint: disable-msg=E0611, F0401, W0611

class Context(object):
    """\

    """

# Disable unused 'p' warnings: pylint: disable-msg=W0613

def p_noop(p): # Handles all grammar rules where the result is unimportant
    """\
    instance    : prolog body
                | body
    body        : statement
                | scoped_statement
                | body statement
                | body scoped_statement
                | body prefix_directive
                | body
    prolog      : directive
                | prolog directive
    statement_body
                : name
                | occurrence
                | isa
                | ako
                | identity
                | association
    in_scope_statements
                : in_scope_statement
                | in_scope_statements in_scope_statement
    occurrence  : KW_OCC opt_char_body
                | char_body
    """
    p[0] = None


def p_directive(p):
    """\
    directive   : prefix_directive
                | DIR_INCLUDE IRI               { include($2); }
                | DIR_LANG2SCOPE bool           { setConvertLanguageToScope($2); }
    """

def p_directive_include(p):
    """\
    directive   : DIR_INCLUDE_IRI
    """

def p_directive_lang2scope(p):
    """\
    directive   : DIR_LANG2SCOPE bool
    """

def p_directive_prefix(p):
    """\
    directive   : prefix_directive
    """

def p_prefix_directive(p):
    """\
    prefix_directive : DIR_PREFIX IDENT IRI
    """

def p_statement(p):
    """\
    statement   : qiris COLON _remember_predicate statement_body
    """

def p__remember_predicate(p):
    """\
    _remember_predicate : 
    """
    #{ _predicates = $1; _addNextPredicate(); _reset(); }

def p_bool(p):
    """\
    bool        : KW_TRUE
                | KW_FALSE
    """
    p[0] = p[1] == 'true'

def _parser(p):
    """\
    
    """
    return p.parser

def _handler(p):
    return _ctx(p).handler

def _ctx(p):
    return _parser(p).context

def p_error(p):
    #TODO: Better error reporting (line, col, token)
    raise mio.MIOException('Unexpected token "%r"' % p)

