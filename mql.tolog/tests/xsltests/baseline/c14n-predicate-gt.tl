%import ex <http://psi.ontopia.net/tolog/experimental/>

select
    $OPERA, $DATE
where
    premiere-date($OPERA, $DATE), 
    $DATE > "1900"
