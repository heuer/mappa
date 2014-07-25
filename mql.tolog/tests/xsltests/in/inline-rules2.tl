
created-by($composer, $work) :-
    composed-by($work: work, $composer: composer)
.

select $opera where created-by(puccini, $opera)?
