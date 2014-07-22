select
    $t
where
    topic($t), 
    item-identifier($t, <iid>)  /* topic-item-identifier */ 
