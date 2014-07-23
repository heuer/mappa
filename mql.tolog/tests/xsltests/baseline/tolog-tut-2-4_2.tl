select
    $OPERA
where
    $DATE = "1870 (22 Feb)",  /* costs: 0 */
    premiere-date($OPERA, $DATE) /* costs: 1000 */
