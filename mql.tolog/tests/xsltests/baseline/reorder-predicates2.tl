%prefix bk <http://psi.bergen.kommune.no/portal/>

select
    $T
where
    $T = @T25720, 
    (bk:vises-vindu: $T)
