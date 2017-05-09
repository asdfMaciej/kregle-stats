import csv
import matplotlib.pyplot as plt
from scipy.interpolate import interp1d
import numpy as np
from statistics import mean
from pprint import pprint
import operator


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
		self.k = self.k.strip()
		if (self.k == 'dziewiątka-amica wronki'): self.k = 'kk dziewiątka-amica wronki'
		if (
			self.k == 'osir tarnowo podgórne' or self.k == 'osir vector tarnowo pod.'
			or 'osir-vector' in self.k or self.k == 'ks osir vector tarnowo pod.'  # :VVVVVV
		): self.k = 'osir vector tarnowo podgórne'
		if self.k == 'wrzos sieraków': self.k = 'kk wrzos sieraków'
		if self.k == 'pilica tomaszów mazowiecki': self.k = 'ks pilica tomaszów mazowiecki'
		if self.k == 'oksit gmina puck': self.k = 'oksit puck'
		if self.k in ('ks alfa vector tarnowo podgórne', 'alfa vector tarnowo podgórne', 'ks alfa vector tarnowo podg.', 'alfa-vector tarnowo podgórne'): self.k = 'ks alfa-vector tarnowo podgórne'
		if self.k == 'ks pilica tomaszów maz.': self.k = 'ks pilica tomaszów mazowiecki'
		if self.k == 'sokół brzesko': self.k = 'tkkf sokół brzesko'
		if self.k in ('kk dziewiatka-amica wronki', 'kk dziewiątka amica wronki', 'kk dziewiątka wronki',
			'kk dziewiątka- amica wronki'): self.k = 'kk dziewiątka-amica wronki'
		if self.k == 'polonia 1912 leszno': self.k = 'ks polonia 1912 leszno'
		if self.k == 'polonia łaziska górne': self.k = 'ks polonia łaziska górne'
		if self.k == 'start gostyń': self.k = 'ks start gostyń'
		if self.k == 'tpt wejherowo': self.k = 'tpk wejherowo'
		if self.k == 'zatoka puck': self.k = 'ks zatoka puck'
		if self.k == 'ks czarna kula poznan': self.k = 'ks czarna kula poznań'
		if self.k == 'tucholanka tuchola': self.k = 'mlks tucholanka tuchola'
		if self.k == 'uks 1 świebodzice': self.k = 'uks jedynka świebodzice'
		if self.k == 'osir vector tarnowo podgóne': self.k = 'osir vector tarnowo podgórne'  # ...
		if self.k == 'ks osir vector tarnowo podgórne': self.k = 'osir vector tarnowo podgórne'
		if self.k == 'czarna kula poznań': self.k = 'ks czarna kula poznań'
		if self.k == 'ks polinia 1912 leszno': self.k = 'ks polonia 1912 leszno'
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

def import_local():
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
	zawodnicy += open_csv('swro15 j m.csv', 'Wronki', 1, 2, 3, 4, 5, 6, 'M', 'Juniorzy młodsi', final=(7, 8, 9, 10), flip=True)
	zawodnicy += open_csv('swro15 j f.csv', 'Wronki', 1, 2, 3, 4, 5, 6, 'F', 'Juniorki młodsze', final=(7, 8, 9, 10), flip=True)
	zawodnicy += open_csv('swro15 ml m.csv', 'Wronki', 1, 2, 3, 4, 5, 6, 'M', 'Młodzicy', final=(7, 8, 9, 10), flip=True)
	zawodnicy += open_csv('swro15 ml f.csv', 'Wronki', 1, 2, 3, 4, 5, 6, 'F', 'Młodziczki', final=(7, 8, 9, 10), flip=True)
	zawodnicy += open_csv('lsz16 j m.csv', 'Leszno', (2, 1), 3, 4, 5, 6, 7, 'M', 'Juniorzy młodsi', final=(8, 9, 10, 11))
	zawodnicy += open_csv('lsz16 j f.csv', 'Leszno', (2, 1), 3, 4, 5, 6, 7, 'F', 'Juniorki młodsze', final=(8, 9, 10, 11))
	zawodnicy += open_csv('lsz16 ml m.csv', 'Leszno', (2, 1), 3, 4, 5, 6, 7, 'M', 'Młodzicy', final=(8, 9, 10, 11))
	zawodnicy += open_csv('lsz16 ml f.csv', 'Leszno', (2, 1), 3, 4, 5, 6, 7, 'F', 'Młodziczki', final=(8, 9, 10, 11))
	zawodnicy += open_csv('tch15 j m.csv', 'Tuchola', 1, 2, 3, 4, 5, 6, 'M', 'Juniorzy młodsi', final=(7, 8, 9, 10))
	zawodnicy += open_csv('tch15 j f.csv', 'Tuchola', 1, 2, 3, 4, 5, 6, 'F', 'Juniorki młodsze', final=(7, 8, 9, 10))
	zawodnicy += open_csv('tch15 ml m.csv', 'Tuchola', 1, 2, 3, 4, 5, 6, 'M', 'Młodzicy', final=(7, 8, 9, 10))
	zawodnicy += open_csv('tch15 ml f.csv', 'Tuchola', 1, 2, 3, 4, 5, 6, 'F', 'Młodziczki', final=(7, 8, 9, 10))
	zawodnicy += open_csv('gst15 j m.csv', 'Gostyń', (2, 1), 3, 4, 5, 6, 7, 'M', 'Juniorzy młodsi')
	zawodnicy += open_csv('gst15 j f.csv', 'Gostyń', (2, 1), 3, 5, 6, 7, 8, 'F', 'Juniorki młodsze')
	zawodnicy += open_csv('gst15 ml m.csv', 'Gostyń', (2, 1), 3, 5, 6, 7, 8, 'M', 'Młodzicy')
	zawodnicy += open_csv('gst15 ml f.csv', 'Gostyń', (2, 1), 3, 5, 6, 7, 8, 'F', 'Młodziczki')
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
	zawodnicy += open_csv('swro14 j m.csv', 'Wronki', 1, 2, 3, 4, 5, 6, 'M', 'Juniorzy młodsi', final=(7, 8, 9, 10), flip=True)
	zawodnicy += open_csv('swro14 j f.csv', 'Wronki', 1, 2, 3, 4, 5, 6, 'F', 'Juniorki młodsze', final=(7, 8, 9, 10), flip=True)
	zawodnicy += open_csv('swro14 ml m.csv', 'Wronki', 1, 2, 3, 4, 5, 6, 'M', 'Młodzicy', final=(7, 8, 9, 10), flip=True)
	zawodnicy += open_csv('swro14 ml f.csv', 'Wronki', 1, 2, 3, 4, 5, 6, 'F', 'Młodziczki', final=(7, 8, 9, 10), flip=True)
	zawodnicy += open_csv('mp14 ml m.csv', 'Wronki', 1, 2, 3, 4, 5, 6, 'M', 'Młodzicy', final=(16, 17, 18, 19), flip=True)
	zawodnicy += open_csv('mp14 ml f.csv', 'Wronki', 1, 2, 3, 4, 5, 6, 'F', 'Młodziczki', final=(16, 17, 18, 19), flip=True)
	zawodnicy.sort(key=lambda x: x.w, reverse=True)

	return zawodnicy

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


zawodnicy = import_local()
db_out = open('baza faza.csv', "w", encoding="utf8")
csv_write = csv.writer(db_out, delimiter=',', quotechar='|', quoting=csv.QUOTE_MINIMAL, lineterminator='\n')
pdoz = []
wynik = []
for z in zawodnicy:
	x = z.p_do_z()
	if x == -1: continue
	csv_write.writerow(list(z._csv()))
	pdoz.append(x)
	wynik.append(z.w)

min_wyn = min(wynik)
max_wyn = max(wynik)
nowe = list(range(min_wyn, max_wyn+1))
fajne_kobiety = [0] * len(nowe)
fajni_mezczyzni = [0] * len(nowe)


dict_krol = {
	'wszystko':[[], [], [], []],
	'Młodziczki':{'wszystko':[[], [], [], []]}, 'Młodzicy':{'wszystko':[[], [], [], []]},
	'Juniorki młodsze':{'wszystko':[[], [], [], []]}, 'Juniorzy młodsi':{'wszystko':[[], [], [], []]},
	'Mężczyźni':{'wszystko':[[], [], [], []]}, 'Kobiety':{'wszystko':[[], [], [], []]}
}
for z in zawodnicy:
	if z.w < 360: # pls
		continue
	if z.k not in dict_krol[z.age]:
		dict_krol[z.age][z.k] = [[], [], [], []]
	if z.k not in dict_krol:
		dict_krol[z.k] = {'wszystko':[[], [], [], []]}
	if z.age not in dict_krol[z.k]:
		dict_krol[z.k][z.age] = [[], [], [], []]
	if z.kreg not in dict_krol:
		dict_krol[z.kreg] = {'wszystko':[[], [], [], []]}
	if z.age not in dict_krol[z.kreg]:
		dict_krol[z.kreg][z.age] = [[], [], [], []]
	if z.kreg not in dict_krol[z.age]:
		dict_krol[z.age][z.kreg] = [[], [], [], []]

	ehh = [z.w, z.p, z.z, z.x]
	for n in range(4):
		if z.age not in ('Kobiety', 'Mężczyźni'):  # wole pominac przy analizie
			dict_krol[z.k][z.age][n].append(int(ehh[n]))
			dict_krol[z.k]['wszystko'][n].append(int(ehh[n]))
			dict_krol[z.age][z.k][n].append(int(ehh[n]))
			dict_krol[z.age]['wszystko'][n].append(int(ehh[n]))
			dict_krol[z.age][z.kreg][n].append(int(ehh[n]))
			dict_krol[z.kreg]['wszystko'][n].append(int(ehh[n]))
			dict_krol['wszystko'][n].append(int(ehh[n]))



for key, value in dict_krol.items():
	pass
	#print(key)

print('Średni wynik wszystkich z danego klubu: ')
print('')
nieudane = {}
a_wiekowe = [
	'Młodziczki', 'Młodzicy', 'Juniorzy młodsi', 'Juniorki młodsze', 'Mężczyźni', 'Kobiety',	
]
a_kregielnie = ['Wronki', 'Gostyń', 'Leszno', 'Tuchola', 'Sieraków', 'Tarnowo', 'Tomaszów']
"""for klub, itemy in dict_krol.items():
	if (klub in a_wiekowe) or (klub in a_kregielnie):
		continue
	try:
		_len = 0
		if klub == 'wszystko':
			sr_w = str(round(mean(itemy[0])))
			_len = len(itemy[0])
		else:
			sr_w = str(round(mean(itemy['wszystko'][0])))
			_len = len(itemy['wszystko'][0])
	except:
		continue
	starty = str(_len)
	if not (_len < 25):
		print(klub + " --- "+sr_w+" (n startow: "+starty+")")
	else:
		nieudane[klub] = starty"""


"""for kregielnia, itemy in dict_krol.items():
	if kregielnia not in a_kregielnie:
		continue
	for kategoria in a_wiekowe:
		if kategoria in ('Mężczyźni', 'Kobiety'):
			continue
		if kregielnia in dict_krol[kategoria]:
			print(kategoria + "," + kregielnia + "," + str(round(mean(dict_krol[kategoria][kregielnia][2]))))"""

a_zawo = {}
a_kategorie = {}
for z in zawodnicy:
	if z.age in ('Mężczyźni', 'Kobiety'):
		continue
	if z.k not in a_zawo: a_zawo[z.k] = 0
	if z.k not in a_kategorie: a_kategorie[z.k] = {}
	if z.age not in a_kategorie[z.k]: a_kategorie[z.k][z.age] = 0
	a_zawo[z.k] += 1
	a_kategorie[z.k][z.age] += 1

a_procent = {'Juniorzy młodsi':{}, 'Juniorki młodsze':{}, 'Młodzicy':{}, 'Młodziczki':{}}
for kateg in ('Juniorzy młodsi', 'Juniorki młodsze', 'Młodzicy', 'Młodziczki'):
	for klub in a_kategorie:
		a_procent[kateg][klub] = 0
		try:
			procent_juniorow =  float(a_kategorie[klub][kateg]/a_zawo[klub]*100)
			a_procent[kateg][klub] = procent_juniorow
		except:
			continue

sorted_mlm = sorted(a_procent['Młodzicy'].items(), key=operator.itemgetter(0))[::-1]
sorted_mlf = sorted(a_procent['Młodziczki'].items(), key=operator.itemgetter(0))[::-1]
sorted_jm = sorted(a_procent['Juniorzy młodsi'].items(), key=operator.itemgetter(0))[::-1]
sorted_jf = sorted(a_procent['Juniorki młodsze'].items(), key=operator.itemgetter(0))[::-1]
klb = []
a1 = []
a2 = []
a3 = []
a4 = []
cyfry = list(range(len(sorted_mlm)))
for kz in sorted_mlm:
	klb.append(kz[0].replace(' ', '\n').replace('-','\n'))  # human readiblity
	a1.append(kz[1])
for kz in sorted_mlf: a2.append(kz[1])
for kz in sorted_jm: a3.append(kz[1])
for kz in sorted_jf: a4.append(kz[1])

xD = np.array
#plt.plot(wynik, pdoz, "-")
fig, ax = plt.subplots()
#ax.bar(nowe, fajne_kobiety)
ax.bar(cyfry, a1, label='Młodzicy')
ax.bar(cyfry, a2, bottom=a1, label='Młodziczki')
ax.bar(cyfry, a3, bottom=xD(a1)+xD(a2), label='Juniorzy młodsi')
ax.bar(cyfry, a4, bottom=xD(a1)+xD(a2)+xD(a3), label='Juniorki młodsze')
plt.xticks(cyfry, klb)
plt.legend(loc='upper left')
plt.show()
