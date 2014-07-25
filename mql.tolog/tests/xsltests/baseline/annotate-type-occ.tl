select
    $T, $O
where
    occurrence($T, $O), 
    type($O, homepage)  /* occurrence-type */ 
