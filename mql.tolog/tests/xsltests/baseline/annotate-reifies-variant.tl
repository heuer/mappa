select
    $v
where
    variant($n, $v), 
    reifies(r, $v)  /* variant-reifies */ 
