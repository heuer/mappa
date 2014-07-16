select $PERSON from
  occurrence($PERSON, $OCC),
  type($OCC, date-of-birth),
  value($OCC, "1973-12-25")?