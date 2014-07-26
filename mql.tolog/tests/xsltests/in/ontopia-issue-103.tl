using nrk for i"nrk:"
using ont   for i"http://psi.ontopia.net/#"
using tech  for i"http://www.techquila.com/psi/thesaurus/#"

descendant-of($ANCESTOR, $DESCENDANT) :-
{
  tech:broader-narrower($ANCESTOR : tech:broader, $DESCENDANT :
tech:narrower) |
  tech:broader-narrower($ANCESTOR : tech:broader, $MID : tech:narrower),
  descendant-of($MID, $DESCENDANT)
}.

has-subject($CLIP, $TOPIC) :- {
{ nrk:omhandler($CLIP : nrk:verk, $TOPIC : nrk:tema) |
nrk:tilhoerer-emne($TOPIC : nrk:klassifisering, $PERSON :
nrk:klassifisert),
nrk:omhandler($CLIP : nrk:verk, $PERSON: nrk:tema) } |
{ nrk:omhandler($CLIP : nrk:verk, $DESCENDANT : nrk:tema) |
nrk:tilhoerer-emne($DESCENDANT : nrk:klassifisering, $PERSON :
nrk:klassifisert),
nrk:omhandler($CLIP : nrk:verk, $PERSON: nrk:tema) },
descendant-of($TOPIC, $DESCENDANT)
}, instance-of($TOPIC, nrk:emne).

select $TOPLEVELTOPIC from  direct-instance-of($TOPLEVELTOPIC,nrk:emne),
not(tech:broader-narrower($PARENT : tech:broader, $TOPLEVELTOPIC :
tech:narrower)), $TOPLEVELTOPIC /= i"http://bogus.ontopia.net/nrk/emne/ukategoriserbart",  $TOPLEVELTOPIC /= i"http://bogus.ontopia.net/nrk/emne/nytt-emne",  has-subject($CLIP, $TOPLEVELTOPIC),  instance-of($CLIP,
nrk:klipp)  order by $TOPLEVELTOPIC ASC  limit 8 ?
