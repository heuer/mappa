select
    $r
where
    item-identifier($r, <http://www.example.org>)  /* role-item-identifier */ , 
    association-role($a, $r)
