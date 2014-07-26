
composed-by($composer, $work) :- 
    composed-by($work: work, $composer: composer)
.

select $opera where composed-by(puccini, $opera)?
