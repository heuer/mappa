select
    $T, $A
where
    occurrence($T, $A), 
    association($A), 
    type($A, member-of)  /* association- and occurrence-type */ 
