%prefix bk <http://psi.bergen.kommune.no/portal/>

select
    $T
where
    $T = @T25720,  /* costs: 0 */
    (bk:vises-vindu: $T) /* costs: 9 */
