SELECT * from t
where nazwa='Maciej Kaszkowiak'
order by kategoria desc, CAST(wynik AS INT) desc;