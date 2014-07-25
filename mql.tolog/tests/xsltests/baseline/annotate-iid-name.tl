select
    $n
where
    item-identifier($n, <http://www.example.org>)  /* name-item-identifier */ , 
    topic-name($t, $n)
