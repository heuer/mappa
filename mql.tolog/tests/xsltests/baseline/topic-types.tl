select
    $type
where
    :types($type)  /* optimizer */
