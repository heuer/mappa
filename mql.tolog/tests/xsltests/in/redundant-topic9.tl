select $TOPIC, $OCC from
  topic($TOPIC),
  not(topic-name($TOPIC, $NAME)),
  occurrence($TOPIC, $OCC)?

