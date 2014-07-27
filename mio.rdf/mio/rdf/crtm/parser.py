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


class ParserContext(object):
    """\

    """
    def __init__(self, base):
        self._base = base
        self._included_by = []
        self.global_lang2scope = False
        self._prefixes = {}
        self.reset()

    def reset(self):
        """\

        """
        self._subject_role = None
        self._object_role = None
        self.lang2scope = False
        self._next_predicate = None
        self.is_name = False
        self.name = None
        self._predicates = []
        self._scope = []
        self._type = None

    def process_association(self, handler):
        subject_role = self._subject_role
        object_role = self._object_role
        scope = self._scope
        type = self._type
        for predicate in self._predicates:
            handler.handleAssociation(predicate, subject_role, object_role,
                                      scope, type)

    def process_characteristic(self, handler):
        scope = self._scope
        type = self._type
        lang2scope = self.lang2scope or self.global_lang2scope
        if self.is_name:
            for predicate in self._predicates:
                handler.handleName(predicate, scope, type, lang2scope)
        else:
            for predicate in self._predicates:
                handler.handleOccurrence(predicate, scope, type, lang2scope)

    def process_sids(self, handler):
        pass

    def process_slos(self, handler):
        pass

    def process_iids(self, handler):
        pass

    def add_predicate(self):
        pass

    def process_type_instance(self, handler):
        pass

    def process_supertype_subtype(self, handler):
        pass

    def register_prefix(self, ident, iri, listener):
        existing = self._prefixes.get(ident)
        if existing and existing != iri:
            raise mio.MIOException(u'The prefix "%s" is already bound to <%s>"' % (ident, self._prefixes[ident]))
        self._prefixes[ident] = iri
        if listener:
            listener.handleNamespace(ident, iri)

    def register_anonymous_prefix(self, iri, listener):
        ident = iri
        if ident.endswith(u'/') or ident.endswith(u'#'):
            ident = ident[:-1]
        slash_idx = ident.rfind(u'/')
        if slash_idx > -1:
            ident = ident[slash_idx+1:]
        existing_iri = self._prefixes.get(ident)
        if existing_iri and existing_iri != iri:
            cnt = 0
            while existing_iri:
                cnt += 1
                ident += unicode(cnt)
                existing_iri = self._prefixes.get(ident)
        self.register_prefix(ident, iri, listener)
        
    def resolve_qname(self, local):
        pass

    def resolve_iri(self, iri):
        pass

    def _set_included_by(self, included_by):
        pass

    included_by = property(lambda self: self._included_by, lambda self, included_by: self._set_included_by(included_by))


def p_noop(p):  # Handles all grammar rules where the result is unimportant
    """\
    instance    : prolog body
                | body
                | prolog
    body        : statement
                | scoped_statement
                | body statement
                | body scoped_statement
                | body prefix_directive
    prolog      : directive
                | prolog directive
    directive   : prefix_directive
    statement   : qiris COLON _remember_predicates statement_body
    statement_body : name
                | occurrence
                | isa
                | ako
                | identity
                | association
    in_scope_statements : in_scope_statement
                | in_scope_statements in_scope_statement
    in_scope_statement : locals COLON _remember_predicates statement_body
    occurrence  : KW_OCC opt_char_body
                | char_body
    name        : KW_NAME _is_name opt_char_body
                | HYPHEN  _is_name opt_char_body
    opt_type    :
                | type
    opt_scope   :
                | scope
    opt_char_body :
                | char_body
    char_body   : type scope opt_lang _process_characteristic
                | type opt_lang _process_characteristic
                | scope opt_lang _process_characteristic
                | qiri COLON _char_body_qiri statement_body
                | IRI LCURLY _char_body_iri in_scope_statements RCURLY

    """
    p[0] = None


def p__char_body_qiri(p):  # Inline action
    """\
    _char_body_qiri :
    """
    ctx = _ctx(p)
    ctx.process_characteristic()
    ctx.reset()
    ctx.predicates = [p[-2]]


def p__char_body_iri(p):  # Inline action
    """\
    _char_body_iri :
    """
    ctx = _ctx(p)
    ctx.process_characteristic()
    ctx.reset()
    ctx.register_anonymous_prefix(p[-2], _prefix_listener(p))


def p__process_characteristic(p):
    """\
    _process_characteristic :
    """
    _ctx(p).process_characteristic(_handler(p))


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
    _ctx(p).register_prefix(p[2], p[3], _prefix_listener(p))


def p__remember_predicates(p):
    """\
    _remember_predicates :
    """
    ctx = _ctx(p)
    predicates = p[-2]
    next_pred = _parser(p)
    if next_pred:
        predicates.append(next_pred)
    ctx.predicates = predicates
    ctx.reset()


def p_local(p):
    """\
    local       : LOCAL_IDENT
                | IDENT
    """
    ctx = _ctx(p)
    p[0] = ctx.resolve_qname(p[1])


def p_locals(p):
    """\
    locals      : local
                | locals COMMA local
    """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1]
        p[0].append(p[3])


def p_identity_sid(p):
    """\
    identity    : KW_SID
    """
    _ctx(p).process_sids(_handler(p))


def p_identity_slo(p):
    """\
    identity    : KW_SLO
    """
    _ctx(p).process_slos(_handler(p))


def p_identity_iid(p):
    """\
    identity    : KW_IID
    """
    _ctx(p).process_iids(_handler(p))


def p_isa(p):
    """\
    isa         : KW_ISA opt_scope
    """
    _ctx(p).process_type_instance(_handler(p))


def p_ako(p):
    """\
    ako         : KW_AKO opt_scope
    """
    _ctx(p).process_supertype_subtype(_handler(p))


def p_char_body_qiri(p):
    """\
    char_body   : qiri COMMA
    """
    ctx = _ctx(p)
    ctx.process_characteristic(_handler(p))
    ctx.reset()
    ctx.next_predicate = p[1]


def p_opt_lang(p):
    """\
    opt_lang    :
                | SEMI KW_LANG EQ bool
    """
    _ctx(p).lang2scope = p[5] if len(p) > 1 else False


def p_bool(p):
    """\
    bool        : KW_TRUE
                | KW_FALSE
    """
    p[0] = p[1] == u'true'


def p_association(p):
    """\
    association : KW_ASSOC opt_type roles opt_scope
                | opt_type roles opt_scope
    """
    _ctx(p).process_association(_handler(p))


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


def p_scoped_statement(p):
    """\
    scoped_statement : IDENT LCURLY in_scope_statements RCURLY
                     | IRI LCURLY _anon_prefix in_scope_statements RCURLY
    """


def p__anon_prefix(p):  # Inline action
    """\
    _anon_prefix :
    """
    _ctx(p).register_anonymous_prefix(p[-2], _prefix_listener(p))


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
    return _parser(p).handler


def _ctx(p):
    return _parser(p).context


def _prefix_listener(p):
    return _parser(p).prefix_listener


def p_error(p):
    #TODO: Better error reporting (line, col, token)
    raise mio.MIOException('Unexpected token "%r"' % p)