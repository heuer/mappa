select
    $N, $V
where
    variant($N, $V), 
    resource($V, <foo>)  /* variant-resource */ 
