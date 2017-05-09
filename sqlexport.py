import csv, sqlite3

con = sqlite3.connect("bazkrolowa.db")
cur = con.cursor()  # nazwa,klub,plec,kategoria,pelne,zbierane,dziury,wynik,kregielnia
cur.execute("CREATE TABLE t (nazwa, klub, plec, kategoria, pelne, zbierane, dziury, wynik, kregielnia);") # use your column names here

with open('baza faza.csv','r', encoding='utf8') as fin: # `with` statement available in 2.5+
    # csv.DictReader uses first line in file for column headings by default
    dr = csv.DictReader(fin) # comma is default delimiter
    to_db = [(i['nazwa'], i['klub'], i['plec'], i['kategoria'], i['pelne'], i['zbierane'], i['dziury'], i['wynik'], i['kregielnia']) for i in dr]

cur.executemany("INSERT INTO t (nazwa, klub, plec, kategoria, pelne, zbierane, dziury, wynik, kregielnia) VALUES (?, ?, ?, ?, ?, ?, ?, ?, ?);", to_db)
con.commit()
con.close()