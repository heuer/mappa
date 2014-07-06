select $TOPIC from
  topic($TOPIC),
  not(topic-name($TOPIC, $NAME))?
