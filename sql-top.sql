SELECT * from t
where kategoria='Młodzicy'
order by CAST(wynik AS INT) desc
limit 3;