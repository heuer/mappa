select
    $type
where
    :direct-types($type)  /* optimizer */
