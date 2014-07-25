select
    $a
where
    association($a), 
    reifies(r, $a)  /* association-reifies */ 
