# -*- coding: utf-8 -*-
#
# Copyright (c) 2010 - 2011 -- Lars Heuer - Semagia <http://www.semagia.com/>.
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
Tests against the parser.

:author:       Lars Heuer (heuer[at]semagia.com)
:organization: Semagia - <http://www.semagia.com/>
:license:      BSD License
"""
import tm
from tm.mql import InvalidQueryError
import mql.tolog as tolog
from mql.tolog.handler import NoopParserHandler

def parse(data, handler=None):
    tolog.parse(tm.Source(data=data, iri='http://www.semagia.com/tolog-test/'), handler or NoopParserHandler())

def fail(msg):
    raise AssertionError(msg)

def test_duplicate_prefixes_invalid():
    def check(data):
        try:
            parse(data)
            fail('Expected an error since x is bound to different IRIs')
        except InvalidQueryError:
            pass
    data = ('''using x for i"http://www.semagia.com/test"
using x for i"http://www.example.org/"
''',
            '''%prefix x <http://www.semagia.com/>
%prefix x <http://www.example.org/>
''',
            '''using x for i"http://www.semagia.com/test"
%prefix x <http://www.semagia.com/>''',
            )
    for d in data:
        yield check, d

def test_duplicate_prefixes():
    data = ('''%prefix x <http://www.semagia.com/>
%prefix x <http://www.semagia.com/>
''',
            # Probably rejected by Ontopia
            '''using x for i"http://www.semagia.com/test"
using x for i"http://www.semagia.com/test"
''',
            )
    for d in data:
        yield parse, d

def test_base():
    data = ('''%base <http://www.semagia.com/> %prefix x <http://www.semagia.com/x>''',)
    for d in data:
        yield parse, d

def test_base_illegal():
    def check(data):
        try:
            parse(data)
            fail('Expected an error since %base is not the first directive')
        except InvalidQueryError:
            pass
    data = ('''%prefix x <http://www.semagia.com/x>
%base <http://www.semagia.com/>''',)
    for d in data:
        yield check, d

def test_accept():
    for d in _ACCEPT_DATA:
        yield parse, d


_ACCEPT_DATA = (
    """\
    %version 1.0
    %prefix ident <http://www.semagia.com/x>
    """,
    """\
    base-locator($LOC)?
    """,
    """\
    base-locator("http://some.base.locator/somewhere")?
    """,
    """\
    base-locator(<http://some.base.locator/somewhere>)?
    """,
    """\
    %prefix xsd <http://www.w3.org/2001/XMLSchema#>
    base-locator("http://some.base.locator/somewhere"^^xsd:anyURI)?
    """,
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
    %prefix xsd <http://www.bla.com/>
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
    %base <http://abc.com/>
    %prefix ex <http://psi.example.org/>
    
    [ex:/onto/homepage]($T, $V),
    =[ex:/onto/homepage]($T, $V),
    ^[ex:/onto/homepage]($T, $V),
    ex:xnxnx($T, $V),
    =ex:xnxnx($T, $V),
    ^ex:ddkdk($T, $V)
    ''',
    '''
    using x for a"http://www.bla.com"
    using y for s"http://www.blub.com"
    using z for i"http://www.blabla.com"
    import "http://blablub.com" as a
    
    x:x($x), y:y($y), z:z($z), a:a($a), [x:x]($x), [y:y]($y), [z:z]($z), [a:a]($a)
    ''',
    '''
    %base <http://www.semagia.com/>
    %prefix ident <http://www.semagia.com/x>
    ''',
    '''
    %import a <http://www.semagia.com/>
    import "http://blablub.com" as b
    ''',
    '''
    %prefix xsd <http://www.w3.org/2001/XMLSchema#>
    
    literal($o, 123), 
    literal($v, <http://www.semagia.com>), 
    literal($o2, 12.34), 
    literal($n, "foo"),
    literal($o3, "foo", xsd:int)?
    ''',
    '''
    %version 1.2
    %prefix xsd <http://www.w3.org/2001/XMLSchema#>
    
    literal($o, 123), 
    literal($v, <http://www.semagia.com>), 
    literal($o2, 12.34), 
    literal($n, "foo"),
    literal($o3, "foo", xsd:int)?
    ''',
    '''
    %prefix xsd <http://www.w3.org/2001/XMLSchema#>
    
    value($o, 123), 
    value($v, <http://www.semagia.com>), 
    value($o2, 12.34), 
    value($n, "foo"),
    value($o3, "foo"^^xsd:int)?
    ''',
    '''
    load <http://www.semagia.com/tolog-xml>
    ''',
    '''
    load <http://www.semagia.com/tolog-xml> into <http://www.semagia.com/foo>
    ''',
    '''
    load <http://www.semagia.com/tolog-xml> into <http://www.semagia.com/foo>, <http://www.semagia.com/bar> 
    ''',
    '''
    drop <http://www.semagia.com/tolog-xml> 
    ''',
    '''
    create <http://www.semagia.com/tolog-xml> 
    ''',
    '''
    select $x using <http://www.semagia.com/> from nonsense($x)?
    ''',
    '''
    select $x using <http://www.semagia.com/> where nonsense($x)?
    '''
    )

if __name__ == '__main__':
    import nose
    nose.core.runmodule()

