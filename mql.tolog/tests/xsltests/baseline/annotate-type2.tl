select
    $T, $A
where
    occurrence($T, $A), 
    topic-name($T, $A), 
    type($A, foo)  /* occurrence- and name-type */ 
