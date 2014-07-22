select
    $T, $O
where
    occurrence($T, $O), 
    resource($O, <foo>)  /* occurrence-resource */ 
