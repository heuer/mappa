select
    $t
where
    item-identifier($t, <http://www.example.org/foo>),  /* costs: 1 */
    topic($t) /* costs: 1000 */
