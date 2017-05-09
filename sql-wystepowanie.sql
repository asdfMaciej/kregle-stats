SELECT nazwa, count(nazwa), max(cast(wynik as int))
from t
WHERE kategoria != 'Mężczyźni'
AND kategoria != 'Kobiety'
GROUP by nazwa
order by count(nazwa) desc;