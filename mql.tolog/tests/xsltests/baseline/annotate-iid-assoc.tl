select
    $a
where
    item-identifier($a, <http://www.example.org>)  /* association-item-identifier */ , 
    association($a)
