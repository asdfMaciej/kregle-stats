SELECT DISTINCT nazwa from t 
WHERE klub='kk dziewiątka-amica wronki'
AND length(nazwa)>10
AND kategoria != 'Mężczyźni'
AND kategoria != 'Kobiety'
ORDER BY nazwa ASC;
