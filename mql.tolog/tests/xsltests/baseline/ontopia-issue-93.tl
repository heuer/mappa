%prefix ph <http://psi.garshol.priv.no/tmphoto/>
%prefix op <http://psi.ontopedia.net/>
%import str <http://psi.ontopia.net/tolog/string/>

year($DATE, $YEAR) :-
    str:substring($YEAR, $DATE, 0, 4)
.

select
    $EVENT, $SDATE, $EDATE, $YEAR, count($PHOTO)
where
    not(ph:hide(ph:hidden: $EVENT) /* costs: 9 */), 
    { ph:start-date($EVENT, $SDATE) /* costs: 1000 */ }, 
    { ph:end-date($EVENT, $EDATE) /* costs: 1000 */ }, 
    { year($SDATE, $YEAR) /* costs: 101 */ | not(year($SDATE, $YEAR) /* costs: 101 */) }, 
    ph:taken-during(op:Image: $PHOTO, op:Event: $EVENT),  /* costs: 8 */
    instance-of($EVENT, op:Event) /* costs: 100 */
order by $YEAR desc, $SDATE desc
