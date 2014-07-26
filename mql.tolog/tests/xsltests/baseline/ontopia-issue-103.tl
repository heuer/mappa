%prefix nrk <nrk:>
%prefix ont <http://psi.ontopia.net/#>
%prefix tech <http://www.techquila.com/psi/thesaurus/#>

descendant-of($ANCESTOR, $DESCENDANT) :-
    { tech:broader-narrower(tech:broader: $ANCESTOR, tech:narrower: $DESCENDANT) /* costs: 8 */ | tech:broader-narrower(tech:broader: $ANCESTOR, tech:narrower: $MID),  /* costs: 8 */
    descendant-of($MID, $DESCENDANT) /* costs: 101 */ }
.

has-subject($CLIP, $TOPIC) :-
    { { nrk:omhandler(nrk:verk: $CLIP, nrk:tema: $TOPIC) /* costs: 8 */ | nrk:tilhoerer-emne(nrk:klassifisering: $TOPIC, nrk:klassifisert: $PERSON),  /* costs: 8 */
    nrk:omhandler(nrk:verk: $CLIP, nrk:tema: $PERSON) /* costs: 8 */ } | { nrk:omhandler(nrk:verk: $CLIP, nrk:tema: $DESCENDANT) /* costs: 8 */ | nrk:tilhoerer-emne(nrk:klassifisering: $DESCENDANT, nrk:klassifisert: $PERSON),  /* costs: 8 */
    nrk:omhandler(nrk:verk: $CLIP, nrk:tema: $PERSON) /* costs: 8 */ }, 
    descendant-of($TOPIC, $DESCENDANT) /* costs: 101 */ }, 
    instance-of($TOPIC, nrk:emne) /* costs: 100 */
.

select
    $TOPLEVELTOPIC
where
    not(tech:broader-narrower(tech:broader: $PARENT, tech:narrower: $TOPLEVELTOPIC) /* costs: 8 */), 
    direct-instance-of($TOPLEVELTOPIC, nrk:emne),  /* costs: 100 */
    instance-of($CLIP, nrk:klipp),  /* costs: 100 */
    has-subject($CLIP, $TOPLEVELTOPIC),  /* costs: 101 */
    $TOPLEVELTOPIC /= <http://bogus.ontopia.net/nrk/emne/ukategoriserbart>,  /* costs: 10000 */
    $TOPLEVELTOPIC /= <http://bogus.ontopia.net/nrk/emne/nytt-emne> /* costs: 10000 */
order by $TOPLEVELTOPIC
limit 8
