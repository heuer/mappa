# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
Compact Topic Maps (CTM) parser.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
from tm import mio
from . import utils, consts
from .lexer import tokens
assert tokens


def unescape_string(s):
    try:
        return utils.unescape_string(s)
    except ValueError, ex:
        raise mio.MIOException(ex)


def p_noop(p):  # Handles all grammar rules where the result is unimportant
    """\
    instance        : prolog header topicmap
                    | prolog header
                    | prolog topicmap
                    | prolog
    prolog          : 
                    | encoding_directive version_directive
                    | version_directive
                    | encoding_directive
    header          : directive
                    | directive topicmap_reifier
                    | topicmap_reifier
                    | header directive
                    | header directive topicmap_reifier
    topicmap        : topic
                    | topicmap topic
                    | association
                    | topicmap association
                    | topicmap directive
                    | tpl_def
                    | topicmap tpl_def
                    | tpl_call
                    | topicmap tpl_call
    directive       : prefix_directive
                    | mergemap_directive
                    | include_directive
    encoding_directive : DIR_ENCODING STRING
    topic           : block_start assignments eot
                    | block_start eot
    assignments     : assignment
                    | assignments SEMI assignment
    assignment      : name
                    | occurrence
                    | tpl_call
                    | identity
                    | isa
                    | ako
    opt_variants    :
                    | variants
    variants        : variant
                    | variants variant
    opt_more_roles  :
                    | COMMA roles
    roles           : role
                    | roles COMMA role
    opt_scope       : 
                    | scope
    themes          : theme
                    | themes COMMA theme
    tpl_body        : topic
                    | association
                    | tpl_call
                    | tpl_body topic
                    | tpl_body association
                    | tpl_body tpl_call
    opt_semi        : 
                    | SEMI
    """
    p[0] = None


def p_topicmap_reifier(p):
    """\
    topicmap_reifier : TILDE topic_ref
    """
    ctx = _ctx(p)
    if not p.parser.content_handler.environment.subordinate:
        ctx.reifier(p[2])
    else:
        ctx.startTopic(p[2])
        ctx.endTopic()


def p_version_directive(p):
    """\
    version_directive : DIR_VERSION DECIMAL 
    """
    if p[2] != u'1.0':
        raise mio.MIOException('Invalid version, expected "1.0", got: "%s"' % p[2])


def p_prefix_directive(p):
    """\
    prefix_directive : DIR_PREFIX IDENT IRI
    """
    _env(p).add_prefix(p[2], p[3])


def p_mergemap_directive(p):
    """\
    mergemap_directive : DIR_MERGEMAP qiri qiri
    """
    _env(p).merge(p[2][1], p[3][1])


def p_include_directive(p):
    """\
    include_directive : DIR_INCLUDE qiri
    """
    _env(p).include(p[2][1])


def p_ident(p):
    """\
    ident           : IDENT
    """
    p[0] = consts.IID, _ctx(p).resolve_ident(p[1])


def p_topic_ref_no_ident(p):
    """\
    topic_ref_no_ident : embedded_topic
                       | iid
                       | qiri
                       | slo
                       | variable
    """
    p[0] = p[1]


def p_topic_ref_no_ident_wildcards(p):
    """\
    topic_ref_no_ident : WILDCARD
                       | NAMED_WILDCARD
    """
    ctx = _ctx(p)
    p[0] = ctx.start_topic_wildcard(p[1] != u'?' and p[1] or None)
    ctx.endTopic()


def p_topic_ref(p):
    """\
    topic_ref       : topic_ref_no_ident
                    | ident
    """
    p[0] = p[1]


def p_block_start(p):
    """\
    block_start     : qiri
                    | slo
                    | iid
                    | ident
                    | variable
    """
    _ctx(p).startTopic(p[1])


def p_block_start_wildcards(p):
    """\
    block_start     : WILDCARD
                    | NAMED_WILDCARD
    """
    _ctx(p).start_topic_wildcard(p[1] != u'?' and p[1] or None)


def p_qiri_qname(p):
    """\
    qiri            : QNAME
    """
    p[0] = consts.IRI, _env(p).resolve_qname(p[1])


def p_qiri_iri(p):
    """\
    qiri            : IRI
    """
    p[0] = consts.IRI, _env(p).resolve_iri(p[1])


def p_slo(p):
    """\
    slo             : EQ qiri
    """
    p[0] = consts.SLO, p[2][1]


def p_slo_variable(p):
    """\
    slo             : EQ VARIABLE
    """
    p[0] = consts.VSLO, p[2]


def p_iid(p):
    """\
    iid             : CIRCUMFLEX qiri
    """
    p[0] = consts.IID, p[2][1]


def p_iid_variable(p):
    """\
    iid             : CIRCUMFLEX VARIABLE
    """
    p[0] = consts.VIID, p[2]


def p_variable(p):
    """\
    variable        : VARIABLE
    """
    p[0] = consts.VARIABLE, p[1]


def p_eot(p):
    """\
    eot             : opt_semi DOT
    """
    _ctx(p).endTopic()


def p_embedded_topic(p):
    """\
    embedded_topic  : embedded_start assignments opt_semi RBRACK
    """
    p[0] = p[1]
    _ctx(p).endTopic()


def p_embedded_start(p):
    """\
    embedded_start  : LBRACK
    """
    p[0] = _ctx(p).start_topic_wildcard()


def p_isa(p):
    """\
    isa             : KW_ISA topic_ref
    """
    _ctx(p).isa(p[2])


def p_ako(p):
    """\
    ako             : KW_AKO topic_ref
    """
    _ctx(p).ako(p[2])


def p_occurrence(p):
    """\
    occurrence      : topic_ref _start_occ COLON literal opt_scope opt_reifier
    """
    ctx = _ctx(p)
    ctx.value(p[4])
    ctx.endOccurrence()


def p__start_occ(p): # Inline action
    """
    _start_occ : 
    """
    _ctx(p).startOccurrence(p[-1])


def p_name_typed(p): # - ($type|type) COLON ...
    """\
    name            : name_start _start_name COLON name_value opt_scope opt_reifier opt_variants
    """
    ctx = _ctx(p)
    ctx.name_value(p[4])
    ctx.endName()


def p_name_untyped1(p): # - $value ...
    """\
    name            : name_start _start_untyped_name opt_scope opt_reifier opt_variants
    """
    ctx = _ctx(p)
    ctx.name_value(p[1])
    ctx.endName()


def p_name_untyped2(p): # - "value" ...
    """\
    name            : HYPHEN _start_name string opt_scope opt_reifier opt_variants
    """
    ctx = _ctx(p)
    ctx.name_value(p[3])
    ctx.endName()


def p__start_untyped_name(p): # Inline action
    """\
    _start_untyped_name :
    """
    _ctx(p).startName()


def p__start_name(p): # Inline action
    """\
    _start_name     : 
    """
    if p[-1] == '-':
        _ctx(p).startName()
    else:
        _ctx(p).startName(p[-1])


def p_name_start(p):
    """\
    name_start      : HYPHEN topic_ref
    """
    p[0] = p[2]


def p_name_value(p):
    """\
    name_value      : string
                    | variable
    """
    p[0] = p[1]


def p_variant(p):
    """\
    variant         : LPAREN _start_variant literal scope opt_reifier RPAREN
    """
    ctx = _ctx(p)
    ctx.value(p[3])
    ctx.endVariant()


def p__start_variant(p):  # Inline action
    """\
    _start_variant  : 
    """
    _ctx(p).startVariant()


def p_association(p):
    """\
    association     : topic_ref_no_ident LPAREN _start_assoc1 roles RPAREN opt_scope opt_reifier
                    | tpl_call_or_assoc_start COLON topic_ref opt_role_reifier _start_assoc2 opt_more_roles RPAREN opt_scope opt_reifier
    """
    _ctx(p).endAssociation()


def p__start_assoc1(p):  # Inline action
    """\
    _start_assoc1   : 
    """
    _ctx(p).startAssociation(p[-2])


def p__start_assoc2(p): # Inline action
    """\
    _start_assoc2   : 
    """
    assoc_type, role_type = p[-4]
    player, reifier = p[-2], p[-1]
    ctx = _ctx(p)
    assoc_type = consts.IID, _ctx(p).resolve_ident(assoc_type)
    ctx.startAssociation(assoc_type)
    ctx.handle_role(role_type, player, reifier)


def p_tpl_call_or_assoc_start(p):
    """\
    tpl_call_or_assoc_start : IDENT LPAREN topic_ref
    """
    p[0] = p[1], p[3]


def p_role(p):
    """\
    role            : topic_ref COLON topic_ref opt_role_reifier
    """
    _ctx(p).handle_role(p[1], p[3], p[4])


def p_opt_role_reifier(p):
    """\
    opt_role_reifier :
                     | TILDE topic_ref
    """
    p[0] = p[2] if len(p) == 3 else None


def p_scope(p):
    """\
    scope           : AT _start_scope themes
    """
    _ctx(p).endScope()


def p__start_scope(p):  # Inline action
    """\
    _start_scope :
    """
    _ctx(p).startScope()


def p_theme(p):
    """\
    theme           : topic_ref
    """
    _ctx(p).theme(p[1])


def p_reifier(p):
    """\
    opt_reifier     : 
                    | reifier
    reifier         : TILDE topic_ref
    """
    if len(p) == 3:
        _ctx(p).reifier(p[2])


def p_identity_qiri(p):
    """\
    identity        : qiri
    """
    _ctx(p).subjectIdentifier(p[1][1])


def p_identity_variable(p):
    """\
    identity        : variable
    """
    _ctx(p).identity(p[1])


def p_identity_slo(p):
    """\
    identity        : slo
    """
    kind, iri = p[1]
    if kind is consts.VSLO:
        _ctx(p).subjectLocator_variable(iri)
    else:
        _ctx(p).subjectLocator(iri)


def p_identity_iid(p):
    """\
    identity        : iid
    """
    kind, iri = p[1]
    if kind is consts.VIID:
        _ctx(p).itemIdentifier_variable(iri)
    else:
        _ctx(p).itemIdentifier(iri)


def p_args(p):
    """\
    args            : arg
                    | args COMMA arg
    """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1]
        p[0].append(p[3])


def p_arg(p):
    """\
    arg             : topic_ref
                    | literal_no_qname
    """
    p[0] = p[1]


def p_tpl_def(p):
    """\
    tpl_def         : tpl_head KW_END
                    | tpl_head tpl_body KW_END
    """
    _ctx(p).end_template()


def p_tpl_head(p):
    """\
    tpl_head        : KW_DEF IDENT LPAREN opt_params RPAREN
    """
    _ctx(p).start_template(p[2], p[4])


def p_opt_params(p):
    """\
    opt_params      : 
                    | variables
    """
    p[0] = () if len(p) == 1 else p[1]


def p_variables(p):
    """\
    variables       : variable
                    | variables COMMA variable
    """ 
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1]
        p[0].append(p[3])


def p_tpl_call_no_args(p):
    """\
    tpl_call        : IDENT LPAREN RPAREN
    """
    _ctx(p).call_template(p[1], [])  # Args MUST be modifable


def p_tpl_call(p):
    """\
    tpl_call        : tpl_call_or_assoc_start opt_more_args RPAREN
    """
    name, topicref = p[1]
    args = p[2]
    args.insert(0, topicref)
    _ctx(p).call_template(name, args)


def p_tpl_call2(p):
    """\
    tpl_call        : IDENT LPAREN literal_no_qname opt_more_args RPAREN
    """
    args = [p[3]]
    args.extend(p[4])
    _ctx(p).call_template(p[1], args)


def p_opt_more_args(p):
    """\
    opt_more_args   : 
                    | COMMA args
    """
    p[0] = len(p) == 3 and p[2] or []


def p_string(p):
    """\
    string          : STRING
    """
    p[0] = consts.STRING, unescape_string(p[1])


def p_literal_no_qname(p):
    """\
    literal_no_qname : string
                     | variable
    """
    p[0] = p[1]


def p_literal_no_qname_explicit_datatype(p):
    """\
    literal_no_qname : STRING DOUBLE_CIRCUMFLEX qiri
    """
    p[0] = consts.LITERAL, (unescape_string(p[1]), p[3])


def p_literal_no_qname_decimal(p):
    """\
    literal_no_qname : DECIMAL 
    """
    p[0] = consts.DECIMAL, p[1]


def p_literal_no_qname_integer(p):
    """\
    literal_no_qname : INTEGER
    """
    p[0] = consts.INTEGER, p[1]


def p_literal_no_qname_ctm_integer(p):
    """\
    literal_no_qname : STAR
    """
    p[0] = consts.CTM_INTEGER, p[1]


def p_literal_no_qname_date(p):
    """\
    literal_no_qname : DATE
    """
    p[0] = consts.DATE, p[1]


def p_literal_no_qname_datetime(p):
    """\
    literal_no_qname : DATE_TIME
    """
    p[0] = consts.DATE_TIME, p[1]


def p_literal(p):
    """\
    literal         : literal_no_qname
                    | qiri
    """
    p[0] = p[1]


def _parser(p):
    """\
    
    """
    return p.parser


def _ctx(p):
    return _parser(p).content_handler


def _env(p):
    """\
    
    """
    return _ctx(p).environment


def p_error(p):
    #TODO: Better error reporting (line, col, token)
    raise mio.MIOException('Unexpected token "%r"' % p)

