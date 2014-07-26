select
    $t, $n
where
    topic-name($t, $n), 
    scope($n, theme)  /* name-scope */ 
