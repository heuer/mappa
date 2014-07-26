select
    $o
where
    item-identifier($o, <http://www.example.org>)  /* occurrence-item-identifier */ , 
    occurrence($t, $o)
