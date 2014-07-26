select
    $T, $O
where
    occurrence($T, $O), 
    value($O, "foo")  /* occurrence-value */ 
