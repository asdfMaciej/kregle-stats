import csv, sqlite3

con = sqlite3.connect("bazkrolowa.db")
cur = con.cursor()  # nazwa,klub,plec,kategoria,pelne,zbierane,dziury,wynik,kregielnia
cur.execute("CREATE TABLE wyniki (nazwa, klub, plec, kategoria, pelne, zbierane, dziury, wynik, kregielnia, turniej, sezon, miesiac);") # use your column names here

with open('baza faza.csv','r', encoding='utf8') as fin: # `with` statement available in 2.5+
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(fin) # comma is default delimiter
    #for i in dr:
    	#print(i)
    to_db = [(i['Imię/nazwisko'], i['Klub'], i['Płeć'], i['Kategoria wiekowa'], i['Pełne'], i['Zbierane'], i['Dziury'], i['Wynik'], i['Kręgielnia'], i['Turniej'], i['Sezon'], i['Miesiąc']) for i in dr]

cur.executemany("INSERT INTO wyniki (nazwa, klub, plec, kategoria, pelne, zbierane, dziury, wynik, kregielnia, turniej, sezon, miesiac) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?);", to_db)
con.commit()
con.close()