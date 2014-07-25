select
    $A, count($B)
where
    composed-by(composer: $A, opera: $B)
