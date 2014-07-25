select
    $A
where
    association($A), 
    scope($A, theme)  /* association-scope */ 
