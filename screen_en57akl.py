#encoding: UTF-8

import math
from PIL import ImageDraw, ImageFont, Image
from random import random, randint
from datetime import datetime, timedelta
from time import gmtime, strftime

# definicje kolorow
czarny = (0,0,0)
blekitny=(155,249,255)
niebieski=(196,236,255)
szary=(51,51,51)
zielony=(58,202,27)
czerwony=(255,0,0)
zolty=(255,204,0)
bialy=(255,255,255)
pomaranczowy = (255,128,40)

class screen_en57akl(abstractscreenrenderer):
	def __init__(self, lookup_path):
		# wczytanie obrazka
		self.tlo = self.openimage(lookup_path + "cab/ekran")
		lookup_path = lookup_path + "screen/"
		self.podklad = Image.open(lookup_path + "podklad.png")
		self.ramki1  = Image.open(lookup_path + "ramki1.png")
		self.ramki2  = Image.open(lookup_path + "ramki2.png")
		self.ezt  = Image.open(lookup_path + "ezt.png")
		self.WN_off  = Image.open(lookup_path + "WN_off.png")
		self.WS_off  = Image.open(lookup_path + "WS_off.png")
		self.WS_gotowosc  = Image.open(lookup_path + "WS_gotowosc.png")
		self.przetwornica_off  = Image.open(lookup_path + "przetwornica_off.png")
		self.bateria_off  = Image.open(lookup_path + "bateria_off.png")
		self.falownik_off  = Image.open(lookup_path + "falownik_off.png")
		self.sprezarka_off  = Image.open(lookup_path + "sprezarka_off.png")
		self.M1M2_off  = Image.open(lookup_path + "M1M2_off.png")
		self.M3M4_off  = Image.open(lookup_path + "M3M4_off.png")
		self.WN_on  = Image.open(lookup_path + "WN_on.png")
		self.WS_on  = Image.open(lookup_path + "WS_on.png")
		self.przetwornica_on  = Image.open(lookup_path + "przetwornica_on.png")
		self.bateria_on  = Image.open(lookup_path + "bateria_on.png")
		self.falownik_on  = Image.open(lookup_path + "falownik_on.png")
		self.sprezarka_on  = Image.open(lookup_path + "sprezarka_on.png")
		self.sprezarka_idle  = Image.open(lookup_path + "sprezarka_idle.png")
		self.M1M2_on  = Image.open(lookup_path + "M1M2_on.png")
		self.M3M4_on  = Image.open(lookup_path + "M3M4_on.png")
		self.awaria_off  = Image.open(lookup_path + "awaria_off.png")
		self.awaria_on  = Image.open(lookup_path + "awaria_on.png")
		self.hamulec_off  = Image.open(lookup_path + "hamulec_off.png")
		self.hamulec_on  = Image.open(lookup_path + "hamulec_on.png")
		self.poslizg_on  = Image.open(lookup_path + "poslizg_on.png")
		self.poslizg_off  = Image.open(lookup_path + "poslizg_off.png")
		self.klima_on  = Image.open(lookup_path + "klima_on.png")
		self.klima_off  = Image.open(lookup_path + "klima_off.png")
		self.grzanie_on  = Image.open(lookup_path + "grzanie_on.png")
		self.grzanie_off  = Image.open(lookup_path + "grzanie_off.png")
		self.medcom = Image.open(lookup_path + "medcom.png")
		# wczytanie czcionki
		czcionka = "./fonts/verdana.ttf"
		self.font = ImageFont.truetype( czcionka, 20)
		self.sredni_font = ImageFont.truetype( czcionka, 17)
		self.maly_font = ImageFont.truetype( czcionka, 15)
		self.bardzo_maly_font = ImageFont.truetype( czcionka, 12)
		self.polduzy_font = ImageFont.truetype( czcionka, 27)
		self.fontv16b = ImageFont.truetype('./fonts/verdanab.ttf', 16)
		
		self.kilometry = (random()*300000)+5000
		self.last_time_update = 0
		self.dzis = datetime.now().timetuple().tm_yday
		self.rok = datetime.now().year
		self.last_hour = 10
		self.losowanie_liniahamulca = randint(0, 30)
		self.losowanie_sprawnosc_drzwi = randint(0, 45)
		self.aktyw = 0
		
	#ekran rozkładu
		baseImageName = "podklad_rj.png"
		if tableShortMode:
			baseImageName = "podklad_rj_akl.png"
			
			# ponadto zmieniamy tutaj (jednorazowo) dane tabeli dla AKL/AKM
			global tableSize
			tableSize = (776, 541)
			global tableRows
			tableRows = [0, 48, 144, 240, 624, 720, 768]
		self.baseImage = Image.open(lookup_path + baseImageName)
		# wczytanie czcionki
		self.font0 = ImageFont.truetype('./fonts/times.ttf', 12)
		self.font0b = ImageFont.truetype('./fonts/timesbd.ttf', 12)
		self.font1 = ImageFont.truetype('./fonts/times.ttf', 14)
		self.font1b = ImageFont.truetype('./fonts/timesbd.ttf', 14)
		self.font2 = ImageFont.truetype('./fonts/times.ttf', 18)
		self.font2b = ImageFont.truetype('./fonts/timesbd.ttf', 18)
		self.font3 = ImageFont.truetype('./fonts/times.ttf', 20)
		self.font3b = ImageFont.truetype('./fonts/timesbd.ttf', 20)
		self.fontv0 = ImageFont.truetype('./fonts/verdana.ttf', 14)
		self.fontv0b = ImageFont.truetype('./fonts/verdanab.ttf', 14)
		self.fontv1 = ImageFont.truetype('./fonts/verdana.ttf', 28)
		self.fontv1b = ImageFont.truetype('./fonts/verdanab.ttf', 28)
		self.fontv2 = ImageFont.truetype('./fonts/verdana.ttf', 42)
		self.fontv2b = ImageFont.truetype('./fonts/verdanab.ttf', 42)

	def _render(self, state):
	
		tlo = self.tlo.copy()
		dt=0
		if (state['battery'] + state['converter']):
			# Liczenie pojazdow
			unit_no = state['unit_no']
			car_no = state['car_no']
			if (car_no == 3) or (car_no > 6):
				pojazdy = 1
			if (unit_no == 2) and (car_no == 6):
				pojazdy = 2
			if (car_no > 6):
				pojazdy = 3
			if (car_no > 9):
				pojazdy = 4
			
			napiecie = state['eimp_c1_uhv']
			napiecie2 = state['eimp_c2_uhv']
			velocity = state['velocity']
			speed = float(velocity)
			if speed > 200:
				speed = 200
			temp = state['air_temperature']
			direction = state['direction']
			seconds = state['seconds']
			minutes = state['minutes']
			hours = state['hours']
			dir_brake = state['dir_brake']
			indir_brake = state['indir_brake']
			brakes_1_spring_active = state['brakes_1_spring_active']
			brakes_3_spring_active = state['brakes_3_spring_active']
			brakes_4_spring_active = state['brakes_4_spring_active']
			brakes_6_spring_active = state['brakes_6_spring_active']
			spring_brake = ((brakes_1_spring_active == 1) | (brakes_3_spring_active == 1))
			dir_or_indir_brake_pn = (dir_brake | indir_brake )
			dir_or_indir_brake = (dir_or_indir_brake_pn | spring_brake)
			doors_1 = state['doors_1']
			doors_2 = state['doors_2']
			doors_3 = state['doors_3']
			doors_ezt1 = (doors_1 | doors_2 | doors_3)
			doors_4 = state['doors_4']
			doors_5 = state['doors_5']
			doors_6 = state['doors_6']
			doors_ezt2 = (doors_4 | doors_5 | doors_6)
			eimp_u1_pf = state['eimp_u1_pf']
			eimp_u1_pr = state['eimp_u1_pr']
			eimp_u2_pf = state['eimp_u2_pf']
			eimp_u2_pr = state['eimp_u2_pr']
			eimp_c1_ms = state['eimp_c1_ms']
			eimp_c2_ms = state['eimp_c2_ms']
			eimp_c1_conv = state['eimp_c1_conv']
			eimp_c2_conv = state['eimp_c2_conv']
			eimp_c1_fuse = state['eimp_c1_fuse']
			ws_gotowosc = state['main_ready']
			gotowy_do_jazdy = ((doors_ezt1 == 0)&(dir_or_indir_brake == 0)&((eimp_c1_ms&eimp_c1_conv) == 1)&(eimp_c1_fuse == 0)&(direction != 0)&((state['pantpress']) > 3.5))
			blokada_drzwi = (state['door_lock'] == 0)
			linia_hamulca = (state['eimp_pn1_bc']>1.2)
			linia_hamulca_wylosowana = (self.losowanie_liniahamulca == 0)
			sprawnosc_drzwi_wylosowana = (self.losowanie_sprawnosc_drzwi == 0 and doors_1 | doors_2 | doors_3)
			sprezarka_pomocnicza = (state['pant_compressor'] == 1)
			komunikacja_can = (pojazdy > 2)

			
			# kopia obrazka na potrzeby tego jednego renderowania
			obrazek = self.podklad.copy()
			# chcemy rysowac po teksturze pulpitu
			draw = ImageDraw.Draw(obrazek)
			
			# kierunek jazdy
			if direction == 1:
				draw.polygon([(294, 87), (305, 50), (294, 53), (307, 28), (320, 53), (309, 50), (320, 87)],fill=zielony) # strzalka kierunkowa naprzod
				
			if direction == -1:
				draw.polygon([(294, 114), (305, 152), (294, 149), (307, 174), (320, 149), (309, 152), (320, 114)],fill=zielony) # strzalka kierunkowa w tyl
				
			# slupek napiecia i jego wartosc
			if napiecie < 0:
				napiecie = 0
			pos = 177 - (napiecie * 150 / 5000)-2
			draw.rectangle((485,pos,469,177), fill=zolty)
			napiecie1 = napiecie/1000
			draw.text((457, 178), '%.1f' % napiecie1, fill=zolty, font=self.maly_font)
					
			# slupek procentu siły zadanej jazdy
			sila = state['eimp_t_pdt']
			pos = 176 - (sila * 150)-2
			draw.rectangle((21,176,37,pos), fill=zolty)
			sila=sila*100
			self.print_fixed_with(draw, '%d' % sila, (8, 176), 3, self.maly_font, zolty)
			
			# napięcie NN
			self.print_fixed_with(draw, '%d' % state['eimp_c1_cv'], (710,122), 3, self.font, zolty)
			
			# prędkość
			self.print_fixed_with(draw, '%d' % speed, (710,172), 3, self.font, zolty)
			
			# czas
			if seconds != self.last_time_update:
				dt = seconds - self.last_time_update
				if dt < 0:
					dt+=60
				self.kilometry += dt*speed * 0.0002778
				self.last_time_update = seconds
			czas = str(hours) + ":" 
			if minutes<10:
				czas = czas + "0" + str(minutes) + ":"
			else:
				czas = czas + str(minutes) + ":"
			if seconds<10:
				czas = czas + "0" +str(seconds)
			else:
				czas = czas + str(seconds)
			draw.text((708,4), czas, fill=bialy, font=self.sredni_font)
			
			# data
			if self.last_hour == 23 and hours == 0:
				self.dzis = self.dzis+1 # wlasnie wybila polnoc
			self.last_hour = hours
			data = datetime(self.rok, 1, 1) + timedelta(self.dzis - 1)
			data = data.strftime("%d/%m/%Y")
			draw.text((686,30), data, fill=bialy, font=self.sredni_font)

			# seria i model
			code = (state['name'])[:12]
			
			self.print_center(draw, code, 710,514, self.font, bialy)

			# kabina a aktywna
			cab = state['cab']
			if cab == 1:
				self.print_center(draw, "Kabina A aktywna", 711,417, self.bardzo_maly_font, bialy)
			if cab == -1:
				self.print_center(draw, "Kabina B aktywna", 711,417, self.bardzo_maly_font, bialy)
			# komunikaty stanu pojazdu
			if (gotowy_do_jazdy&(velocity < 0.5 )):
				komunikat2 = 'Gotowy do jazdy' #dodać warunki na ezt 2 i 3; zielony
				komunikat2_kolor = zielony
			elif ((dir_brake)&((state['brake_op_mode_flag']) == 8)&(velocity > 0.5 )):
				komunikat2 = u'Hamowanie ED' #żólty
				komunikat2_kolor = zolty
			elif (gotowy_do_jazdy&(velocity > 0.5 )&(state['eimp_t_fdt'] == 0)):
				komunikat2 = 'Wybieg' #brak zadanej mocy, brak hamowania, jedzie; zółty
				komunikat2_kolor = zolty
			else:
				komunikat2 = ''
				komunikat2_kolor = bialy
			
			if (dir_or_indir_brake&(velocity < 0.5 )):
				komunikat = u'Blokada napędu' #zahamowany i stoi; czerwony
				komunikat_kolor = czerwony
			elif (((state['door_lock']) == 0)&(velocity > 0.5)):
				komunikat = 'Jazda awaryjna' #(door_signaling==false)&(engine_damaged==false); czerwony
				komunikat_kolor = czerwony
			elif (gotowy_do_jazdy&(velocity > 0.5 )):
				komunikat = u'Napęd sprawny' #jak "gotowy do jazdy" tylko jedzie; zielony
				komunikat_kolor = zielony
			elif (False):
				komunikat = u'Napęd nieaktywny' #brak rozrządu prawdopodobnie; czerowny
				komunikat_kolor = czerwony
			else:
				komunikat = ''
				komunikat_kolor = bialy
			self.print_center(draw, komunikat, 711,443, self.fontv16b, komunikat_kolor)
			self.print_center(draw, komunikat2, 711,477, self.fontv16b, komunikat2_kolor)
			
			if state['slip_2'] or state['slip_4']:#poslizg
				obrazek.paste(self.poslizg_on,(369,2),self.poslizg_on)
			else:
				obrazek.paste(self.poslizg_off,(369,2),self.poslizg_off)
				
			if dir_or_indir_brake:#hamulec
				obrazek.paste(self.hamulec_on,(369,67),self.hamulec_on)
			else:
				obrazek.paste(self.hamulec_off,(369,67),self.hamulec_off)
				
			if state['fuse'] or state['converter_overload'] or linia_hamulca and linia_hamulca_wylosowana or blokada_drzwi:#awaria
				obrazek.paste(self.awaria_on,(369,132),self.awaria_on)
			else:
				obrazek.paste(self.awaria_off,(369,132),self.awaria_off)
				
			if state['eimp_c1_heat']:#grzanie
				obrazek.paste(self.grzanie_on,(730,54),self.grzanie_on)
			else:
				obrazek.paste(self.grzanie_off,(730,54),self.grzanie_off)
				
			# if state['']:#klimatyzacja
				# obrazek.paste(self.klima_on,(680,54),self.klima_on)
			# else:
			obrazek.paste(self.klima_off,(680,54),self.klima_off)
				
			
			### komunikaty duze
			
			messages = [
				{"name":u"EZT1: Brak kierunku jazdy","color":zolty,"cond":direction == 0},
				{"name":u"EZT1: Niskie ciśnienie pantografów","color":czerwony,"cond":state["pantpress"] < 2.5},
				{"name":u"EZT1: Blokada napędu od pneumatyki","color":czerwony,"cond":dir_or_indir_brake_pn and velocity < 0.5},
				{"name":u"EZT2: Blokada napędu od pneumatyki","color":czerwony,"cond":pojazdy >= 2 and dir_or_indir_brake_pn and velocity < 0.5},
				#{"name":u"EZT3: Blokada napędu od pneumatyki","color":czerwony,"cond":pojazdy >= 3 and dir_or_indir_brake_pn and velocity < 0.5},
				{"name":u"EZT1: Otwarte drzwi - strona prawa","color":bialy,"cond":(((cab == 1) & (state["doors_r_1"] or state["doors_r_2"] or state["doors_r_3"])) | ((cab == -1) & (state["doors_l_1"] or state["doors_l_2"] or state["doors_l_3"])))},
				{"name":u"EZT2: Otwarte drzwi - strona prawa","color":bialy,"cond":(((cab == 1) & (state["doors_r_4"] or state["doors_r_5"] or state["doors_r_6"])) | ((cab == -1) & (state["doors_l_4"] or state["doors_l_5"] or state["doors_l_6"])))},
				#{"name":u"EZT3: Otwarte drzwi - strona prawa","color":bialy,"cond":(((cab == 1) & (state["doors_r_7"] or state["doors_r_8"] or state["doors_r_9"])) | ((cab == -1) & (state["doors_l_7"] or state["doors_l_8"] or state["doors_l_9"])))},
				{"name":u"EZT1: Otwarte drzwi - strona lewa","color":bialy,"cond":(((cab == 1) & (state["doors_l_1"] or state["doors_l_2"] or state["doors_l_3"])) | ((cab == -1) & (state["doors_r_1"] or state["doors_r_2"] or state["doors_r_3"])))},
				{"name":u"EZT2: Otwarte drzwi - strona lewa","color":bialy,"cond":(((cab == 1) & (state["doors_l_4"] or state["doors_l_5"] or state["doors_l_6"])) | ((cab == -1) & (state["doors_r_4"] or state["doors_r_5"] or state["doors_r_6"])))},
				#{"name":u"EZT3: Otwarte drzwi - strona lewa","color":bialy,"cond":(((cab == 1) & (state["doors_l_7"] or state["doors_l_8"] or state["doors_l_9"])) | ((cab == -1) & (state["doors_r_7"] or state["doors_r_8"] or state["doors_r_9"])))},
				{"name":u"EZT1: Próba szczelności","color":czerwony,"cond":state["brake_op_mode_flag"] == 1},
				{"name":u"EZT2: Próba szczelności","color":czerwony,"cond":state["brake_op_mode_flag"] == 1 and pojazdy == 2 },
				{"name":u"EZT1: Niskie ciśnienie w przewodzie zasilającym","color":czerwony,"cond":state["eimp_pn2_sp"] < 5.7},
				{"name":u"EZT2: Niskie ciśnienie w przewodzie zasilającym","color":czerwony,"cond":state["eimp_pn4_sp"] < 5.7 and pojazdy == 2 },
				{"name":u"Tempomat aktywny","color":bialy,"cond":state["scndctrl_pos"] > 0},
				{"name":u"EZT1: Przekroczona górna granica napięcia trakcji","color":czerwony,"cond":napiecie > 4500},
				{"name":u"EZT2: Przekroczona górna granica napięcia trakcji","color":czerwony,"cond":napiecie2 > 4500 and pojazdy == 2},
				{"name":u"EZT1: Niskie napięcie baterii","color":czerwony,"cond":state["eimp_c1_cv"] < 75},
				{"name":u"EZT2: Niskie napięcie baterii","color":czerwony,"cond":state["eimp_c2_cv"] < 75 and pojazdy == 2 },
				{"name":u"EZT1: Odblokuj urządzenia nadmiarowe","color":czerwony,"cond":state["eimp_c1_fuse"]},
				{"name":u"EZT2: Odblokuj urządzenia nadmiarowe","color":czerwony,"cond":state["eimp_c2_fuse"]},
				{"name":u"EZT1: Wyłącznik szybki gotowy do załączenia","color":bialy,"cond":(state['main_ready'])},
				{"name":u"EZT2: Wyłącznik szybki gotowy do załączenia","color":bialy,"cond":(state['main_ready']) and pojazdy == 2 and napiecie2 > 2000},
				{"name":u"EZT1: Załączony hamulec parkingowy na wagonie Ra","color":czerwony,"cond":brakes_1_spring_active},
				{"name":u"EZT1: Załączony hamulec parkingowy na wagonie Rb","color":czerwony,"cond":brakes_3_spring_active},
				{"name":u"EZT2: Załączony hamulec parkingowy na wagonie Ra","color":czerwony,"cond":brakes_4_spring_active and pojazdy == 2 },
				{"name":u"EZT2: Załączony hamulec parkingowy na wagonie Rb","color":czerwony,"cond":brakes_6_spring_active and pojazdy == 2 },
				{"name":u"EZT1: Przerwana pętla bezpieczeństwa","color":czerwony,"cond":blokada_drzwi},
				{"name":u"EZT2: Przerwana pętla bezpieczeństwa","color":czerwony,"cond":blokada_drzwi and pojazdy == 2 },
				{"name":u"EZT1: Błąd linii hamulca","color":czerwony,"cond":linia_hamulca and linia_hamulca_wylosowana},
				{"name":u"EZT1: Hamowanie pojazdu","color":czerwony,"cond":linia_hamulca and linia_hamulca_wylosowana},
				{"name":u"EZT1: Brak sprawności sterownika drzwi automatycznych","color":czerwony,"cond":sprawnosc_drzwi_wylosowana},
				{"name":u"EZT1: Sprężarka pantografowa pracuje","color":bialy,"cond":sprezarka_pomocnicza},
				{"name":u"EZT2: Sprężarka pantografowa pracuje","color":bialy,"cond":sprezarka_pomocnicza and pojazdy == 2},
				{"name":u"EZT3: Brak komunikacji CAN z EZT 3","color":czerwony,"cond":state['car_no']>=9},
				{"name":u"EZT2: Brak komunikacji CAN z EZT 2","color":czerwony,"cond":state['car_no']>=7},
				{"name":u"EZT1: Poślizg","color":czerwony,"cond":state['slip_2']},
				{"name":u"EZT2: Poślizg","color":czerwony,"cond":state['slip_4']}
			]
			
			global activeMessages
			
			for i in range(len(messages)):
				message = messages[i]
				messageActive = message["cond"] # czy powinno byc
				messageActived = i in activeMessages # czy jest
				if messageActive and (not messageActived): # dodawanie do listy
					activeMessages.insert(0, i) # dajemy na poczatek listy, poniewaz najnowsze komunikaty pojawiaja sie na gorze
				if (not messageActive) and messageActived: # usuwanie z listy
					activeMessages.remove(i)
			
			# i to tyle jesli chodzi o logike, teraz rysowanie
			
			for i in range(len(activeMessages)):
				messageId = activeMessages[i]
				message = messages[messageId]
				draw.text((8, 410 + (i * 25)), message["name"], font = self.fontv16b, fill = message["color"])
				if i == 3: # po 4 konczymy, wiecej sie nie zmiesci
					break
			
			### koniec komunikatow duzych
			
	 #dla jednego EZT
			if (car_no == 3) or (car_no > 6):
				obrazek.paste(self.ramki1,self.ramki1)
				
				#sila trakcyjna
				sila = state['eimp_c1_fr']
				pos = 100 - (sila * 0.5)-2
				draw.rectangle((126,100,137,pos), fill=zolty)
				draw.rectangle((139,100,150,pos), fill=zolty)
				
				#prad czlonu
				prad = state['eimp_c1_ihv']
				pos = 101 - (prad * 0.10)-2
				draw.rectangle((576,101,591,pos), fill=zolty)
				self.print_fixed_with(draw, '%d' % prad, (552,178), 4, self.maly_font, zolty)
				
	#dla jednego lub dwóch
			if (3 >= pojazdy >= 1):
			
				draw.text((1, 286), 'EZT1', fill=bialy, font=self.polduzy_font)#NR EZT
			#Pasek ikon
				if (napiecie > 2500):#Wysokie napięcie
					obrazek.paste(self.WN_on,(75,270),self.WN_on)
				else:
					obrazek.paste(self.WN_off,(75,270),self.WN_off)
				
				if state['main_ready']: #Gotowość WS
					obrazek.paste(self.WS_gotowosc,(150,270),self.WS_gotowosc)
				else:
					if eimp_c1_ms: #Wylacznik szybki
						obrazek.paste(self.WS_on,(150,270),self.WS_on)
					else:
						obrazek.paste(self.WS_off,(150,270),self.WS_off)
				
				if eimp_c1_conv:#Przetwornica
					obrazek.paste(self.przetwornica_on,(226,270),self.przetwornica_on)
				else:
					obrazek.paste(self.przetwornica_off,(226,270),self.przetwornica_off)
					
				if state['eimp_c1_batt']:#Bateria
					obrazek.paste(self.bateria_on,(302,270),self.bateria_on)
				else:
					obrazek.paste(self.bateria_off,(302,270),self.bateria_off)
					
				if eimp_c1_ms:#Falownik
					obrazek.paste(self.falownik_on,(378,270),self.falownik_on)
				else:
					obrazek.paste(self.falownik_off,(378,270),self.falownik_off)
					
				if (state['eimp_u1_comp_w'] & eimp_c1_conv): #Sprezarka
					obrazek.paste(self.sprezarka_on,(454,270),self.sprezarka_on)
				elif (state['eimp_u1_comp_a'] & eimp_c1_conv):
					obrazek.paste(self.sprezarka_idle,(454,270),self.sprezarka_idle)
				else:
					obrazek.paste(self.sprezarka_off,(454,270),self.sprezarka_off)
					
				if eimp_c1_ms:#Silniki 1&2
					obrazek.paste(self.M1M2_on,(530,270),self.M1M2_on)
				else:
					obrazek.paste(self.M1M2_off,(530,270),self.M1M2_off)
					
				if eimp_c1_ms:#Silniki 3&4
					obrazek.paste(self.M3M4_on,(606,270),self.M3M4_on)
				else:
					obrazek.paste(self.M3M4_off,(606,270),self.M3M4_off)
				
				
				#prąd silników 1,2
				im = abs(state['eimp_c1_im'])
				self.print_fixed_with(draw, '%d' % im, (696, 294), 3, self.bardzo_maly_font, zolty)
				
				#temp silników 1,2
				temp = temp + ((20 - temp) * 0.000329060 + (im * im) * 0.000007031) * dt
				self.print_fixed_with(draw, '%d' % temp, (696, 314), 3, self.bardzo_maly_font, zolty)
				
				#prąd silników 3,4
				self.print_fixed_with(draw, '%d' % im, (757, 294), 3, self.bardzo_maly_font, zolty)
				
				#temp silników 3,4
				self.print_fixed_with(draw, '%d' % temp, (757, 314), 3, self.bardzo_maly_font, zolty)
				
			#Ikona EZT
				obrazek.paste(self.ezt,(5, 218),self.ezt)
				draw.text((14,238), '1', fill=bialy, font=self.bardzo_maly_font)
				#Drzwi EZT1
				#człon a
				x=58
				if doors_ezt1: #wszystkie człony mają pokazywać razem, gdy cokolwiek otwarte
					kolor = czerwony
					dx=10
				else:
					kolor = niebieski
					dx=0
				draw.line([(x-dx,225),(x-15-dx,225),(x-15-dx,250),(x-dx,250),(x-dx,225)], fill=kolor, width=2)
				draw.line([(x-3-dx,228),(x-11-dx,228),(x-11-dx,239),(x-3-dx,239),(x-3-dx,228)], fill=kolor, width=2)
				draw.line([(x+15+dx,225),(x+dx,225),(x+dx,250),(x+15+dx,250),(x+15+dx,225)], fill=kolor, width=2)
				draw.line([(x+11+dx,228),(x+3+dx,228),(x+3+dx,239),(x+11+dx,239),(x+11+dx,228)], fill=kolor, width=2)
				#człon s
				x=136
				draw.line([(x-dx,225),(x-15-dx,225),(x-15-dx,250),(x-dx,250),(x-dx,225)], fill=kolor, width=2)
				draw.line([(x-3-dx,228),(x-11-dx,228),(x-11-dx,239),(x-3-dx,239),(x-3-dx,228)], fill=kolor, width=2)
				draw.line([(x+15+dx,225),(x+dx,225),(x+dx,250),(x+15+dx,250),(x+15+dx,225)], fill=kolor, width=2)
				draw.line([(x+11+dx,228),(x+3+dx,228),(x+3+dx,239),(x+11+dx,239),(x+11+dx,228)], fill=kolor, width=2)
				#człon b
				x=214
				draw.line([(x-dx,225),(x-15-dx,225),(x-15-dx,250),(x-dx,250),(x-dx,225)], fill=kolor, width=2)
				draw.line([(x-3-dx,228),(x-11-dx,228),(x-11-dx,239),(x-3-dx,239),(x-3-dx,228)], fill=kolor, width=2)
				draw.line([(x+15+dx,225),(x+dx,225),(x+dx,250),(x+15+dx,250),(x+15+dx,225)], fill=kolor, width=2)
				draw.line([(x+11+dx,228),(x+3+dx,228),(x+3+dx,239),(x+11+dx,239),(x+11+dx,228)], fill=kolor, width=2)
				
				#oświeltenie przedziałów
				if state['lights_compartments'] == 1:
					kolor=zolty
				else:
					kolor=szary
				draw.line([(31,222),(83,222)], fill=kolor, width=3)
				draw.line([(109,222),(163,222)], fill=kolor, width=3)
				draw.line([(187,222),(241,222)], fill=kolor, width=3)
				
				#pantografy
				if ((eimp_u1_pf & (cab == 1)) | (eimp_u1_pr & (cab == -1))): #przedni
					draw.line([(115,220),(107,213),(115,206),(122,213),(115,220)], fill=zolty, width=2)
					draw.line([(115,220),(115,206)], fill=zolty, width=2)
				else:
					draw.line([(115,220),(107,216),(115,214),(122,216),(115,220)], fill=niebieski, width=2)
					draw.line([(115,220),(115,214)], fill=niebieski, width=2)
				
				if ((eimp_u1_pf & (cab == -1)) | (eimp_u1_pr & (cab == 1))): #tylny
					draw.line([(155,220),(147,213),(155,206),(162,213),(155,220)], fill=zolty, width=2)
					draw.line([(155,220),(155,206)], fill=zolty, width=2)
				else:
					draw.line([(155,220),(147,216),(155,214),(162,216),(155,220)], fill=niebieski, width=2)
					draw.line([(155,220),(155,214)], fill=niebieski, width=2)
			
	#dla dwóch EZT
			if (pojazdy == 2):
				obrazek.paste(self.ramki2,self.ramki2)
				draw.text((1, 356), 'EZT2', fill=bialy, font=self.polduzy_font)#NR EZT
				
				#sila trakcyjna
				sila = state['eimp_c1_fr']
				pos = 100 - (sila * 0.5)-2
				draw.rectangle((117,100,129,pos), fill=zolty)
				draw.rectangle((131,100,143,pos), fill=zolty)
				sila = state['eimp_c2_fr']
				pos = 100 - (sila * 0.5)-2
				draw.rectangle((145,100,157,pos), fill=zolty)
				draw.rectangle((159,100,171,pos), fill=zolty)
				
				#prad czlonu
				prad = state['eimp_c1_ihv']
				pos = 101 - (prad * 0.10)-2
				draw.rectangle((570,101,583,pos), fill=zolty)
				prad = state['eimp_c2_ihv']
				pos = 101 - (prad * 0.10)-2
				draw.rectangle((586,101,599,pos), fill=zolty)
				
			#Pasek ikon
				if (napiecie > 2500):#Wysokie napięcie
					obrazek.paste(self.WN_on,(75,339),self.WN_on)
				else:
					obrazek.paste(self.WN_off,(75,339),self.WN_off)
									
				if state['main_ready']: #Gotowość WS
					obrazek.paste(self.WS_gotowosc,(150,339),self.WS_gotowosc)
				else:
					if eimp_c2_ms: #Wylacznik szybki
						obrazek.paste(self.WS_on,(150,339),self.WS_on)
					else:
						obrazek.paste(self.WS_off,(150,339),self.WS_off)	
				
				if eimp_c2_conv:#Przetwornica
					obrazek.paste(self.przetwornica_on,(226,339),self.przetwornica_on)
				else:
					obrazek.paste(self.przetwornica_off,(226,339),self.przetwornica_off)
					
				if state['eimp_c2_batt']:#Bateria
					obrazek.paste(self.bateria_on,(302,339),self.bateria_on)
				else:
					obrazek.paste(self.bateria_off,(302,339),self.bateria_off)
					
				if eimp_c2_ms:#Falownik
					obrazek.paste(self.falownik_on,(378,339),self.falownik_on)
				else:
					obrazek.paste(self.falownik_off,(378,339),self.falownik_off)
					
				if (state['eimp_u2_comp_w'] & eimp_c2_conv): #Sprezarka
					obrazek.paste(self.sprezarka_on,(454,339),self.sprezarka_on)
				elif (state['eimp_u2_comp_a'] & eimp_c2_conv):
					obrazek.paste(self.sprezarka_idle,(454,339),self.sprezarka_idle)
				else:
					obrazek.paste(self.sprezarka_off,(454,339),self.sprezarka_off)
					
				if eimp_c2_ms:#Silniki 1&2
					obrazek.paste(self.M1M2_on,(530,339),self.M1M2_on)
				else:
					obrazek.paste(self.M1M2_off,(530,339),self.M1M2_off)
					
				if eimp_c2_ms:#Silniki 3&4
					obrazek.paste(self.M3M4_on,(606,339),self.M3M4_on)
				else:
					obrazek.paste(self.M3M4_off,(606,339),self.M3M4_off)
				
				
				#prąd silników 1,2
				im = abs(state['eimp_c2_im'])
				self.print_fixed_with(draw, '%d' % im, (696, 364), 3, self.bardzo_maly_font, zolty)
				
				#temp silników 1,2
				temp = temp + ((20 - temp) * 0.000329060 + (im * im) * 0.000007031) * dt
				self.print_fixed_with(draw, '%d' % temp, (696, 384), 3, self.bardzo_maly_font, zolty)
				
				#prąd silników 3,4
				self.print_fixed_with(draw, '%d' % im, (757, 364), 3, self.bardzo_maly_font, zolty)
				
				#temp silników 3,4
				self.print_fixed_with(draw, '%d' % temp, (757, 384), 3, self.bardzo_maly_font, zolty)
				
			#Ikona EZT
				obrazek.paste(self.ezt,(269, 218),self.ezt)
				draw.text((278,238), '2', fill=bialy, font=self.bardzo_maly_font)
				#Drzwi EZT1
				#człon a
				x=322
				if doors_ezt2:
					kolor = czerwony
					dx=10
				else:
					kolor = niebieski
					dx=0
				draw.line([(x-dx,225),(x-15-dx,225),(x-15-dx,250),(x-dx,250),(x-dx,225)], fill=kolor, width=2)
				draw.line([(x-3-dx,228),(x-11-dx,228),(x-11-dx,239),(x-3-dx,239),(x-3-dx,228)], fill=kolor, width=2)
				draw.line([(x+15+dx,225),(x+dx,225),(x+dx,250),(x+15+dx,250),(x+15+dx,225)], fill=kolor, width=2)
				draw.line([(x+11+dx,228),(x+3+dx,228),(x+3+dx,239),(x+11+dx,239),(x+11+dx,228)], fill=kolor, width=2)
				#człon s
				x=400
				draw.line([(x-dx,225),(x-15-dx,225),(x-15-dx,250),(x-dx,250),(x-dx,225)], fill=kolor, width=2)
				draw.line([(x-3-dx,228),(x-11-dx,228),(x-11-dx,239),(x-3-dx,239),(x-3-dx,228)], fill=kolor, width=2)
				draw.line([(x+15+dx,225),(x+dx,225),(x+dx,250),(x+15+dx,250),(x+15+dx,225)], fill=kolor, width=2)
				draw.line([(x+11+dx,228),(x+3+dx,228),(x+3+dx,239),(x+11+dx,239),(x+11+dx,228)], fill=kolor, width=2)
				#człon b
				x=478
				draw.line([(x-dx,225),(x-15-dx,225),(x-15-dx,250),(x-dx,250),(x-dx,225)], fill=kolor, width=2)
				draw.line([(x-3-dx,228),(x-11-dx,228),(x-11-dx,239),(x-3-dx,239),(x-3-dx,228)], fill=kolor, width=2)
				draw.line([(x+15+dx,225),(x+dx,225),(x+dx,250),(x+15+dx,250),(x+15+dx,225)], fill=kolor, width=2)
				draw.line([(x+11+dx,228),(x+3+dx,228),(x+3+dx,239),(x+11+dx,239),(x+11+dx,228)], fill=kolor, width=2)
				
				#oświeltenie przedziałów
				x=264
				if state['lights_compartments'] == 1:
					kolor=zolty
				else:
					kolor=szary
				draw.line([(x+31,222),(x+83,222)], fill=kolor, width=3)
				draw.line([(x+109,222),(x+163,222)], fill=kolor, width=3)
				draw.line([(x+187,222),(x+241,222)], fill=kolor, width=3)
				
				#pantografy
				if ((eimp_u2_pf & (cab == 1)) | (eimp_u2_pr & (cab == -1))):
					draw.line([(x+115,220),(x+107,213),(x+115,206),(x+122,213),(x+115,220)], fill=zolty, width=2)
					draw.line([(x+115,220),(x+115,206)], fill=zolty, width=2)
				else:
					draw.line([(x+115,220),(x+107,216),(x+115,214),(x+122,216),(x+115,220)], fill=niebieski, width=2)
					draw.line([(x+115,220),(x+115,214)], fill=niebieski, width=2)
				
				if ((eimp_u2_pf & (cab == -1)) | (eimp_u2_pr & (cab == 1))):
					draw.line([(x+155,220),(x+147,213),(x+155,206),(x+162,213),(x+155,220)], fill=zolty, width=2)
					draw.line([(x+155,220),(x+155,206)], fill=zolty, width=2)
				else:
					draw.line([(x+155,220),(x+147,216),(x+155,214),(x+162,216),(x+155,220)], fill=niebieski, width=2)
					draw.line([(x+155,220),(x+155,214)], fill=niebieski, width=2)
					
			#bootowanie medcom	
			self.aktyw += dt
			if self.aktyw<10:
				obrazek.paste(self.medcom, (0,0))
				draw.rectangle((210,270,210 + 38 * self.aktyw,355), fill=pomaranczowy)
				
	#rozkład jazdy
			baseImage = self.baseImage.copy()
			# chcemy rysowac po teksturze pulpitu
			draw = ImageDraw.Draw(baseImage)
			if (state['light_level']<0.325):
				tableColor = (0,0,0)
				tableTextColor = (210, 210, 210)
			else:
				tableColor = (210, 210, 210)
				tableTextColor = (0, 0, 0)
			### dane ###
			# uwaga: wiekszosc globali zostala przeniesiona nizej, tutaj zostaja te ktore musza byc przeliczane co klatke
			global globalState
			globalState = state # state nie jest globalem, wiec musimy go skopiowac
			
			# czy rozklad jazdy istnieje
			timetableExists = not (state["trainnumber"] == "none" or state["trainnumber"] == "rozklad" or state["train_stationcount"] == 0)
			
			global tableTrainName
			if timetableExists and tableTrainName != state["trainnumber"]: # gdy nastapila zmiana rozkladu (a takze przy wczytaniu) odswiezamy dane rozkladu
				tableTrainName = state["trainnumber"]
				prepareTableData()
			
			# kalkulacja zielonej kropki
			global tableGPSIndex
			if state["train_atpassengerstop"]:
				tableGPSIndex = state["train_stationstart"]
			if tableGPSIndex < state["train_stationstart"]:
				tableGPSIndex = 0
			
			### gorny panel ###
			# godzina
			draw.text((4, 16), timeText(state["hours"], state["minutes"]), font = self.fontv1b, fill = panelTextColor)
			# numer pociagu lub czas do odjazdu lub informacja o braku rozkladu
			if tableGPSIndex > 0 and state["seconds"] % 6 < 3: # co 6 sekund na 3 sekundy
				text = ""
				timeToDeparture = int(math.ceil(journeyTime(state["hours"], state["minutes"] + (state["seconds"] / 60.0), tableData[state["train_stationstart"] - 1]["dh"], tableData[state["train_stationstart"] - 1]["dm"] + (tableData[state["train_stationstart"] - 1]["dhalf"] / 10.0))))
				if timeToDeparture > 0:
					text = u"Do odjazdu: " + str(timeToDeparture) + u" min."
				elif timeToDeparture == 0:
					text = u"Odjazd!"
				elif timeToDeparture < 0:
					text = u"Opóźnienie: " + str(-timeToDeparture) + u" min."
				draw.text(((baseImage.size[0] / 2) - (draw.textsize(text, font = self.fontv2b)[0] / 2), 8), text, font = self.fontv2b, fill = panelTextColor)
			elif timetableExists:
				# gora
				draw.text((100, 12), "Nr poc/zam:", font = self.fontv0, fill = panelTextColor)
				draw.text((100 + draw.textsize("Nr poc/zam: ", font = self.fontv0)[0], 12), trainNumber(state["trainnumber"]) + "/" + str(int(hash(state["trainnumber"]) % 200000) + 900000), font = self.fontv0b, fill = panelTextColor)
				# numer zamowionego rozkladu generowany losowo na podstawie numeru pociagu, zakres mozna zmienic
				# dol
				draw.text((100, 36), removeUnderscores(state["train_station1_name"]) + " - " + removeUnderscores(state["train_station" + str(state["train_stationcount"]) + "_name"]), font = self.fontv0b, fill = panelTextColor)
			else:
				draw.text((100, 12), u"Brak rozkładu!", font = self.fontv0b, fill = panelTextColor)
			if not (tableGPSIndex > 0 and state["seconds"] % 15 < 3):
				draw.text((600, 8), "Tryb\nGPS", font = self.fontv0, fill = panelTextColor)
			
			### tabela ###
			# robimy nowa teksture dla tabeli, zeby nie wykroczyla poza zakres i nie wyjechala na sasiednie ekrany
			tableImage = Image.new("RGB", tableSize)
			tableDraw = ImageDraw.Draw(tableImage)
			tableDraw.rectangle((0, 0, tableSize[0], tableSize[1]), fill = tableColor)
			
			if timetableExists:
				tableTotalY = 0
				for i in range(state["train_stationstart"] - 1, len(tableData)):
					tableRowData = tableData[i]
					tableRowHeight = 48
					if i == 0 or not (tableRowData["vmax"] is None):
						tableRowHeight = 72
					
					# linie poziome
					if i == 0 or not (tableRowData["id12"] is None):
						tableDraw.line([addVec(tableOffset, (tableRows[0], tableTotalY)), addVec(tableOffset, (tableRows[1], tableTotalY))], fill = tableTextColor, width = 1)
					if i == 0 or not (tableRowData["vkm"] is None):
						tableDraw.line([addVec(tableOffset, (tableRows[1], tableTotalY)), addVec(tableOffset, (tableRows[3], tableTotalY))], fill = tableTextColor, width = 1)
					tableDraw.line([addVec(tableOffset, (tableRows[3], tableTotalY)), addVec(tableOffset, (tableRows[-1], tableTotalY))], fill = tableTextColor, width = 1)
					# miejsce na nazwe rozkladu
					if i == 0:
						tableDraw.line([addVec(tableOffset, (tableRows[4] + 16, tableTotalY + (tableRowHeight * (1 / 3.0)))), addVec(tableOffset, (tableRows[6] - 16, tableTotalY + (tableRowHeight * (1 / 3.0))))], fill = tableTextColor, width = 1)
						tableDraw.line([addVec(tableOffset, (tableRows[4] + 16, tableTotalY + (tableRowHeight * (2 / 3.0)))), addVec(tableOffset, (tableRows[6] - 16, tableTotalY + (tableRowHeight * (2 / 3.0))))], fill = tableTextColor, width = 1)
					# przedzielenie czasow jazdy
					if i > 0:
						tableDraw.line([addVec(tableOffset, (tableRows[5], tableTotalY + (tableRowHeight / 2))), addVec(tableOffset, (tableRows[6], tableTotalY + (tableRowHeight / 2)))], fill = tableTextColor, width = 1)
					# przedzielenie rubryk obslugi trakcyjnej
					if not tableShortMode:
						color = tableTextColor
						if not tableRowData["trainChange"]:
							color = tableGrayTextColor
						tableDraw.line([addVec(tableOffset, (tableRows[6], tableTotalY + (tableRowHeight * (1 / 3.0)))), addVec(tableOffset, (tableRows[7], tableTotalY + (tableRowHeight * (1 / 3.0))))], fill = color, width = 1)
						tableDraw.line([addVec(tableOffset, (tableRows[6], tableTotalY + (tableRowHeight * (2 / 3.0)))), addVec(tableOffset, (tableRows[7], tableTotalY + (tableRowHeight * (2 / 3.0))))], fill = color, width = 1)
						tableDraw.line([addVec(tableOffset, (tableRows[7], tableTotalY + (tableRowHeight / 2))), addVec(tableOffset, (tableRows[9], tableTotalY + (tableRowHeight / 2)))], fill = color, width = 1)
					
					# linie pionowe
					tableDraw.line([addVec(tableOffset, (tableRows[0], tableTotalY)), addVec(tableOffset, (tableRows[0], tableTotalY + tableRowHeight))], fill = tableTextColor, width = 1)
					tableDraw.line([addVec(tableOffset, (tableRows[1], tableTotalY)), addVec(tableOffset, (tableRows[1], tableTotalY + tableRowHeight))], fill = tableTextColor, width = 1)
					tableDraw.line([addVec(tableOffset, (tableRows[2], tableTotalY)), addVec(tableOffset, (tableRows[2], tableTotalY + tableRowHeight))], fill = tableTextColor, width = 3)
					tableDraw.line([addVec(tableOffset, (tableRows[3], tableTotalY)), addVec(tableOffset, (tableRows[3], tableTotalY + tableRowHeight))], fill = tableTextColor, width = 1)
					if tableRowData["tracks"] == 1:
						tableDraw.line([addVec(tableOffset, (tableRows[4], tableTotalY)), addVec(tableOffset, (tableRows[4], tableTotalY + tableRowHeight))], fill = tableTextColor, width = 7)
					elif tableRowData["tracks"] == 2:
						tableDraw.line([addVec(tableOffset, (tableRows[4] - 2.5, tableTotalY)), addVec(tableOffset, (tableRows[4] - 2.5, tableTotalY + tableRowHeight))], fill = tableTextColor, width = 2)
						tableDraw.line([addVec(tableOffset, (tableRows[4] + 2.5, tableTotalY)), addVec(tableOffset, (tableRows[4] + 2.5, tableTotalY + tableRowHeight))], fill = tableTextColor, width = 2)
					if i == 0:
						tableDraw.line([addVec(tableOffset, (tableRows[5], tableTotalY)), addVec(tableOffset, (tableRows[5], tableTotalY + (tableRowHeight * (1 / 3.0))))], fill = tableTextColor, width = 1)
						tableDraw.line([addVec(tableOffset, (tableRows[5], tableTotalY + (tableRowHeight * (2 / 3.0)))), addVec(tableOffset, (tableRows[5], tableTotalY + tableRowHeight))], fill = tableTextColor, width = 1)
					else:
						tableDraw.line([addVec(tableOffset, (tableRows[5], tableTotalY)), addVec(tableOffset, (tableRows[5], tableTotalY + tableRowHeight))], fill = tableTextColor, width = 1)
					tableDraw.line([addVec(tableOffset, (tableRows[6], tableTotalY)), addVec(tableOffset, (tableRows[6], tableTotalY + tableRowHeight))], fill = tableTextColor, width = 1)
					color = tableTextColor
					if not tableShortMode:
						if not tableRowData["trainChange"]:
							color = tableGrayTextColor
						tableDraw.line([addVec(tableOffset, (tableRows[7], tableTotalY)), addVec(tableOffset, (tableRows[7], tableTotalY + tableRowHeight))], fill = color, width = 1)
						tableDraw.line([addVec(tableOffset, (tableRows[8], tableTotalY)), addVec(tableOffset, (tableRows[8], tableTotalY + tableRowHeight))], fill = color, width = 1)
						tableDraw.line([addVec(tableOffset, (tableRows[9], tableTotalY)), addVec(tableOffset, (tableRows[9], tableTotalY + tableRowHeight))], fill = tableTextColor, width = 1)
					
					# tekst
					# pierwsze 3 rubryki
					if not (tableRowData["id12"] is None):
						tableDraw.text(addVec(tableOffset, (((tableRows[0] + tableRows[1]) / 2) - (tableDraw.textsize(tableRowData["id12"], font = self.font1)[0] / 2), tableTotalY + 4)), tableRowData["id12"], font = self.font1, fill = tableTextColor)
					if not (tableRowData["vkm"] is None):
						tableDraw.text(addVec(tableOffset, (tableRows[1] + 4, tableTotalY + 4)), kmText(tableRowData["vkm"]), font = self.font1, fill = tableTextColor)
					if not (tableRowData["vmax"] is None):
						tableDraw.text(addVec(tableOffset, (((tableRows[2] + tableRows[3]) / 2) - (tableDraw.textsize(str(tableRowData["vmax"]), font = self.font2b)[0] / 2), tableTotalY + 2)), str(tableRowData["vmax"]), font = self.font2b, fill = tableTextColor)
					# 4 rubryka - nazwa stacji
					text = tableRowData["name"]
					if i > 0 and tableRowData["ah"] != -1:
						text += " ; ph"
					font = self.font3
					if tableRowData["station"]:
						font = self.font3b
					tableDraw.text(addVec(tableOffset, (tableRows[3] + 4, tableTotalY + 2)), text, font = font, fill = tableTextColor)
					text = kmText(tableRowData["km"])
					if not (tableRowData["id12"] is None):
						text = "0." + tableRowData["id12"] + "/" + text
					tableDraw.text(addVec(tableOffset, (tableRows[3] + 4, (tableTotalY + tableRowHeight) - 22)), text, font = self.font3, fill = tableTextColor)
					tableDraw.text(addVec(tableOffset, ((tableRows[4] - tableDraw.textsize(tableRowData["eq"], self.font3)[0]) - 8, (tableTotalY + tableRowHeight) - 22)), tableRowData["eq"], font = self.font3, fill = tableTextColor)
					# zielona kropka przy postoju
					if i + 1 == tableGPSIndex:
						tableDraw.ellipse(((tableOffset[0] + tableRows[3]) - 3, (tableOffset[1] + tableTotalY) + 7, (tableOffset[0] + tableRows[3]) + 7, (tableOffset[1] + tableTotalY) + 17), fill = (0, 0, 0))
						tableDraw.ellipse(((tableOffset[0] + tableRows[3]) - 2, (tableOffset[1] + tableTotalY) + 8, (tableOffset[0] + tableRows[3]) + 6, (tableOffset[1] + tableTotalY) + 16), fill = (0, 192, 0))
					# 5 rubryka - godziny przyjazdu i odjazdu
					font = self.font3b
					if tableRowData["ah"] == -1:
						font = self.font3
					if i == 0:
						# numer pociagu
						tableDraw.line([addVec(tableOffset, (tableRows[4] + 8, tableTotalY + 12)), addVec(tableOffset, (tableRows[5] - 8, tableTotalY + 12))], fill = tableTextColor, width = 1)
						tableDraw.text(addVec(tableOffset, (((tableRows[4] + tableRows[6]) / 2) - (tableDraw.textsize(tableTrainName, font = self.font1b)[0] / 2), (tableTotalY + (tableRowHeight / 2)) - 7)), tableTrainName, font = self.font1b, fill = tableTextColor)
					elif tableRowData["ah"] == -1:
						# przelot (kreska)
						tableDraw.line([addVec(tableOffset, ((tableRows[4] + tableRows[5]) / 2, tableTotalY + 2)), addVec(tableOffset, ((tableRows[4] + tableRows[5]) / 2, tableTotalY + 22))], fill = tableTextColor, width = 1)
					else:
						# normalny przyjazd
						tableDraw.text(addVec(tableOffset, (((tableRows[4] + tableRows[5]) / 2) - (tableDraw.textsize(timeText(tableRowData["ah"], tableRowData["am"]), font = font)[0] / 2), tableTotalY + 2)), timeText(tableRowData["ah"], tableRowData["am"]), font = font, fill = tableTextColor)
						# ulamek minuty
						if tableRowData["ahalf"] > 0:
							tableDraw.text(addVec(tableOffset, (((tableRows[4] + tableRows[5]) / 2) + (tableDraw.textsize(timeText(tableRowData["ah"], tableRowData["am"]), font = font)[0] / 2), tableTotalY - 2)), str(tableRowData["ahalf"]), font = self.font2, fill = tableTextColor)
					# odjazd
					tableDraw.text(addVec(tableOffset, (((tableRows[4] + tableRows[5]) / 2) - (tableDraw.textsize(timeText(tableRowData["dh"], tableRowData["dm"]), font = font)[0] / 2), (tableTotalY + tableRowHeight) - 22)), timeText(tableRowData["dh"], tableRowData["dm"]), font = font, fill = tableTextColor)
					# ulamek minuty
					if tableRowData["dhalf"] > 0:
						tableDraw.text(addVec(tableOffset, (((tableRows[4] + tableRows[5]) / 2) + (tableDraw.textsize(timeText(tableRowData["dh"], tableRowData["dm"]), font = font)[0] / 2), (tableTotalY + tableRowHeight) - 26)), str(tableRowData["dhalf"]), font = self.font2, fill = tableTextColor)
					# 6 rubryka - czasy jazdy
					if i > 0:
						tableDraw.text(addVec(tableOffset, (tableRows[5] + 4, tableTotalY + 6)), str(tableRowData["jtime"]), font = self.font0, fill = tableTextColor)
						tableDraw.text(addVec(tableOffset, (tableRows[5] + 4, (tableTotalY + tableRowHeight) - 18)), str(tableRowData["jtimeShort"]), font = self.font0, fill = tableTextColor)
					if not tableShortMode:
						# 7 i 8 rubryka wyszarzala gdy nie ma zmiany wzgledem poprzedniej
						color = tableTextColor
						if not tableRowData["trainChange"]:
							color = tableGrayTextColor
						# 7 rubryka - obsluga trakcyjna
						for i in range(3):
							if tableRowData["veh" + str(i + 1)] == None:
								break
							tableDraw.text(addVec(tableOffset, (((tableRows[6] + tableRows[7]) / 2) - (tableDraw.textsize(tableRowData["veh" + str(i + 1)], font = self.font1)[0] / 2), (tableTotalY + (tableRowHeight * (((i * 2) + 1) / 6.0))) - 6)), tableRowData["veh" + str(i + 1)], font = self.font1, fill = color)
						# 8 rubryka - masa, vmax, dlugosc, % masy hamowania
						tableDraw.text(addVec(tableOffset, (((tableRows[7] + tableRows[8]) / 2) - (tableDraw.textsize(str(int(tableRowData["vehweight"])), font = self.font3)[0] / 2), (tableTotalY + (tableRowHeight * (1 / 4.0))) - 12)), str(int(tableRowData["vehweight"])), font = self.font3, fill = color)
						tableDraw.text(addVec(tableOffset, (((tableRows[7] + tableRows[8]) / 2) - (tableDraw.textsize(str(int(tableRowData["vehvmax"])), font = self.font3)[0] / 2), (tableTotalY + (tableRowHeight * (3 / 4.0))) - 12)), str(int(tableRowData["vehvmax"])), font = self.font3, fill = color)
						tableDraw.text(addVec(tableOffset, (((tableRows[8] + tableRows[9]) / 2) - (tableDraw.textsize(str(int(tableRowData["vehlength"])), font = self.font3)[0] / 2), (tableTotalY + (tableRowHeight * (1 / 4.0))) - 12)), str(int(tableRowData["vehlength"])), font = self.font3, fill = color)
						tableDraw.text(addVec(tableOffset, (((tableRows[8] + tableRows[9]) / 2) - (tableDraw.textsize(str(int(tableRowData["vehbrake"])), font = self.font3)[0] / 2), (tableTotalY + (tableRowHeight * (3 / 4.0))) - 12)), str(int(tableRowData["vehbrake"])), font = self.font3, fill = color)
					
					tableTotalY += tableRowHeight
					# dalej i tak nie widzimy - optymalizacja
					if tableTotalY > tableSize[1]:
						break
				# domkniecie tabelki
				tableDraw.line([addVec(tableOffset, (tableRows[0], tableTotalY)), addVec(tableOffset, (tableRows[-1], tableTotalY))], fill = tableTextColor, width = 1)
			
			# informacja tymczasowa
			if "scenarion" in state:
				tableDraw.text((20, 80), u"Pobierz nowe exe\nz działu \"Na warsztacie\"\nJESZCZE RAZ\nw posiadanym wkradła\nsię literówka\nUNIEMOŻLIWIAJĄCA prawidłowe\ndziałanie ekranu!!!", font = self.fontv2b, fill = (255, 0, 0))
			
			baseImage.paste(tableImage, tableBackOffset)
			tlo.paste(baseImage, (0,0))
			
			tlo.paste(obrazek, (0,1440))
		else:
			self.aktyw = 0
		return tlo

# globale do komunikatow
activeMessages = []

# globale do rozkladu jazdy
globalState = {}

tableShortMode = True # true dla AKL i AKM, false dla AKS; nie zmieniamy po zaladowaniu symulatora
tableGPSIndex = 0 # numer stacji przy ktorej jest zielona kropka, numerujemy od 1, 0 oznacza nigdzie
tableSize = (717, 541)
tableBackOffset = (0, 64)
tableOffset = (5, 5)
tableColor = (210, 210, 210) # zamienic ten i ten nizej miejscami jesli chcesz tryb nocny
tableTextColor = (0, 0, 0)
tableGrayTextColor = (105, 105, 105)
panelTextColor = (210, 210, 210)
tableRows = [0, 32, 96, 176, 464, 536, 576, 624, 664, 704]
tableData = [
	# id12 - numer linii
	# vkm - kilometr dla nowej Vmax
	# vmax - nowa predkosc maksymalna
	# name - nazwa stacji
	# km - kilometr stacji
	# station - true jesli to stacja, false jesli przystanek lub posterunek odgalezny
	# eq - wyposazenie
	# tracks - liczba torow
	# ah, am, ahalf, dh, dm, dhalf -
	# pierwszy czlon: a - przyjazd, d - odjazd
	# drugi czlon: h - godzina, m - minuta, half - cyfra w indeksie gornym (0 = brak)
	# jtime - czas przejazdu
	# jtimeShort - czas skrocony przejazdu
	# trainChange - true na poczatku i na kazdej stacji gdzie zmienia sie sklad (dolaczamy, odlaczamy, zmieniamy)
	# ponizsze to od trakcyjnej
	# veh1 - pojazd 1
	# veh2 - pojazd 2
	# veh3 - pojazd 3
	# vehweight - masa
	# vehvmax - vmax
	# vehlength - dlugosc
	# vehbrake - % masy hamowania
	
	# przykladowe dane
	#{"id12":"191","vkm":19.71,"vmax":40,"name":u"Wisła Głębce","km":19.71,"station":True,"eq":"R2, H","ah":-1,"am":-1,"ahalf":0,"dh":13,"dm":43,"dhalf":0,"jtime":None,"jtimeShort":None},
	#{"id12":None,"vkm":None,"vmax":None,"name":u"Wisła Kopydło po","km":17.96,"station":False,"eq":"","ah":13,"am":46,"ahalf":5,"dh":13,"dm":47,"dhalf":0,"jtime":3.5,"jtimeShort":3},
	#{"id12":None,"vkm":None,"vmax":None,"name":u"Wisła Dziechc. po","km":16.241,"station":False,"eq":"","ah":13,"am":50,"ahalf":0,"dh":13,"dm":50,"dhalf":5,"jtime":3,"jtimeShort":2.9},
	#{"id12":None,"vkm":14,"vmax":60,"name":u"Wisła Uzdrowisko","km":14.61,"station":True,"eq":"R2, H","ah":13,"am":53,"ahalf":5,"dh":13,"dm":54,"dhalf":0,"jtime":3,"jtimeShort":2.8},
	#{"id12":None,"vkm":None,"vmax":None,"name":u"Wisła Obłaziec po","km":12.338,"station":False,"eq":"","ah":13,"am":59,"ahalf":0,"dh":13,"dm":59,"dhalf":5,"jtime":5,"jtimeShort":4.7},
	#{"id12":None,"vkm":None,"vmax":None,"name":u"Ustroń Polana m, po","km":9.662,"station":False,"eq":"R2, H","ah":14,"am":3,"ahalf":0,"dh":14,"dm":3,"dhalf":5,"jtime":3.5,"jtimeShort":3.4},
	#{"id12":None,"vkm":None,"vmax":None,"name":u"Ustroń Zdrój po","km":6.655,"station":False,"eq":"","ah":14,"am":7,"ahalf":5,"dh":14,"dm":8,"dhalf":0,"jtime":4,"jtimeShort":3.6}
]
tableTrainName = ""

# funkcje do rozkladu jazdy
def prepareTableData():
	state = globalState
	global tableData
	tableData = [] # czyscimy
	
	lastVmax = None # potrzebne nam jest to zeby co pozycje sprawdzac czy vmax sie zmienila, i jesli tak - to wprowadzic to do tabelki
	# nie mozemy tego zrobic uzyskujac dane z ostatniej kolumny, poniewaz brak zmiany oznaczony jest jako none, co spowodowaloby pojawienie sie tej samej predkosci co druga rubryke
	
	for i in range(state["train_stationcount"]):
		tableRowData = {}
		if i == 0:
			# NA POCZATEK WIELKIE SZAMYNSTWO!!! Numer linii generowany losowo!!! W dodatku z wyjatkami na nazwy niektorych scenerii!!!
			# Zakres 1-299, co prawda w rzeczywistosci jest do 999, ale powyzej 300 to juz raczej malutkie linie i lacznice
			# generowanie na podstawie 5 pierwszych znakow lacznie z dolarem, zeby sie numery linii nie roznily przy np. baltyk i baltyk_zima
			if state["scenario"][:5] == "$l053":
				tableRowData["id12"] = "53"
			elif state["scenario"][:9] == "$l61+l144":
				tableRowData["id12"] = "144"
			elif state["scenario"][:8] == "$linia61":
				tableRowData["id12"] = "61"
			else:
				tableRowData["id12"] = str(tryInt((int(hash(state["scenario"][:5])) % 299) + 1))
		else:
			tableRowData["id12"] = None
		if i == 0 or state["train_station" + str(i + 1) + "_vmax"] != lastVmax:
			tableRowData["vkm"] = state["train_station" + str(i + 1) + "_lctn"]
			tableRowData["vmax"] = int(state["train_station" + str(i + 1) + "_vmax"])
		else:
			tableRowData["vkm"] = None
			tableRowData["vmax"] = None
		lastVmax = state["train_station" + str(i + 1) + "_vmax"]
		tableRowData["name"] = removeUnderscores(state["train_station" + str(i + 1) + "_name"])
		tableRowData["km"] = state["train_station" + str(i + 1) + "_lctn"]
		tableRowData["station"] = not (tableRowData["name"][:2] == "po" or tableRowData["name"][:4] == "podg" or tableRowData["name"][-2:] == "po" or tableRowData["name"][-4:] == "podg") # wyszukac wszystkie mozliwe koncowki
		tableRowData["eq"] = state["train_station" + str(i + 1) + "_fclt"]
		tableRowData["tracks"] = state["train_station" + str(i + 1) + "_tracks"]
		tableRowData["ah"] = state["train_station" + str(i + 1) + "_ah"]
		tableRowData["am"] = int(state["train_station" + str(i + 1) + "_am"])
		tableRowData["ahalf"] = int(round((state["train_station" + str(i + 1) + "_am"] * 10) % 10))
		tableRowData["dh"] = state["train_station" + str(i + 1) + "_dh"]
		tableRowData["dm"] = int(state["train_station" + str(i + 1) + "_dm"])
		tableRowData["dhalf"] = int(round((state["train_station" + str(i + 1) + "_dm"] * 10) % 10))
		if i == 0:
			tableRowData["jtime"] = None
			tableRowData["jtimeShort"] = None
		else:
			if tableRowData["ah"] == -1:
				tableRowData["jtime"] = tryInt(journeyTime(tableData[-1]["dh"], tableData[-1]["dm"] + (tableData[-1]["dhalf"] * 0.1), tableRowData["dh"], tableRowData["dm"] + (tableRowData["dhalf"] * 0.1)))
			else:
				tableRowData["jtime"] = tryInt(journeyTime(tableData[-1]["dh"], tableData[-1]["dm"] + (tableData[-1]["dhalf"] * 0.1), tableRowData["ah"], tableRowData["am"] + (tableRowData["ahalf"] * 0.1)))
			tableRowData["jtimeShort"] = tryInt(tableRowData["jtime"] - (((int(hash(tableRowData["name"])) % 5) * 0.1) + 0.1)) # szamynstwo do czasu rozszerzenia funkcji rozkladow jazdy
		tableRowData["trainChange"] = i == 0
		vehicles = state["train_enginetype"].split("_")
		for i in range(3):
			if len(vehicles) > i:
				tableRowData["veh" + str(i + 1)] = vehicles[i]
			else:
				tableRowData["veh" + str(i + 1)] = None
		tableRowData["vehweight"] = state["train_engineload"]
		tableRowData["vehvmax"] = 120 # do zmiany przy kopiowaniu skryptu lub przy rozszerzeniu funkcji rozkladow
		tableRowData["vehlength"] = len(vehicles) * 64 # szamynstwo i postepowanie jak wyzej
		tableRowData["vehbrake"] = state["train_brakingmassratio"]
		tableData.append(tableRowData)


def addVec(vector1, vector2):
	return (vector1[0] + vector2[0], vector1[1] + vector2[1])

def timeText(hour, minute):
	return headZeros(hour, 2) + ":" + headZeros(minute, 2)

def journeyTime(hour1, minute1, hour2, minute2):
	return (((((hour2 - hour1) * 60) + (minute2 - minute1)) + 720) % 1440) - 720

def tryInt(value):
	if value == int(value):
		return int(value)
	return value

def removeUnderscores(string):
	return string.replace("_", " ")

def trainNumber(trainName):
	digits = ("0", "1", "2", "3", "4", "5", "6", "7", "8", "9")
	for i in range(len(trainName)):
		if trainName[i:(i + 1)] in digits:
			return trainName[i:]

def kmText(km):
	return str(int(km)) + "." + headZeros(int((km * 1000) % 1000), 3)

def headZeros(value, digits):
	text = str(value)
	while len(text) < digits:
		text = "0" + text
	return text