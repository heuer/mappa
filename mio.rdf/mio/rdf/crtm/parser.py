# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
Compact RTM (CRTM) parser.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
from tm import mio
from .lexer import tokens
assert tokens


class Context(object):
    """\

    """
    __slots__ = ('global_lang2scope', 'lang2scope', 'next_predicate', 'is_name', '_base', '_included_by')

    def __init__(self, base):
        self._base = base
        self._included_by = []
        self.global_lang2scope = False
        self.reset()

    def reset(self):
        """\

        """
        self.lang2scope = False
        self.next_predicate = None
        self.is_name = False

    def process_association(self):
        pass

    def process_sids(self):
        pass

    def process_slos(self):
        pass

    def process_iids(self):
        pass

    def add_predicate(self):
        pass

    def process_type_instance(self):
        pass

    def process_supertype_subtype(self):
        pass

    def register_anonymous_prefix(self, iri):
        self.name = ident
        
    def resolve_qname(self, local):
        pass

    def resolve_iri(self, iri):
        pass

    def _set_included_by(self, included_by):
        pass

    included_by = property(lambda self: self._included_by, lambda self, included_by: self._set_included_by(included_by))


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
    statement   : qiris COLON _remember_predicate statement_body
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
    in_scope_statement
                : locals COLON _remember_predicate statement_body
    occurrence  : KW_OCC opt_char_body
                | char_body
    name        : KW_NAME _is_name opt_char_body
                | HYPHEN  _is_name opt_char_body
    directive   : prefix_directive
    opt_type    :
                | type
    opt_scope   :
                | scope
    char_body   : qiri COLON _process_characteristic statement_body
                | IRI LCURLY _anonymous_prefix in_scope_statements RCURLY
                | type scope opt_lang _process_characteristic
                | type opt_lang _process_characteristic
                | scope opt_lang _process_characteristic
    
    """
    p[0] = None


def p__process_characteristic(p):
    """\
    _process_characteristic
                : 
    """
    _ctx(p).process_characteristic()


def p__anonymous_prefix(p):
    """\
    _anonymous_prefix
                : 
    """
    ctx = _ctx(p)
    ctx.process_characteristic()
    ctx.reset()
    ctx.register_anonymous_prefix(p[-2])


def p__is_name(p):
    """\
    _is_name    :
    """
    _ctx(p).is_name = True


def p_include_directive(p):
    """\
    directive   : DIR_INCLUDE IRI
    """
    _ctx(p).include(p[2])


def p_lang2scope_directive(p):
    """\
    directive   : DIR_LANG2SCOPE bool
    """
    _ctx(p).global_lang2scope = p[2]


def p_prefix_directive(p):
    """\
    prefix_directive : DIR_PREFIX IDENT IRI
    """
    _ctx(p).register_prefix(p[2], p[3])


def p__remember_predicate(p):
    """\
    _remember_predicate : 
    """
    ctx = _ctx(p)
    ctx.predicates = p[-2]
    ctx.add_predicate()
    ctx.reset()


def p_local(p):
    """\
    local       : LOCAL_IDENT
                | IDENT
    """
    ctx = _ctx(p)
    p[0] = ctx.resolve_qname(p[1])


def p_identity_sid(p):
    """\
    identity    : KW_SID
    """
    _ctx(p).process_sids()


def p_identity_slo(p):
    """\
    identity    : KW_SLO
    """
    _ctx(p).process_slos()


def p_identity_iid(p):
    """\
    identity    : KW_IID
    """
    _ctx(p).process_iids()


def p_isa(p):
    """\
    isa         : KW_ISA opt_scope
    """
    _ctx(p).process_type_instance()


def p_ako(p):
    """\
    ako         : KW_AKO opt_scope
    """
    _ctx(p).process_supertype_subtype()


def p_char_body_qiri(p):
    """\
    char_body   : qiri COMMA
    """
    ctx = _ctx(p)
    ctx.process_characteristic()
    ctx.reset()
    ctx.next_predicate = p[1]


def p_opt_lang(p):
    """\
    opt_lang    :
                | SEMI KW_LANG EQ bool
    """
    if len(p) > 1:
        _ctx(p).lang2scope = p[5]
    else:
        _ctx(p).lang2scope = False


def p_bool(p):
    """\
    bool        : KW_TRUE
                | KW_FALSE
    """
    p[0] = p[1] == 'true'


def p_association(p):
    """\
    association : KW_ASSOC opt_type roles opt_scope
                | opt_type roles opt_scope
    """
    _ctx(p).process_association()


def p_roles(p):
    """\
    roles       : LPAREN qiri COMMA qiri RPAREN
    """
    p[0] = p[2], p[4]


def p_type(p):
    """\
    type        : qiri
    """
    _ctx(p).type = p[1]


def p_scope(p):
    """\
    scope       : AT qiris
    """
    _ctx(p).scope = p[2]


def p_qiri_qname(p):
    """\
    qiri        : QNAME
    """
    _ctx(p).resolve_qname(p[1])    


def p_qiri_iri(p):
    """\
    qiri        : IRI
    """
    _ctx(p).resolve_iri(p[1])


def p_qiris(p):
    """\
    qiris       : qiri
                | qiris COMMA qiri
    """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1]
        p[0].append(p[3])


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
