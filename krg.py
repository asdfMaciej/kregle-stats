import csv
import matplotlib.pyplot as plt


class Zawodnik:
	def __init__(self, n, k, p, z, x, w, gender, age, kreg):
		self.n = n
		self.k = k
		self.p = p
		self.z = z
		self.x = x
		self.w = int(w)  # sorting purposes
		self.gender = gender
		self.age = age
		self.kreg = kreg

		self.cleanup()

	def cleanup(self):
		# this is unclean but so was the database - and i think thats a fair trade
		self.k = self.k.replace('"', '').lower()
		if (self.k == 'dziewiątka-amica wronki'): self.k = 'kk dziewiątka-amica wronki'
		if (
			self.k == 'osir tarnowo podgórne' or self.k == 'osir vector tarnowo pod.'
			or 'osir-vector' in self.k or self.k == 'ks osir vector tarnowo pod.'  # :VVVVVV
		): self.k = 'osir vector tarnowo podgórne'
		if self.k == 'wrzos sieraków': self.k = 'kk wrzos sieraków'
		if self.k == 'pilica tomaszów mazowiecki': self.k = 'ks pilica tomaszów mazowiecki'
		if self.k == 'oksit gmina puck': self.k = 'oksit puck'
		if self.k == 'alfa vector tarnowo podgórne': self.k = 'ks alfa-vector tarnowo podgórne'
		if self.k == 'ks pilica tomaszów maz.': self.k = 'ks pilica tomaszów mazowiecki'
		if self.n == 'Jan Klemeński': self.n = 'Jan Klemenski'
		self.n = ' '.join(self.n.split())  # removes double spaces
		if (len(self.n.split()) > 2):
			self.n = self.n[0] + " " + self.n[-1]  # who the hell adds middle names?

	def __str__(self):
		t = (self.n + " ("+self.k+") --- ")
		t += str(self.w)+" - "
		t += "p:"+self.p + " z:"+self.z + " x: "+self.x
		return t

	def _csv(self, header=False):
		if header:
			return [
				'Imię/nazwisko', 'Klub', 'Płeć', 'Kategoria wiekowa',
				'Pełne', 'Zbierane', 'Dziury', 'Wynik', 'Kręgielnia'
			]
		else:
			return [
				self.n, self.k, self.gender, self.age, self.p,
				self.z, self.x, str(self.w), self.kreg
			]

	def p_do_z(self):
		try:
			mn = float(int(self.p)/int(self.z))
		except ZeroDivisionError:
			return -1
		return mn


def open_csv(filename, kreg, nn, nk, np, nz, nx, nw, gender, age, final=[], flip=False):
	zawodnicy = []
	with open(filename, 'rt', encoding="utf8") as elob:
		reader = csv.reader(elob, delimiter=',', quotechar='|')
		for row in reader:
			nzw = ""
			if isinstance(nn, tuple) or isinstance(nn, list): 
				for item in nn:
					nzw += row[item]+" "
			else:
				try:
					nzw = row[nn]
					if flip:
						nzw = ' '.join(nzw.split(' ')[::-1])
				except:
					continue
			nzw = nzw.strip()
			try:
				if (nzw) and (row[nk].lower() != "klub") and (row[np].isdigit()):
					zawodnicy.append(Zawodnik(nzw, row[nk], row[np], row[nz], row[nx], row[nw], gender, age, kreg))
			except:
				print("[l 84]ERR: "+' '.join(row))
				continue
			if (nzw) and final and (row[nk].lower() != "klub") and (row[np].isdigit()):  # n pelnych, n zbieranych, n dziur, n wyniku
				if row[final[0]] and row[final[3]]:
					zawodnicy.append(Zawodnik(
						nzw, row[nk], row[final[0]], row[final[1]], row[final[2]], row[final[3]],
						gender, age, kreg
					))

	return zawodnicy

zawodnicy = []
#zawodnicy.append(Zawodnik("perfekcyjny zawodnik", "kk bogowie", '540', '540', '0', '1080', 'test', 'test'))
zawodnicy += open_csv('tom j m.csv', 'Tomaszów', 4, 7, 26, 27, 28, 29, 'M', 'Juniorzy młodsi', final=(46, 47, 48, 49), flip=True)
zawodnicy += open_csv('tom j f.csv', 'Tomaszów', 4, 7, 26, 27, 28, 29, 'F', 'Juniorki młodsze', final=(46, 47, 48, 49), flip=True)
zawodnicy += open_csv('mm j m.csv', 'Leszno', (2, 1), 3, 4, 5, 6, 7, 'M', 'Juniorzy młodsi', final=(8, 9, 10, 11))
zawodnicy += open_csv('mm j f.csv', 'Leszno', (2, 1), 3, 4, 5, 6, 7, 'F', 'Juniorki młodsze', final=(8, 9, 10, 11))
zawodnicy += open_csv('5 rzmslo mez.csv', 'Wronki', (2, 1), 3, 4, 5, 6, 7, 'M', 'Mężczyźni', final=(8, 9, 10, 11))
zawodnicy += open_csv('5 rzmslo kob.csv', 'Wronki', (2, 1), 3, 4, 5, 6, 7, 'F', 'Kobiety', final=(8, 9, 10, 11))
zawodnicy += open_csv('star sr j m.csv', 'Sieraków', (2, 1), 3, 4, 5, 6, 7, 'M', 'Juniorzy młodsi', final=(8, 9, 10, 11))
zawodnicy += open_csv('star sr j f.csv', 'Sieraków', (2, 1), 3, 4, 5, 6, 7, 'F', 'Juniorki młodsze', final=(8, 9, 10, 11))
zawodnicy += open_csv('sw j m.csv', 'Tarnowo', 1, 2, 3, 4, 5, 6, 'M', 'Juniorzy młodsi', final=(7, 8, 9, 10))
zawodnicy += open_csv('sw j f.csv', 'Tarnowo', 1, 2, 3, 4, 5, 6, 'F', 'Juniorki młodsze', final=(7, 8, 9, 10))
zawodnicy += open_csv('sw ml m.csv', 'Tarnowo', 1, 2, 3, 4, 5, 6, 'M', 'Młodzicy', final=(7, 8, 9, 10))
zawodnicy += open_csv('sw ml f.csv', 'Tarnowo', 1, 2, 3, 4, 5, 6, 'F', 'Młodziczki', final=(7, 8, 9, 10))
zawodnicy += open_csv('puchar j m.csv', 'Wronki', (2, 1), 3, 4, 5, 6, 7, 'M', 'Juniorzy młodsi', final=(8, 9, 10, 11))
zawodnicy += open_csv('puchar j f.csv', 'Wronki', (2, 1), 3, 4, 5, 6, 7, 'F', 'Juniorki młodsze', final=(8, 9, 10, 11))
zawodnicy += open_csv('puchar ml m.csv', 'Wronki', (2, 1), 3, 4, 5, 6, 7, 'M', 'Młodzicy', final=(8, 9, 10, 11))
zawodnicy += open_csv('puchar ml f.csv', 'Wronki', (2, 1), 3, 4, 5, 6, 7, 'F', 'Młodziczki', final=(8, 9, 10, 11))
zawodnicy += open_csv('mp16 ml m.csv', 'Tuchola', 1, 2, 19, 20, 21, 22, 'M', 'Młodzicy', final=(39, 40, 41, 42), flip=True)
zawodnicy += open_csv('mp16 ml f.csv', 'Tuchola', 1, 2, 19, 20, 21, 22, 'F', 'Młodziczki', final=(39, 40, 41, 42), flip=True)
zawodnicy += open_csv('pw14 j m.csv', 'Wronki', (2, 1), 3, 4, 5, 6, 7, 'M', 'Juniorzy młodsi', final=(8, 9, 10, 11))
zawodnicy += open_csv('pw14 j f.csv', 'Wronki', (2, 1), 3, 4, 5, 6, 7, 'F', 'Juniorki młodsze', final=(8, 9, 10, 11))
zawodnicy += open_csv('pw14 ml m.csv', 'Wronki', (2, 1), 3, 4, 5, 6, 7, 'M', 'Młodzicy', final=(8, 9, 10, 11))
zawodnicy += open_csv('pw14 ml f.csv', 'Wronki', (2, 1), 3, 4, 5, 6, 7, 'F', 'Młodziczki', final=(8, 9, 10, 11))
zawodnicy += open_csv('pw15 j m.csv', 'Wronki', (2, 1), 3, 4, 5, 6, 7, 'M', 'Juniorzy młodsi', final=(8, 9, 10, 11))
zawodnicy += open_csv('pw15 j f.csv', 'Wronki', (2, 1), 3, 4, 5, 6, 7, 'F', 'Juniorki młodsze', final=(8, 9, 10, 11))
zawodnicy += open_csv('pw15 ml m.csv', 'Wronki', (2, 1), 3, 4, 5, 6, 7, 'M', 'Młodzicy', final=(8, 9, 10, 11))
zawodnicy += open_csv('pw15 ml f.csv', 'Wronki', (2, 1), 3, 4, 5, 6, 7, 'F', 'Młodziczki', final=(8, 9, 10, 11))
zawodnicy += open_csv('pw16 j m.csv', 'Wronki', (2, 1), 3, 4, 5, 6, 7, 'M', 'Juniorzy młodsi', final=(8, 9, 10, 11))
zawodnicy += open_csv('pw16 j f.csv', 'Wronki', (2, 1), 3, 4, 5, 6, 7, 'F', 'Juniorki młodsze', final=(8, 9, 10, 11))
zawodnicy += open_csv('pw16 ml m.csv', 'Wronki', (2, 1), 3, 4, 5, 6, 7, 'M', 'Młodzicy', final=(8, 9, 10, 11))
zawodnicy += open_csv('pw16 ml f.csv', 'Wronki', (2, 1), 3, 4, 5, 6, 7, 'F', 'Młodziczki', final=(8, 9, 10, 11))
zawodnicy += open_csv('gostyn mez.csv', 'Gostyń', 1, 2, 3, 4, 5, 6, 'M', 'Mężczyźni', final=(7, 8, 9, 10), flip=True)
zawodnicy += open_csv('gostyn kob.csv', 'Gostyń', 1, 2, 3, 4, 5, 6, 'F', 'Kobiety', final=(7, 8, 9, 10), flip=True)
zawodnicy += open_csv('mpmlles ml m.csv', 'Leszno', 1, 2, 3, 4, 5, 6, 'M', 'Młodzicy', final=(16, 17, 18, 19), flip=True)
zawodnicy += open_csv('mpmlles ml f.csv', 'Leszno', 1, 2, 3, 4, 5, 6, 'F', 'Młodziczki', final=(16, 17, 18, 19), flip=True)
zawodnicy += open_csv('mp16gost j m.csv', 'Gostyń', 4, 7, 26, 27, 28, 29, 'M', 'Juniorzy młodsi', final=(46, 47, 48, 49), flip=True)
zawodnicy += open_csv('mp16gost j f.csv', 'Gostyń', 4, 7, 26, 27, 28, 29, 'F', 'Juniorki młodsze', final=(46, 47, 48, 49), flip=True)
zawodnicy += open_csv('mmmtarn ml m.csv', 'Tarnowo', 4, 5, 9, 10, 11, 12, 'M', 'Młodzicy', final=(13, 14, 15, 16), flip=True)
zawodnicy += open_csv('mmmtarn ml f.csv', 'Tarnowo', 4, 5, 9, 10, 11, 12, 'F', 'Młodziczki', final=(13, 14, 15, 16), flip=True)
zawodnicy += open_csv('swgost13 ml m.csv', 'Gostyń', 1, 2, 3, 4, 5, 6, 'M', 'Młodzicy', final=(7, 8, 9, 10), flip=True)
zawodnicy += open_csv('swgost13 ml f.csv', 'Gostyń', 1, 2, 3, 4, 5, 6, 'F', 'Młodziczki', final=(7, 8, 9, 10), flip=True)
zawodnicy += open_csv('swro15 j m.csv', 'Wronki', 1, 2, 3, 4, 5, 6, 'M', 'Młodzicy', final=(7, 8, 9, 10), flip=True)
zawodnicy += open_csv('swro15 j f.csv', 'Wronki', 1, 2, 3, 4, 5, 6, 'F', 'Młodziczki', final=(7, 8, 9, 10), flip=True)
zawodnicy += open_csv('swro15 ml m.csv', 'Wronki', 1, 2, 3, 4, 5, 6, 'M', 'Juniorzy młodsi', final=(7, 8, 9, 10), flip=True)
zawodnicy += open_csv('swro15 ml f.csv', 'Wronki', 1, 2, 3, 4, 5, 6, 'F', 'Juniorki młodsze', final=(7, 8, 9, 10), flip=True)
zawodnicy += open_csv('lsz16 j m.csv', 'Leszno', (2, 1), 3, 4, 5, 6, 7, 'M', 'Juniorzy młodsi', final=(8, 9, 10, 11))
zawodnicy += open_csv('lsz16 j f.csv', 'Leszno', (2, 1), 3, 4, 5, 6, 7, 'F', 'Juniorki młodsze', final=(8, 9, 10, 11))
zawodnicy += open_csv('lsz16 ml m.csv', 'Leszno', (2, 1), 3, 4, 5, 6, 7, 'M', 'Młodzicy', final=(8, 9, 10, 11))
zawodnicy += open_csv('lsz16 ml f.csv', 'Leszno', (2, 1), 3, 4, 5, 6, 7, 'F', 'Młodziczki', final=(8, 9, 10, 11))
zawodnicy += open_csv('tch15 j m.csv', 'Tuchola', 1, 2, 3, 4, 5, 6, 'M', 'Młodzicy', final=(7, 8, 9, 10))
zawodnicy += open_csv('tch15 j f.csv', 'Tuchola', 1, 2, 3, 4, 5, 6, 'F', 'Młodziczki', final=(7, 8, 9, 10))
zawodnicy += open_csv('tch15 ml m.csv', 'Tuchola', 1, 2, 3, 4, 5, 6, 'M', 'Juniorzy młodsi', final=(7, 8, 9, 10))
zawodnicy += open_csv('tch15 ml f.csv', 'Tuchola', 1, 2, 3, 4, 5, 6, 'F', 'Juniorki młodsze', final=(7, 8, 9, 10))
zawodnicy += open_csv('gst15 j m.csv', 'Gostyń', (2, 1), 3, 4, 5, 6, 7, 'M', 'Młodzicy')
zawodnicy += open_csv('gst15 j f.csv', 'Gostyń', (2, 1), 4, 5, 6, 7, 8, 'F', 'Młodziczki')
zawodnicy += open_csv('gst15 ml m.csv', 'Gostyń', (2, 1), 4, 5, 6, 7, 8, 'M', 'Juniorzy młodsi')
zawodnicy += open_csv('gst15 ml f.csv', 'Gostyń', (2, 1), 4, 5, 6, 7, 8, 'F', 'Juniorki młodsze')
zawodnicy += open_csv('lsz14 j m.csv', 'Leszno', (2, 1), 3, 4, 5, 6, 7, 'M', 'Juniorzy młodsi', final=(8, 9, 10, 11))
zawodnicy += open_csv('lsz14 j f.csv', 'Leszno', (2, 1), 3, 4, 5, 6, 7, 'F', 'Juniorki młodsze', final=(8, 9, 10, 11))
zawodnicy += open_csv('lsz14 ml m.csv', 'Leszno', (2, 1), 3, 4, 5, 6, 7, 'M', 'Młodzicy', final=(8, 9, 10, 11))
zawodnicy += open_csv('lsz14 ml f.csv', 'Leszno', (2, 1), 3, 4, 5, 6, 7, 'F', 'Młodziczki', final=(8, 9, 10, 11))
zawodnicy += open_csv('pw13 j m.csv', 'Wronki', (2, 1), 3, 4, 5, 6, 7, 'M', 'Juniorzy młodsi', final=(8, 9, 10, 11))
zawodnicy += open_csv('pw13 j f.csv', 'Wronki', (2, 1), 3, 4, 5, 6, 7, 'F', 'Juniorki młodsze', final=(8, 9, 10, 11))
zawodnicy += open_csv('pw13 ml m.csv', 'Wronki', (2, 1), 3, 4, 5, 6, 7, 'M', 'Młodzicy', final=(8, 9, 10, 11))
zawodnicy += open_csv('pw13 ml f.csv', 'Wronki', (2, 1), 3, 4, 5, 6, 7, 'F', 'Młodziczki', final=(8, 9, 10, 11))
zawodnicy += open_csv('lsz15 j m.csv', 'Leszno', (2, 1), 3, 4, 5, 6, 7, 'M', 'Juniorzy młodsi', final=(8, 9, 10, 11))
zawodnicy += open_csv('lsz15 j f.csv', 'Leszno', (2, 1), 3, 4, 5, 6, 7, 'F', 'Juniorki młodsze', final=(8, 9, 10, 11))
zawodnicy += open_csv('lsz15 ml m.csv', 'Leszno', (2, 1), 3, 4, 5, 6, 7, 'M', 'Młodzicy', final=(8, 9, 10, 11))
zawodnicy += open_csv('lsz15 ml f.csv', 'Leszno', (2, 1), 3, 4, 5, 6, 7, 'F', 'Młodziczki', final=(8, 9, 10, 11))
zawodnicy += open_csv('mp15 ml m.csv', 'Leszno', 1, 2, 3, 4, 5, 6, 'M', 'Młodzicy', final=(16, 17, 18, 19), flip=True)
zawodnicy += open_csv('mp15 ml f.csv', 'Leszno', 1, 2, 3, 4, 5, 6, 'F', 'Młodziczki', final=(16, 17, 18, 19), flip=True)
zawodnicy += open_csv('swro14 j m.csv', 'Wronki', 1, 2, 3, 4, 5, 6, 'M', 'Młodzicy', final=(7, 8, 9, 10), flip=True)
zawodnicy += open_csv('swro14 j f.csv', 'Wronki', 1, 2, 3, 4, 5, 6, 'F', 'Młodziczki', final=(7, 8, 9, 10), flip=True)
zawodnicy += open_csv('swro14 ml m.csv', 'Wronki', 1, 2, 3, 4, 5, 6, 'M', 'Juniorzy młodsi', final=(7, 8, 9, 10), flip=True)
zawodnicy += open_csv('swro14 ml f.csv', 'Wronki', 1, 2, 3, 4, 5, 6, 'F', 'Juniorki młodsze', final=(7, 8, 9, 10), flip=True)
zawodnicy += open_csv('mp14 ml m.csv', 'Wronki', 1, 2, 3, 4, 5, 6, 'M', 'Młodzicy', final=(16, 17, 18, 19), flip=True)
zawodnicy += open_csv('mp14 ml f.csv', 'Wronki', 1, 2, 3, 4, 5, 6, 'F', 'Młodziczki', final=(16, 17, 18, 19), flip=True)
zawodnicy.sort(key=lambda x: x.w, reverse=True)

db_out = open('baza faza.csv', "w", encoding="utf8")
csv_write = csv.writer(db_out, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
pdoz = []
wynik = []
for z in zawodnicy:
	x = z.p_do_z()
	if x == -1: continue
	csv_write.writerow(list(z._csv()))
	if (int(z.w) > 420):
		pdoz.append(x)
		wynik.append(z.w)

plt.plot(wynik, pdoz)
plt.show()
