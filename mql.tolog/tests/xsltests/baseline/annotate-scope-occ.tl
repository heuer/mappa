select
    $t, $o
where
    occurrence($t, $o), 
    scope($o, theme)  /* occurrence-scope */ 
