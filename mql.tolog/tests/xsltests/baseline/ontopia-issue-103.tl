%prefix nrk <nrk:>
%prefix ont <http://psi.ontopia.net/#>
%prefix tech <http://www.techquila.com/psi/thesaurus/#>

descendant-of($ANCESTOR, $DESCENDANT) :-
    { (tech:broader: $ANCESTOR, tech:narrower: $DESCENDANT) | (tech:broader: $ANCESTOR, tech:narrower: $MID), 
    descendant-of($MID, $DESCENDANT) }
.

has-subject($CLIP, $TOPIC) :-
    { { (nrk:verk: $CLIP, nrk:tema: $TOPIC) | (nrk:klassifisering: $TOPIC, nrk:klassifisert: $PERSON), 
    (nrk:verk: $CLIP, nrk:tema: $PERSON) } | { (nrk:verk: $CLIP, nrk:tema: $DESCENDANT) | (nrk:klassifisering: $DESCENDANT, nrk:klassifisert: $PERSON), 
    (nrk:verk: $CLIP, nrk:tema: $PERSON) }, 
    descendant-of($TOPIC, $DESCENDANT) }instance-of($TOPIC, nrk:emne)
.

select
    $TOPLEVELTOPIC
where
    not((tech:broader: $PARENT, tech:narrower: $TOPLEVELTOPIC)), 
    has-subject($CLIP, $TOPLEVELTOPIC), 
    direct-instance-of($TOPLEVELTOPIC, nrk:emne), 
    instance-of($CLIP, nrk:klipp), 
    $TOPLEVELTOPIC /= <http://bogus.ontopia.net/nrk/emne/
ukategoriserbart>, 
    $TOPLEVELTOPIC /= <http://bogus.ontopia.net/nrk/emne/
nytt-emne>
order by $TOPLEVELTOPIC
limit $8
