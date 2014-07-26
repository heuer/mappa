select
    $TOPIC, $OCC
where
    not(topic-name($TOPIC, $NAME)), 
    occurrence($TOPIC, $OCC)
