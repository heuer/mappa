select
    $A, $O
where
    topic-name($A, $O), 
    occurrence($A, $O), 
    type($O, homepage), 
    value($O, "foo")
