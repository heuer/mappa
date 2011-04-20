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
import re
from tm.mql import InvalidQueryError
from mql.tolog import consts, lexer
from mql.tolog.utils import is_builtin_predicate

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


# Taken from mio.ctm

# Start of an identifier
_ident_start = ur'[a-zA-Z_]|[\u00C0-\u00D6]|[\u00D8-\u00F6]' + \
                ur'|[\u00F8-\u02FF]|[\u0370-\u037D]' + \
                ur'|[\u037F-\u1FFF]|[\u200C-\u200D]' + \
                ur'|[\u2070-\u218F]|[\u2C00-\u2FEF]' + \
                ur'|[\u3001-\uD7FF]|[\uF900-\uFDCF]|[\uFDF0-\uFFFD]'

_ident_part = ur'%s|[\-0-9]|[\u00B7]|[\u0300-\u036F]|[\u203F-\u2040]' % _ident_start

_variable = ur'\$((?:%s)+(?:\.*(?:%s))*)' % (_ident_start, _ident_part)

find_ctm_variables = re.compile(_variable).findall


def p_noop(p): # Handles all grammar rules where the result is not of interest
    """\
    instance        : head
                    | head statement
                    | statement
    head            : rule
                    | directive
                    | head directive
                    | head rule
    directive       : using_directive
                    | prefix_directive
                    | import_directive
                    | version_directive
    statement       : query
                    | insert
                    | merge
                    | delete
                    | update
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
    opt_from_clause : 
                    | from_clause
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

def p_delete(p):
    """\
    delete          : KW_DELETE _start_delete delete_element opt_from_clause
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
    insert          : KW_INSERT _start_insert fragment opt_from_clause
    """
    _handler(p).endInsert()

def p__start_insert(p): # Inline action
    """\
    _start_insert   : 
    """
    _handler(p).startInsert()

def p_fragment(p):
    """\
    fragment        : TM_FRAGMENT
    """
    fragment = p[1]
    handler = _handler(p)
    handler.startFragment()
    handler.fragmentContent(fragment)
    for var in find_ctm_variables(fragment):    
        handler.variable(var)
    handler.endFragment()

def p_update(p):
    """\
    update          : KW_UPDATE _start_update function_call opt_from_clause
    """
    _handler(p).endUpdate()

def p__start_update(p): # Inline action
    """\
    _start_update   : 
    """
    _handler(p).startUpdate()

def p_merge(p):
    """\
    merge           : KW_MERGE _start_merge literal COMMA literal opt_from_clause
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
    from_clause     : KW_FROM _start_where clauselist
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

def p_version_directive(p):
    """\
    version_directive : DIR_VERSION INTEGER
    """

def p_import_directive(p):
    """\
    import_directive : KW_IMPORT iri_or_string KW_AS IDENT
    """
    _handle_prefix(p.parser, p[4], p[2], consts.MODULE)
    #TODO: Import 

def p_select_query(p):
    """\
    select_query    : KW_SELECT _start_select select_elements from_clause opt_tail opt_qm
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
    p[0] = consts.QNAME, (consts.IRI, p[1])

def p_qname_CURIE(p):
    """\
    qname           : CURIE
    """
    p[0] = consts.CURIE, (consts.IRI, p[1])

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
    kind, (k, value) = p[2]
    p[0] = kind, (consts.SLO, value)

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
    kind, (k, value) = p[2]
    p[0] = kind, (consts.IID, value)    

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
    _handler(p).endRule()

def p__start_rule(p): # Inline action
    """\
    _start_rule     : 
    """
    def make_variables(args):
        return [v[1] for v in args if v[0] == consts.VARIABLE]
    (kind, name), args = p[-2]
    # 'predclause' may contain a name which is not an IDENT or bound arguments
    if consts.IDENT != kind:
        raise InvalidQueryError('Invalid rule name "%s".' % name)
    params = make_variables(args)
    if len(params) != len(args):
        raise InvalidQueryError('The rule head of "%s" contains a non-variable parameter' % name)
    p.parser.rule_names.append(name)
    _handler(p).startRule(name, params)


_PREDICATE = 'Predicate'
_OCC_PREDICATE = 'Occurrence' + _PREDICATE
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
            predicate_kind = _OCC_PREDICATE
        elif kind in (consts.QNAME, consts.CURIE):
            print name
            prefix = name[1].split(':')[0]
            print '-..................', prefix
            binding_kind = p.parser.prefixes[prefix][0]
            if binding_kind != consts.MODULE:
                predicate_kind = _OCC_PREDICATE
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
    datatype        : STRING
                    | IRI
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
    existing = parser.prefixes.get(ident)
    if existing:
        existing_kind, existing_iri = existing
        if existing_kind != kind or existing_iri != iri:
            raise InvalidQueryError('The prefix "%s" is already bound to <%s>' % (ident, iri))
    else:
        parser.prefixes[ident] = (kind, iri)
        parser.handler.namespace(ident, iri, kind)
                   

def _to_event(handler, arg, stringtoiri=False):
    kind, name = arg
    meth = consts.get_name(kind)
    if not meth:
        print 'unhandled', kind #TODO
        return
    if stringtoiri and meth == 'string':
        meth = 'iri'
    method = getattr(handler, meth)
    if kind in (consts.QNAME, consts.CURIE):
        method(consts.get_name(name[0]), name[1])
    else:
        method(name)

def _arguments_to_events(handler, args, stringtoiri=False):
    for kind, name in args:
        _to_event(handler, (kind, name), stringtoiri)

if __name__ == '__main__':
    test_input = (
"""\
base-locator($LOC)?
""",
"""\
base-locator("http://some.base.locator/somewhere")?
""",
"""\
base-locator(<http://some.base.locator/somewhere>)?
""",
#"""\
#base-locator("http://some.base.locator/somewhere"^^xsd:anyURI)?
#""",
"""
born-in(Entenhausen: city, $p: person)?
""",
"""\
instance-of($TOPIC, $TYPE)?
""",
"""\
born-in($PERSON : person, $CITY : place),
located-in($CITY : containee, italy : container)?
""",
"""
select $PERSON from
  born-in($PERSON : person, $CITY : place),
  located-in($CITY : containee, italy : container)?
""",
"""
select $A, count($B) from
  composed-by($A : composer, $B : opera)?
""",
"""
  select $A, count($B) from
    composed-by($A : composer, $B : opera)
  order by $B desc?
""",
"""
date-of-birth($PERSON, "1867 (24 Mar)")?
""",
"""
homepage($TOPIC, "http://www.puccini.it")?
""",
"""
select $OPERA from
  { premiere($OPERA : opera, milano : place) | 
    premiere($OPERA : opera, $THEATRE : place), 
    located-in($THEATRE : containee, milano : container) }?
""",
"""
instance-of($OPERA, opera),
{ premiere($OPERA : opera, %param% : place) }?
""",
"""
instance-of($OPERA, opera),
{ premiere($OPERA : opera, $THEATRE : place), 
  instance-of($THEATRE, theatre) }?
""",
"""
influenced-by($A, $B) :- {
  pupil-of($A : pupil, $B : teacher) |
  composed-by($OPERA : opera, $A : composer),
  based-on($OPERA : result, $WORK : source),
  written-by($WORK : work, $B : writer)
}.
""",
"""
select $TOP from
  i"http://www.topicmaps.org/xtm/1.0/core.xtm#superclass-subclass"(
    $TOP : i"http://www.topicmaps.org/xtm/1.0/core.xtm#superclass",
    $SUB : i"http://www.topicmaps.org/xtm/1.0/core.xtm#subclass"),
  not(i"http://www.topicmaps.org/xtm/1.0/core.xtm#superclass-subclass"(
    $OTHER : i"http://www.topicmaps.org/xtm/1.0/core.xtm#superclass",
    $TOP : i"http://www.topicmaps.org/xtm/1.0/core.xtm#subclass"))?
""",
"""
import "opera.tl" as opera

instance-of($COMPOSER, composer),
opera:influenced-by($COMPOSER, $INFLUENCE),
born-in($INFLUENCE : person, $PLACE : place),
not(located-in($PLACE : containee, italy : container))?
""",
"""
select $A, count($B) from
  composed-by($A : composer, $B : opera)
order by $B desc LiMiT 1?
""",
"""
instance-of($OPERA, opera)
order by $OPERA limit 10 offset 10?
""",
"""
premiere-date($OPERA, $DATE),
$DATE < "1900"?
""",
"""
date-of-birth($PERSON1, $DATE),
date-of-birth($PERSON2, $DATE),
$PERSON1 /= $PERSON2?
""",
"""
select $UPNAME from
  instance-of($PERSON, person), name($PERSON, $NAME),
  substring($NAME, 0, 1, $FIRST), translate($FIRST, "abcdef...", "ABCDEF...", $U1),
  substring($NAME, 1, 1000, $REST), concat($U1, $REST, $UPNAME)
order by $UPNAME?
""",
'''INSERT
  tolog-updates isa update-language;
    - "tolog updates".''',
'''INSERT
  from-hell
    - "I am from hell".''',
'''import "http://psi.ontopia.net/tolog/string/" as str
  insert $topic $psi . from
  article-about($topic, $psi),
  str:starts-with($psi, "http://en.wikipedia.org/wiki/")''',
'''update value($TN, "Ontopia") from
  topic-name(oks, $TN)''',
'''merge $T1, $T2 from
  email($T1, $EMAIL),
  email($T2, $EMAIL)''',
'''
select $x from { bla($x) || blub($x) } ?
''',
'''
using x for i"bla"
using y for s"blub"
using z for a"blub"
''',
'''
update value(@2312, "Ontopia")
''',
'''
instance-of($OPERA, opera),
{ premiere($OPERA : opera, $THEATRE : place), 
  instance-of($THEATRE, theatre) }?
''',
'''
instance-of($OPERA, opera),
{ premiere($OPERA : opera, $THEATRE : place), 
  instance-of($THEATRE, theatre) }?
''',
'''
value($x, "semagia"), datatype($x, xsd:string), value($y, "Semagia"), { datatype($y, xsd:string) }?
''',
'''
scope($occ, a), scope($occ, b), { scope($occ, c) }, scope($occ, d), scope($name, e) ?
''',
'''
association($a), type($a, x)?
''',
'''
association($a), reifies(x, $a)?
''',
'''
occurrence($A, $O), type($O, rekkefolge), value($O, $VALUE)?
''',
'''
b($A, ^<http://www.semagia.com/>)?
''',
'''
b($A, 2011-02-23)?
''',
'''
b($A, 1)?
''',
'''
b($A, 1.2)?
''',
'''
b($A, 2011-02-23T23:00:00)?
''',
'''
b($A, "Tritra"^^<http://www.example.org/>)?
''',
'''
base-locator("http://www.semagia.com/")?
''',
'''
select $x where bla($blub)
''',
'''
update resource(@2312, "http://www.semagia.com/") where bla($blub)
''',
'''
association($a), association-role($a, $r)
''',
'''
topic($t), {subject-identifier($t, <jjj>)}, type($x, $t)
''',
'''
role-player($x, bla), type($x, $t)
''',
'''
select $TYPE, $VALUE from
  occurrence(topic, $OCC),
  type($OCC, $TYPE),
  { resource($OCC, $VALUE) | value($OCC, $VALUE) }?
''',
'''
%prefix ex <http://psi.example.org/>

=[ex:/onto/homepage]($T, $V),
^[ex:/onto/homepage]($T, $V),
=ex:xnxnx($T, $V),
^ex:ddkdk($T, $V)
'''
    )
    from ply import yacc
    from tm import plyutils
    from tm.xmlutils import EtreeXMLWriter
    from mql.tolog import lexer as lexer_mod
    from mql.tolog.handler import XMLHandler
    from lxml import etree
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
            writer = EtreeXMLWriter()
            parse(data, XMLHandler(writer))
            print etree.tostring(writer.getroot(), pretty_print=True)
        except Exception, ex:
            print data
            raise ex
