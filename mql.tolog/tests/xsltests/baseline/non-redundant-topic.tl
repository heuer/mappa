select
    $TOPIC
where
    topic($TOPIC), 
    not(topic-name($TOPIC, $NAME))
