select
    $N, $V
where
    variant($N, $V), 
    value($V, "foo")  /* variant-value */ 
