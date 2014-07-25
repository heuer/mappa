select
    $t, $n
where
    topic-name($t, $n), 
    item-identifier($t, <iid>)  /* topic-item-identifier */ 
