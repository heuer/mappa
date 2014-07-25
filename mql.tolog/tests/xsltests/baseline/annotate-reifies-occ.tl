select
    $o
where
    occurrence($t, $o), 
    reifies(r, $o)  /* occurrence-reifies */ 
