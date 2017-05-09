DELETE from zawodnicy;

INSERT into zawodnicy (nazwa, zyciowka, najgorszy, klub, plec, avg_pelne, avg_zbierane, avg_wynik, ilosc)
SELECT nazwa, max(cast(wynik as int)), min(cast(wynik as int)), klub, plec, avg(pelne), avg(zbierane), avg(wynik), count(nazwa)
from t
WHERE kategoria != 'Mężczyźni'
AND kategoria != 'Kobiety'
AND cast(wynik as int) > 360
GROUP by nazwa
order by nazwa desc;

CREATE VIEW statystycznie_relevant AS
SELECT * FROM zawodnicy
WHERE ilosc>9;