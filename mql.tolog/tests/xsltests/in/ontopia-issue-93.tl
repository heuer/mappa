  using ph      for i"http://psi.garshol.priv.no/tmphoto/"
  using op      for i"http://psi.ontopedia.net/"
  import "http://psi.ontopia.net/tolog/string/" as str

  year($DATE, $YEAR) :-
    str:substring($YEAR, $DATE, 0, 4).

  select $EVENT, $SDATE, $EDATE, $YEAR, count($PHOTO) from
    instance-of($EVENT, op:Event),
      not(ph:hide($EVENT : ph:hidden)),
    { ph:start-date($EVENT, $SDATE) },
    { ph:end-date($EVENT, $EDATE) },
    { year($SDATE, $YEAR) | not(year($SDATE, $YEAR)) },
    ph:taken-during($PHOTO : op:Image, $EVENT : op:Event)
  order by $YEAR desc, $SDATE desc?
