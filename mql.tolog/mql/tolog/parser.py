# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2012 -- Lars Heuer - Semagia <http://www.semagia.com/>.
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
tolog parser.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD License
"""
from __future__ import absolute_import
from tm.mql import InvalidQueryError
from mql.tolog import consts, lexer
from mql.tolog.utils import is_builtin_predicate, is_module_iri

tokens = lexer.tokens # Just to get rid of unused import warnings

def initialize_parser(parser, handler, tolog_plus=False):
    """\
    Initializes the parser.

    `handler`
        A handler which receives the events.
    """
    parser.handler = handler
    parser.prefixes = {}
    parser.rule_names = []
    parser.tolog_plus = tolog_plus

def p_noop(p): # Handles all grammar rules where the result is not of interest
    """\
    instance        : prolog head
                    | prolog head statement
                    | prolog statement
    prolog          :
                    | version_directive
                    | version_directive base_directive
                    | base_directive
    head            : rule
                    | directive
                    | head directive
                    | head rule
    directive       : using_directive
                    | prefix_directive
                    | import_directive
    statement       : query
                    | insert
                    | merge
                    | delete
                    | update
                    | create
                    | load
                    | drop
    query           : select_query
                    | clause_query
    select_elements : select_element
                    | select_elements COMMA select_element
    select_element  : count_clause
    clause_query    : clauselist opt_tail opt_qm
    clauselist      : clause
                    | clauselist COMMA clause
    clause          : orclause
                    | notclause
                    | opclause
    opt_qm          :
                    | QM  
    delete_element  : function_call
                    | paramlist
    opt_from        : 
                    | from_clause
    opt_where       : 
                    | where_clause
    opt_tail        : 
                    | tail
    tail            : order_clause opt_limit_offset
    order_elements  : order_element
                    | order_elements COMMA order_element
    opt_limit_offset : 
                     | limit_offset
    opt_more_pairs  : 
                    | COMMA pairs
    pairs           : pair
                    | pairs COMMA pair
    oredclauses     : oredclause
                    | oredclauses oredclause
    oredclause      : PIPE _start_branch clauselist
                    | PIPE_PIPE _start_branch clauselist
    """
    p[0] = None


def p_create(p):
    """\
    create          : KW_CREATE qiri
    """
    handler = _handler(p)
    handler.startCreate()
    _to_event(handler, p[2])
    handler.endCreate()

def p_load(p):
    """\
    load            : KW_LOAD qiri _start_load opt_into
    """
    _handler(p).endLoad()

def p__start_load(p): # Inline action
    """\
    _start_load     : 
    """
    handler = _handler(p)
    handler.startLoad()
    _to_event(handler, p[-1])
    
def p_drop(p):
    """\
    drop            : KW_DROP qiris
    """
    handler = _handler(p)
    handler.startDrop()
    for item in p[2]:
        _to_event(handler, item)
    handler.endDrop()
    
def p_delete(p):
    """\
    delete          : KW_DELETE _start_delete delete_element opt_from opt_where
    """
    _handler(p).endDelete()

def p__start_delete(p): # Inline action
    """\
    _start_delete   : 
    """
    _handler(p).startDelete()


_IRI_FUNCTIONS = ('subject-identifier', 'subject-locator',
                  'item-identifier', 'resource')

def p_function_call(p):
    """\
    function_call   : IDENT LPAREN paramlist RPAREN
    """
    handler = _handler(p)
    name = p[1]
    handler.startFunction(name)
    _arguments_to_events(handler, p[3], stringtoiri=name in _IRI_FUNCTIONS)
    handler.endFunction()

def p_paramlist(p):
    """\
    paramlist       : param
                    | paramlist COMMA param
    """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1]
        p[0].append(p[3])

def p_param(p):
    """\
    param           : variable
                    | ref
    """
    p[0] = p[1]

def p_param_STRING(p):
    """\
    param           : STRING
    """
    p[0] = consts.STRING, p[1]
    

def p_insert(p):
    """\
    insert          : KW_INSERT _start_insert fragment opt_into opt_where
    """
    _handler(p).endInsert()

def p__start_insert(p): # Inline action
    """\
    _start_insert   : 
    """
    _handler(p).startInsert()
    
def p_opt_into(p):
    """\
    opt_into        : 
                    | KW_INTO qiris
    """
    if len(p) > 1:
        handler = _handler(p)
        handler.startInto()
        for item in p[2]:
            _to_event(handler, item)
        handler.endInto()

def p_qiris(p):
    """\
    qiris           : qiri
                    | qiris COMMA qiri
    """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1]
        p[0].append(p[3])
        
def p_fragment(p):
    """\
    fragment        : TM_FRAGMENT
    """
    import mio.ctm.utils as ctm_utils
    fragment = p[1]
    handler = _handler(p)
    for var in ctm_utils.find_variables(fragment, omit_dollar=True):
        handler.variable(var)
    handler.startFragment()
    handler.fragmentContent(fragment)
    handler.endFragment()

def p_update(p):
    """\
    update          : KW_UPDATE _start_update function_call opt_from opt_where
    """
    _handler(p).endUpdate()

def p__start_update(p): # Inline action
    """\
    _start_update   : 
    """
    _handler(p).startUpdate()

def p_merge(p):
    """\
    merge           : KW_MERGE _start_merge literal COMMA literal opt_from opt_where
    """
    _handler(p).endMerge()

def p__start_merge(p): # Inline action
    """\
    _start_merge    :
    """
    _handler(p).startMerge()

def p_literal_variable(p):
    """\
    literal         : VARIABLE
    """
    _handler(p).variable(p[1])

def p_literal_topic_ref(p):
    """\
    literal         : ref
    """
    _to_event(_handler(p), p[1])

def p_from_clause(p):
    """\
    from_clause     : KW_FROM qiris
    """
    handler = _handler(p)
    handler.startFrom()
    for item in p[2]:
        _to_event(handler, item)
    handler.endFrom()

def p_where_clause(p):
    """\
    where_clause    : KW_WHERE _start_where clauselist    
    """
    _handler(p).endWhere()

def p__start_where(p): # Inline action
    """\
    _start_where    : 
    """
    _handler(p).startWhere()

def p_using_directive(p):
    """\
    using_directive : KW_USING IDENT KW_FOR uri_ref
    """
    kind, iri = p[4]
    _handle_prefix(p.parser, p[2], iri, kind)

def p_prefix_directive(p):
    """\
    prefix_directive : DIR_PREFIX IDENT IRI
    """
    _handle_prefix(p.parser, p[2], p[3])

def p_import_directive(p):
    """\
    import_directive : KW_IMPORT iri_or_string KW_AS IDENT
                     | DIR_IMPORT IDENT IRI 
    """
    ident, iri = (p[4], p[2]) if len(p) == 5 else (p[2], p[3])
    _handle_prefix(p.parser, ident, iri, consts.MODULE)
    if not is_module_iri(iri):
        pass #TODO: Import 

def p_version_directive(p):
    """\
    version_directive : DIR_VERSION DECIMAL
    """
    version = [int(part) for part in p[2].split(u'.')]
    if version[0] != 1 or version[1] > 2:
        raise InvalidQueryError('Unknown version %s' % p[2])
    p.parser.tolog_plus = True
    p.lexer.tolog_plus = True

def p_base_directive(p):
    """\
    base_directive  : DIR_BASE IRI
    """
    _handler(p).base(p[2])

def p_select_query(p):
    """\
    select_query    : KW_SELECT _start_select select_elements opt_from where_clause opt_tail opt_qm
    """
    _handler(p).endSelect()

def p__start_select(p):
    """\
    _start_select   : 
    """
    _handler(p).startSelect()

def p_select_element(p):
    """\
    select_element  : VARIABLE
    """
    _handler(p).variable(p[1])

def p_ref(p):
    """\
    ref             : uri_ref
    """
    p[0] = p[1]

def p_qiri_IRI(p):
    """\
    qiri            : IRI
    """
    p[0] = consts.IRI, p[1]

def p_qiri_qname(p):
    """\
    qiri            : qname
    """
    p[0] = p[1]

def p_iri_or_string(p):
    """\
    iri_or_string   : IRI
                    | STRING
    """
    p[0] = p[1]

def p_ref_IDENT(p):
    """\
    ref             : IDENT
    """
    p[0] = consts.IDENT, p[1]

def p_ref_OID(p):
    """\
    ref             : OID
    """
    p[0] = consts.OID, p[1]

def p_variable(p):
    """\
    variable        : VARIABLE
    """
    p[0] = consts.VARIABLE, p[1]

def p_qname_QNAME(p):
    """\
    qname           : QNAME
    """
    prefix, lp = p[1].split(':')
    res = p.parser.prefixes.get(prefix)
    if not res:
        raise InvalidQueryError('The prefix "%s" is not defined' % prefix)
    p[0] = consts.QNAME, (res[0], prefix, lp)

def p_qname_CURIE(p):
    """\
    qname           : CURIE
    """
    prefix, lp = p[1].split(':', 1)
    res = p.parser.prefixes.get(prefix)
    if not res:
        raise InvalidQueryError('The prefix "%s" is not defined' % prefix)
    p[0] = consts.CURIE, (res[0], prefix, lp)

def p_uri_ref(p):
    """\
    uri_ref         : sid
                    | slo
                    | iid
    """
    p[0] = p[1]

def p_sid_SID(p):
    """\
    sid             : SID
    """
    p[0] = consts.SID, p[1]

def p_sid_qiri(p):
    """\
    sid             : qiri
    """
    p[0] = p[1]

def p_slo(p):
    """\
    slo             : SLO
                    | EQ IRI
    """
    p[0] = consts.SLO, p[len(p)-1]

def p_slo_QNAME(p):
    """\
    slo         : EQ qname
    """
    kind, (k, prefix, lp) = p[2]
    p[0] = kind, (consts.SLO, prefix, lp)

def p_iid(p):
    """\
    iid             : IID
                    | CIRCUMFLEX IRI
    """
    p[0] = consts.IID, p[len(p)-1]

def p_iid_QNAME(p):
    """\
    iid            : CIRCUMFLEX qname
    """
    kind, (k, prefix, lp) = p[2]
    p[0] = kind, (consts.IID, prefix, lp)    

def p_count_clause(p):
    """\
    count_clause    : KW_COUNT LPAREN VARIABLE RPAREN
    """
    _handler(p).count(p[3])

def p_order_clause(p):
    """\
    order_clause    : KW_ORDER KW_BY _start_order order_elements
    """
    _handler(p).endOrderBy()

def p__start_order(p): # Inline action
    """\
    _start_order    : 
    """
    _handler(p).startOrderBy()

def p_order_element(p):
    """\
    order_element   : VARIABLE direction
    """
    if p[2] == consts.ASC:
        _handler(p).ascending(p[1])
    else:
        _handler(p).descending(p[1])

def p_direction_ASC(p):
    """\
    direction       : 
                    | KW_ASC
    """
    p[0] = consts.ASC  # Even if 'empty' since ASC is the default

def p_direction_DESC(p):
    """\
    direction       : KW_DESC
    """
    p[0] = consts.DESC

def p_limit_offset(p):
    """\
    limit_offset    : KW_OFFSET INTEGER
                    | KW_LIMIT INTEGER
                    | KW_LIMIT INTEGER KW_OFFSET INTEGER
    """
    handler = _handler(p)
    handler.startPagination()
    if len(p) == 3:
        getattr(handler, p[1].lower())(int(p[2]))
    else:
        handler.limit(int(p[2]))
        handler.offset(int(p[4]))
    handler.endPagination()

def p_rule(p):
    """\
    rule            : predclause IMPLIES _start_rule clauselist DOT
    """
    handler = _handler(p)
    handler.endBody()
    handler.endRule()

def p__start_rule(p): # Inline action
    """\
    _start_rule     : 
    """
    (kind, name), args = p[-2]
    # 'predclause' may contain a name which is not an IDENT or bound arguments
    if consts.IDENT != kind:
        raise InvalidQueryError('Invalid rule name "%s".' % name)
    p.parser.rule_names.append(name)
    handler = _handler(p)
    handler.startRule(name)
    for arg in args:
        if arg[0] != consts.VARIABLE:
            raise InvalidQueryError('The rule head of "%s" contains a non-variable parameter' % name)
        handler.variable(arg[1])
    handler.startBody()
    


_PREDICATE = 'Predicate'
_DYN_PREDICATE = 'Dynamic' + _PREDICATE
_IRI_PREDICATES = ('base-locator', 'datatype', 'item-identifier',
             'subject-locator', 'subject-identifier', 'resource')

def p_clause_predcause(p):
    """\
    clause          : predclause
    """
    (kind, name), args = p[1]
    handler = _handler(p)
    if kind == consts.IDENT and is_builtin_predicate(name):
        handler.startBuiltinPredicate(name)
        _arguments_to_events(handler, args, stringtoiri=name in _IRI_PREDICATES)
        handler.endBuiltinPredicate()
    else:
        predicate_kind = None
        arity = len(args)
        if arity == 2 and kind == consts.IDENT and name not in p.parser.rule_names:
            predicate_kind = _DYN_PREDICATE
        elif kind in (consts.QNAME, consts.CURIE):
            prefix = name[1].split(':')[0]
            binding_kind = p.parser.prefixes[prefix][0]
            if binding_kind != consts.MODULE:
                predicate_kind = _DYN_PREDICATE
        if predicate_kind is None:
            predicate_kind = _PREDICATE
        getattr(handler, 'start' + predicate_kind)()
        handler.startName()
        _to_event(handler, (kind, name))
        handler.endName()
        _arguments_to_events(handler, args)
        getattr(handler, 'end' + predicate_kind)()

def p_clause_assoc_predicate(p):
    """\
    clause          : ref LPAREN _first_pair opt_more_pairs RPAREN
    """
    _handler(p).endAssociationPredicate()

# Correct grammar for roles/pairs:
#
#   pair ::= expr COLON ref
#
# Switched to more lenient grammar for tolog+ where
# the type/player tuple is reversed
#
# Correct tolog 1.2:
#
#     premiere($OPERA : opera, $THEATRE : place)
#
# tolog+:
#
#     premiere(opera: $OPERA, place: $THEATRE)
# 

def p__first_pair(p): # Inline action
    """\
    _first_pair     : expr COLON expr
    """
    handler = _handler(p)
    handler.startAssociationPredicate()
    handler.startName()
    _to_event(handler, p[-2])
    handler.endName()
    _handle_pair(p, p[1], p[3])

def p_pair(p):
    """\
    pair            : expr COLON expr
    """
    _handle_pair(p, p[1], p[3])

def p_predclause(p):
    """\
    predclause      : ref LPAREN arguments RPAREN
    """
    p[0] = p[1], p[3]

def p_arguments(p):
    """\
    arguments       : expr
                    | arguments COMMA expr
    """
    if len(p) == 2:
        p[0] = [p[1]]
    else:
        p[0] = p[1]
        p[1].append(p[3])

def p_expr(p):
    """\
    expr            : variable
                    | ref
                    | value
                    | parameter
    """
    p[0] = p[1]


_OP2NAME = {
    '=': 'eq',
    '/=': 'ne',
    '<': 'lt',
    '<=': 'le',
    '>': 'gt',
    '>=': 'ge',
}

def p_opclause(p):
    """\
    opclause        : expr EQ expr
                    | expr NE expr
                    | expr LE expr
                    | expr LT expr
                    | expr GE expr
                    | expr GT expr
    """
    handler = _handler(p)
    name = _OP2NAME[p[2]]
    handler.startInfixPredicate(name)
    _to_event(handler, p[1])
    _to_event(handler, p[3])
    handler.endInfixPredicate()

def p_orclause(p):
    """\
    orclause        : LCURLY _start_or clauselist RCURLY
                    | LCURLY _start_or clauselist oredclauses RCURLY
    """
    handler = _handler(p)
    handler.endBranch()
    handler.endOr()

def p__start_or(p): # Inline action
    """\
    _start_or       :
    """
    handler = _handler(p)
    handler.startOr()
    handler.startBranch(False)

def p__start_branch(p): # Inline action
    """\
    _start_branch   :
    """
    handler = _handler(p)
    handler.endBranch()
    handler.startBranch(p[-1] == '||')

def p_notclause(p):
    """\
    notclause       : KW_NOT _start_not LPAREN clauselist RPAREN
    """
    _handler(p).endNot()

def p__start_not(p): # Inline action
    """\
    _start_not      : 
    """
    _handler(p).startNot()

def p_parameter(p):
    """\
    parameter       : PARAM
    """
    p[0] = consts.PARAM, p[1]

def p_value_literal_iri(p):
    """\
    value           : STRING DOUBLE_CIRCUMFLEX datatype
    """
    p[0] = consts.LITERAL, (p[1], p[3])

def p_datatype_iri(p):
    """\
    datatype        : IRI
    """
    p[0] = consts.IRI, p[1]

def p_datatype_qname(p):
    """\
    datatype        : qname
    """
    p[0] = p[1]

def p_value_STRING(p):
    """\
    value           : STRING
    """
    p[0] = consts.STRING, p[1]

def p_value_INTEGER(p):
    """\
    value           : INTEGER
    """
    p[0] = consts.INTEGER, p[1]

def p_value_DECIMAL(p):
    """\
    value           : DECIMAL
    """
    p[0] = consts.DECIMAL, p[1]

def p_value_DATE(p):
    """\
    value           : DATE
    """
    p[0] = consts.DATE, p[1]

def p_value_DATE_TIME(p):
    """\
    value           : DATE_TIME
    """
    p[0] = consts.DATE_TIME, p[1]

def p_value_IRI(p):
    """\
    value           : IRI
    """
    p[0] = consts.IRI, p[1]

def p_error(p):
    raise InvalidQueryError(p)

def _handler(p):
    return p.parser.handler

def _resolve_qnames(p):
    return p.parser.resolve_qnames

def _handle_pair(p, first, second):
    if p.parser.tolog_plus:
        type, player = first, second
    else:
        player, type = first, second
    handler = _handler(p)
    handler.startPair()
    handler.startType()
    _to_event(handler, type)
    handler.endType()
    handler.startPlayer()
    _to_event(handler, player)
    handler.endPlayer()
    handler.endPair()

def _handle_prefix(parser, ident, iri, kind=None):
    kind = kind or consts.IRI
    existing = parser.prefixes.get(ident)
    if existing:
        existing_kind, existing_iri = existing
        if existing_kind != kind or existing_iri != iri:
            raise InvalidQueryError('The prefix "%s" is already bound to <%s>' % (ident, existing_iri))
    else:
        parser.prefixes[ident] = (kind, iri)
        parser.handler.namespace(ident, iri, kind)
                   

def _to_event(handler, arg, stringtoiri=False):
    kind, name = arg
    meth = consts.get_name(kind)
    if not meth:
        raise Exception('Unhandled: "%r"' % kind) #TODO: Better exception
    if stringtoiri and meth == 'string':
        meth = 'iri'
    method = getattr(handler, meth)
    if kind in (consts.QNAME, consts.CURIE):
        # name is a tuple: kind-of-namespace (MODULE, SID, IID, SLO), prefix, localpart
        method(*name)
    elif kind == consts.LITERAL:
        value, datatype = name
        datatype_kind = datatype[0]
        if datatype_kind == consts.IRI:
            method(value, datatype_iri=datatype[1])
        else:
            _, prefix, lp = datatype[1]
            method(value, datatype_prefix=prefix, datatype_lp=lp)
    else:
        method(name)

def _arguments_to_events(handler, args, stringtoiri=False):
    for kind, name in args:
        _to_event(handler, (kind, name), stringtoiri)

if __name__ == '__main__':
    test_input = (

    )
    from ply import yacc
    from tm import plyutils, xmlutils
    from mql.tolog import lexer as lexer_mod
    from mql.tolog.handler import XMLHandler
    from lxml import etree
    import lxml.sax
    def parse(data, handler):
        parser = yacc.yacc(debug=True)
        initialize_parser(parser, handler)
        handler.start()
        parser.parse(data, lexer=plyutils.make_lexer(lexer_mod))
        handler.end()

    for cnt, data in enumerate(test_input):
        print(cnt)
        print(data)
        try:
            contenthandler = lxml.sax.ElementTreeContentHandler()
            handler = XMLHandler(xmlutils.SAXSimpleXMLWriter(contenthandler))
            parse(data, handler)
            print etree.tostring(contenthandler.etree, pretty_print=True)
        except Exception, ex:
            print data
            raise ex
