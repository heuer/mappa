select
    $o
where
    occurrence($t, $o), 
    themes($o, theme-1, theme-2)
