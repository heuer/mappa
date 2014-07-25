select
    $A, $R
where
    association-role($A, $R), 
    type($R, member)  /* role-type */ 
