# -*- coding: utf-8 -*-
#
# Copyright (c) 2007 - 2014 -- Lars Heuer - Semagia <http://www.semagia.com/>.
# All rights reserved.
#
# BSD license.
#
"""\
Tests against the parser.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD License
"""
from tm.mql import InvalidQueryError
import mql.tolog as tolog
from mql.tolog.handler import NoopParserHandler


def parse(data, handler=None, tolog_plus=True):
    tolog.parse(data, handler or NoopParserHandler(),
                iri=u'http://www.semagia.com/tolog-test/',
                tolog_plus=tolog_plus)


def fail(msg): raise AssertionError(msg)


def test_duplicate_prefixes_invalid():
    def check(data):
        try:
            parse(data)
            fail('Expected an error since x is bound to different IRIs')
        except InvalidQueryError:
            pass
    data = (u'''using x for i"http://www.semagia.com/test"
using x for i"http://www.example.org/"
''',
            u'''%prefix x <http://www.semagia.com/>
%prefix x <http://www.example.org/>
''',
            u'''using x for i"http://www.semagia.com/test"
%prefix x <http://www.semagia.com/>''',
            )
    for d in data:
        yield check, d


def test_duplicate_prefixes():
    data = (u'''%prefix x <http://www.semagia.com/>
%prefix x <http://www.semagia.com/>
''',
            # Probably rejected by Ontopia
            u'''using x for i"http://www.semagia.com/test"
using x for i"http://www.semagia.com/test"
''',
            )
    for d in data:
        yield parse, d


def test_base():
    data = (u'''%base <http://www.semagia.com/> %prefix x <http://www.semagia.com/x>''',)
    for d in data:
        yield parse, d


def test_base_illegal():
    def check(data):
        try:
            parse(data)
            fail('Expected an error since %base is not the first directive')
        except InvalidQueryError:
            pass
    data = (u'''%prefix x <http://www.semagia.com/x>
%base <http://www.semagia.com/>''',)
    for d in data:
        yield check, d


def test_accept():
    for d in _ACCEPT_DATA:
        tolog_plus = True
        if isinstance(d, tuple):
            d, tolog_plus = d
        yield parse, d, None, tolog_plus


_ACCEPT_DATA = (
    u"""\
    %version 1.0
    %prefix ident <http://www.semagia.com/x>
    """,
    u"""\
    base-locator($LOC)?
    """,
    u"""\
    base-locator("http://some.base.locator/somewhere")?
    u""",
    u"""\
    base-locator(<http://some.base.locator/somewhere>)?
    """,
    u"""\
    %prefix xsd <http://www.w3.org/2001/XMLSchema#>
    base-locator("http://some.base.locator/somewhere"^^xsd:anyURI)?
    u""",
    u"""
    born-in(Entenhausen: city, $p: person)?
    """,
    u"""\
    instance-of($TOPIC, $TYPE)?
    """,
    u"""\
    born-in($PERSON : person, $CITY : place),
    located-in($CITY : containee, italy : container)?
    """,
    (u"""\
    select $PERSON from
      born-in($PERSON : person, $CITY : place),
      located-in($CITY : containee, italy : container)?
    """, False),
    (u"""\
    select $A, count($B) from
      composed-by($A : composer, $B : opera)?
    """, False),
    (u"""\
      select $A, count($B) from
        composed-by($A : composer, $B : opera)
      order by $B desc?
    """, False),
    """
    date-of-birth($PERSON, "1867 (24 Mar)")?
    """,
    """
    homepage($TOPIC, "http://www.puccini.it")?
    """,
    (u"""\
    select $OPERA from
      { premiere($OPERA : opera, milano : place) | 
        premiere($OPERA : opera, $THEATRE : place), 
        located-in($THEATRE : containee, milano : container) }?
    """, False),
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
    (u"""\
    select $TOP from
      i"http://www.topicmaps.org/xtm/1.0/core.xtm#superclass-subclass"(
        $TOP : i"http://www.topicmaps.org/xtm/1.0/core.xtm#superclass",
        $SUB : i"http://www.topicmaps.org/xtm/1.0/core.xtm#subclass"),
      not(i"http://www.topicmaps.org/xtm/1.0/core.xtm#superclass-subclass"(
        $OTHER : i"http://www.topicmaps.org/xtm/1.0/core.xtm#superclass",
        $TOP : i"http://www.topicmaps.org/xtm/1.0/core.xtm#subclass"))?
    """, False),
    """
    import "opera.tl" as opera
    
    instance-of($COMPOSER, composer),
    opera:influenced-by($COMPOSER, $INFLUENCE),
    born-in($INFLUENCE : person, $PLACE : place),
    not(located-in($PLACE : containee, italy : container))?
    """,
    (u"""\
    select $A, count($B) from
      composed-by($A : composer, $B : opera)
    order by $B desc LiMiT 1?
    """, False),
    u"""
    instance-of($OPERA, opera)
    order by $OPERA limit 10 offset 10?
    """,
    u"""
    premiere-date($OPERA, $DATE),
    $DATE < "1900"?
    """,
    u"""
    date-of-birth($PERSON1, $DATE),
    date-of-birth($PERSON2, $DATE),
    $PERSON1 /= $PERSON2?
    """,
    (u"""\
    select $UPNAME from
      instance-of($PERSON, person), name($PERSON, $NAME),
      substring($NAME, 0, 1, $FIRST), translate($FIRST, "abcdef...", "ABCDEF...", $U1),
      substring($NAME, 1, 1000, $REST), concat($U1, $REST, $UPNAME)
    order by $UPNAME?
    """, False),
    u'''INSERT
tolog-updates isa update-language;
  - "tolog updates".''',
    '''INSERT
from-hell
- "I am from hell".''',
    (u'''import "http://psi.ontopia.net/tolog/string/" as str
   insert $topic $psi . from
   article-about($topic, $psi),
   str:starts-with($psi, "http://en.wikipedia.org/wiki/")''', False),
    (u'''update value($TN, "Ontopia") from
   topic-name(oks, $TN)''', False),
    (u'''merge $T1, $T2 from
   email($T1, $EMAIL),
   email($T2, $EMAIL)''', False),
    (u'''
    select $x from { bla($x) || blub($x) } ?
    ''', False),
    u'''
    using x for i"bla"
    using y for s"blub"
    using z for a"blub"
    ''',
    u'''
    update value(@2312, "Ontopia")
    ''',
    u'''
    instance-of($OPERA, opera),
    { premiere($OPERA : opera, $THEATRE : place), 
      instance-of($THEATRE, theatre) }?
    ''',
    u'''
    instance-of($OPERA, opera),
    { premiere($OPERA : opera, $THEATRE : place), 
      instance-of($THEATRE, theatre) }?
    ''',
    u'''
    %prefix xsd <http://www.bla.com/>
    value($x, "semagia"), datatype($x, xsd:string), value($y, "Semagia"), { datatype($y, xsd:string) }?
    ''',
    u'''
    scope($occ, a), scope($occ, b), { scope($occ, c) }, scope($occ, d), scope($name, e) ?
    ''',
    u'''
    association($a), type($a, x)?
    ''',
    u'''
    association($a), reifies(x, $a)?
    ''',
    u'''
    occurrence($A, $O), type($O, rekkefolge), value($O, $VALUE)?
    ''',
    u'''
    b($A, ^<http://www.semagia.com/>)?
    ''',
    u'''
    b($A, 2011-02-23)?
    ''',
    u'''
    b($A, 1)?
    ''',
    u'''
    b($A, 1.2)?
    ''',
    u'''
    b($A, 2011-02-23T23:00:00)?
    ''',
    u'''
    b($A, "Tritra"^^<http://www.example.org/>)?
    ''',
    u'''
    base-locator("http://www.semagia.com/")?
    ''',
    u'''
    select $x where bla($blub)
    ''',
    u'''
    update resource(@2312, "http://www.semagia.com/") where bla($blub)
    ''',
    u'''
    association($a), association-role($a, $r)
    ''',
    u'''
    topic($t), {subject-identifier($t, <jjj>)}, type($x, $t)
    ''',
    u'''
    role-player($x, bla), type($x, $t)
    ''',
    (u'''
    select $TYPE, $VALUE from
      occurrence(topic, $OCC),
      type($OCC, $TYPE),
      { resource($OCC, $VALUE) | value($OCC, $VALUE) }?
    ''', False),
    u'''
    %base <http://abc.com/>
    %prefix ex <http://psi.example.org/>
    
    [ex:/onto/homepage]($T, $V),
    =[ex:/onto/homepage]($T, $V),
    ^[ex:/onto/homepage]($T, $V),
    ex:xnxnx($T, $V),
    =ex:xnxnx($T, $V),
    ^ex:ddkdk($T, $V)
    ''',
    u'''
    using x for a"http://www.bla.com"
    using y for s"http://www.blub.com"
    using z for i"http://www.blabla.com"
    import "http://blablub.com" as a
    
    x:x($x), y:y($y), z:z($z), a:a($a), [x:x]($x), [y:y]($y), [z:z]($z), [a:a]($a)
    ''',
    u'''
    %base <http://www.semagia.com/>
    %prefix ident <http://www.semagia.com/x>
    ''',
    u'''
    %import a <http://www.semagia.com/>
    import "http://blablub.com" as b
    ''',
    u'''
    %prefix xsd <http://www.w3.org/2001/XMLSchema#>
    
    literal($o, 123), 
    literal($v, <http://www.semagia.com>), 
    literal($o2, 12.34), 
    literal($n, "foo"),
    literal($o3, "foo", xsd:int)?
    ''',
    u'''
    %version 1.2
    %prefix xsd <http://www.w3.org/2001/XMLSchema#>
    
    literal($o, 123), 
    literal($v, <http://www.semagia.com>), 
    literal($o2, 12.34), 
    literal($n, "foo"),
    literal($o3, "foo", xsd:int)?
    ''',
    u'''
    %prefix xsd <http://www.w3.org/2001/XMLSchema#>
    
    value($o, 123), 
    value($v, <http://www.semagia.com>), 
    value($o2, 12.34), 
    value($n, "foo"),
    value($o3, "foo"^^xsd:int)?
    ''',
    u'''
    load <http://www.semagia.com/tolog-xml>
    ''',
    u'''
    load <http://www.semagia.com/tolog-xml> into <http://www.semagia.com/foo>
    ''',
    u'''
    load <http://www.semagia.com/tolog-xml> into <http://www.semagia.com/foo>, <http://www.semagia.com/bar> 
    ''',
    u'''
    drop <http://www.semagia.com/tolog-xml> 
    ''',
    u'''
    create <http://www.semagia.com/tolog-xml> 
    ''',

    #
    # Not yet supported. Why did I add these queries?
    #
    #'''
    #select $x using <http://www.semagia.com/> from nonsense($x)?
    #''',
    #'''
    #select $x using <http://www.semagia.com/> where nonsense($x)?
    #'''
    )


if __name__ == '__main__':
    import nose
    nose.core.runmodule()

