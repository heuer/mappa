%prefix ph <http://psi.garshol.priv.no/tmphoto/>
%prefix op <http://psi.ontopedia.net/>
%import str <http://psi.ontopia.net/tolog/string/>

year($DATE, $YEAR) :-
    str:substring($YEAR, $DATE, 0, 4)
.

select
    $EVENT, $SDATE, $EDATE, $YEAR, count($PHOTO)
where
    not((ph:hidden: $EVENT)), 
    { ph:start-date($EVENT, $SDATE) }, 
    { ph:end-date($EVENT, $EDATE) }, 
    { year($SDATE, $YEAR) | not(year($SDATE, $YEAR)) }, 
    (op:Image: $PHOTO, op:Event: $EVENT), 
    instance-of($EVENT, op:Event)
order by $YEAR desc, $SDATE desc
