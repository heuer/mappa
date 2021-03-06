# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
Linear Topic Maps Notation (LTM) 1.3 parser.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - http://www.semagia.com/
:license:      BSD license
"""
from tm import mio, XSD
from tm import TMDM, XTM_10
from mio.ltm.lexer import tokens
_TOPICNAME = mio.SUBJECT_IDENTIFIER, TMDM.topic_name
_SORT = mio.SUBJECT_IDENTIFIER, XTM_10.SORT
_DISPLAY = mio.SUBJECT_IDENTIFIER, XTM_10.DISPLAY
_ROLE_TYPE = mio.SUBJECT_IDENTIFIER, XTM_10.DEFAULT_ROLE_TYPE
del XTM_10
del TMDM
assert tokens


def _process_scope(handler, scope):
    if scope:
        handler.startScope()
        for theme in scope:
            handler.theme(theme)
        handler.endScope()


def p_noop(p):  # Handles all grammar rules where the result is unimportant
    """\
    instance        : prolog
                    | prolog tm
    tm              : topic
                    | assoc
                    | occ
                    | directive
                    | tm topic
                    | tm assoc
                    | tm occ
                    | tm directive
    prolog          :
                    | encoding_directive
                    | version_directive
                    | encoding_directive version_directive
    directive       : tm_directive
                    | prefix_directive
                    | mergemap_directive
                    | include_directive
                    | baseuri_directive
    encoding_directive : AT STRING
    opt_sids        : 
                    | sids
    sids            : sid
                    | sids sid
    opt_types       : 
                    | COLON types
    opt_names       : 
                    | names
    names           : name
                    | names name
    opt_variants    :
                    | variants
    variants        : variant
                    | variants variant
    roles           : role
                    | roles COMMA role
    """
    p[0] = None


def p_tm_directive(p):
    """\
    tm_directive    : DIR_TOPICMAP IDENT
                    | DIR_TOPICMAP TILDE IDENT
    """
    if len(p) == 3:
        _context(p).tm_iid(p[2])
    else:
        _context(p).tm_reifier(p[3])


def p_version_directive(p):
    """\
    version_directive : DIR_VERSION STRING
    """
    _context(p).check_version(p[2])


def p_prefix_directive_slo(p):
    """\
    prefix_directive : DIR_PREFIX IDENT PERCENT STRING
    """
    _context(p).register_slo_prefix(p[2], p[4])


def p_prefix_directive_sid(p):
    """\
    prefix_directive : DIR_PREFIX IDENT AT STRING
    """
    _context(p).register_sid_prefix(p[2], p[4])


def p_baseuri_directive(p):
    """\
    baseuri_directive : DIR_BASEURI STRING
    """
    _context(p).set_baseuri(p[2])


def p_mergemap_directive(p):
    """\
    mergemap_directive : DIR_MERGEMAP STRING
                       | DIR_MERGEMAP STRING STRING
    """
    iri = p[2]
    if len(p) == 3:
        _context(p).merge_ltm(iri)
    else:
        _context(p).merge(iri, p[3])


def p_include_directive(p):
    """\
    include_directive : DIR_INCLUDE STRING
    """
    _context(p).include(p[2])


def p_tid_IDENT(p):
    """\
    tid             : IDENT
    """
    p[0] = _context(p).create_topic_by_iid(p[1])


def p_tid_QNAME(p):
    """\
    tid             : QNAME
    """
    p[0] = _context(p).create_topic_by_qname(*p[1])


def p_tids(p):
    """\
    tids            : tid
                    | tids tid
    """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1]
        p[1].append(p[2])


def p_topic(p):
    """\
    topic           : LBRACK tid _start_topic opt_types opt_names opt_slo opt_sids RBRACK
    """
    _handler(p).endTopic()


def p__start_topic(p):  # Inline action
    """\
    _start_topic :
    """
    _handler(p).startTopic(p[-1])  # -1 is a topic identifier


def p_types(p):
    """\
    types           : tid
                    | types tid
    """
    _handler(p).isa(len(p) > 2 and p[2] or p[1])


def p_opt_slo(p):
    """\
    opt_slo         : 
                    | PERCENT STRING
    """
    if len(p) > 1:
        ctx = _context(p)
        ctx.handler.subjectLocator(ctx.resolve_iri(p[2]))


def p_sid(p):
    """\
    sid             : AT STRING
    """
    ctx = _context(p)
    ctx.handler.subjectIdentifier(ctx.resolve_iri(p[2]))


def p_name(p):
    """\
    name            : EQ STRING _start_name opt_sort_display opt_name_scope opt_reifier opt_variants
    """
    ctx = _context(p)
    handler = ctx.handler
    # Process display/sortname
    for v, t in p[4]:
        handler.startVariant()
        handler.startScope()
        handler.theme(t)
        handler.endScope()
        handler.value(v, XSD.string)
        handler.endVariant()
    ctx.reifier(p[6])
    handler.endName()


def p_start_name(p):
    """\
    _start_name : 
    """
    handler = _handler(p)
    handler.startName(_TOPICNAME)
    handler.value(p[-1])  # -1 is a string


def p_opt_name_scope(p):
    """\
    opt_name_scope  :
                    | SLASH tids
    """
    if len(p) == 3:
        _process_scope(_handler(p), p[2])


def p_opt_sort_display(p):
    """\
    opt_sort_display : 
                     | sortname displayname
                     | SEMI displayname
                     | sortname
    """
    l = len(p)
    if l > 1:
        if l > 2:
            p[0] = [p[2]] if p[1] == u';' else [p[1], p[2]]
        else:
            p[0] = [p[1]]  # sortname
    else:
        p[0] = []  # empty


def p_sortname(p):
    """\
    sortname        : SEMI STRING
    """
    # value, scope
    p[0] = p[2], _SORT


def p_displayname(p):
    """\
    displayname     : SEMI STRING
    """
    # value, scope
    p[0] = p[2], _DISPLAY


def p_variant(p):
    """\
    variant         : LPAREN STRING SLASH tids opt_reifier RPAREN
    """
    ctx = _context(p)
    handler = ctx.handler
    handler.startVariant()
    handler.startScope()
    for theme in p[4]:
        handler.theme(theme)
    handler.endScope()
    handler.value(p[2], XSD.string)
    ctx.reifier(p[5])
    handler.endVariant()


def p_assoc(p):
    """\
    assoc           : tid LPAREN _start_assoc roles RPAREN opt_scope opt_reifier
    """
    ctx = _context(p)
    handler = ctx.handler
    _process_scope(handler, p[6])
    ctx.reifier(p[7])
    handler.endAssociation()


def p_start_assoc(p):
    """\
    _start_assoc : 
    """
    _handler(p).startAssociation(p[-2])  # -2 is a topic identifier


def p_role(p):
    """\
    role            : _start_role player opt_role_type opt_reifier
    """
    ctx = _context(p)
    ctx.reifier(p[4])
    ctx.handler.endRole()


def p_start_role(p):
    """\
    _start_role :
    """
    handler = _handler(p)
    handler.startRole()
    handler.startPlayer()


def p_player(p):
    """\
    player          : tid
                    | topic
    """
    handler = _handler(p)
    if p[1]:
        handler.topicRef(p[1])
    handler.endPlayer()


def p_opt_role_type(p):
    """\
    opt_role_type   : 
                    | COLON tid
    """
    typ = p[2] if len(p) == 3 else _ROLE_TYPE
    _handler(p).type(typ)


def p_occ(p):
    """\
    occ             : LCURLY tid COMMA tid COMMA resource RCURLY opt_scope opt_reifier
    """
    ctx = _context(p)
    handler = ctx.handler
    handler.startTopic(p[2])
    handler.startOccurrence(p[4])
    handler.value(*p[6])
    _process_scope(handler, p[8])
    ctx.reifier(p[9])
    handler.endOccurrence()
    handler.endTopic()


def p_resource_uri(p):
    """\
    resource        : STRING
    """
    p[0] = _context(p).resolve_iri(p[1]), XSD.anyURI


def p_resource_string(p):
    """\
    resource        : DATA
    """
    p[0] = p[1], XSD.string


def p_opt_scope(p):
    """\
    opt_scope       : 
                    | SLASH themes
    """
    p[0] = p[2] if len(p) > 1 else []


def p_themes(p):
    """\
    themes          : tids
                    | tids assoc
    """
    p[0] = p[1]


def p_opt_reifier(p):
    """\
    opt_reifier     : 
                    | TILDE IDENT
    """
    p[0] = p[2] if len(p) > 1 else None


def p_error(p):
    #TODO: Better error reporting (line, col, token)
    raise mio.MIOException('Unexpected token "%r"' % p)


def _context(p):
    """\
    Returns the parser context.
    """
    return p.parser.context


def _handler(p):
    """\
    Returns the ``IMapHandler``
    """
    return p.parser.context.handler
