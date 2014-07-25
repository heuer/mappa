select
    $T, $N
where
    topic-name($T, $N), 
    value($N, "foo")  /* name-value */ 
