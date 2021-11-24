import requests
from tkinter import *
from bs4 import BeautifulSoup

class WeatherScrap:

	def __init__(self):
		self.window = Tk()
		self.window.title("WeatherScrap")
		self.all_labels = []

		lbl = Label(self.window, text="Città: ", font=("Calibri bold", 15))
		lbl.grid(column=0, row=0)
		e = Entry(self.window, font=("Calibri regular", 15))
		e.grid(column=2, row=0)
		b1 = Button(self.window, text ="IlMeteo", command = lambda: self.get_ilmeteo(e.get()))
		b1.grid(column=4, row=0)
		b2 = Button(self.window, text ="3Bmeteo", command = lambda: self.get_3bmeteo(e.get()))
		b2.grid(column=5, row=0)

		lbl = Label(self.window, text="Ora", font=("Calibri bold", 15))
		lbl.grid(column=0, row=1)
		lbl = Label(self.window, text="|", font=("Calibri bold", 15))
		lbl.grid(column=1, row=1)
		lbl = Label(self.window, text="Meteo", font=("Calibri bold", 15))
		lbl.grid(column=2, row=1)
		lbl = Label(self.window, text="|", font=("Calibri bold", 15))
		lbl.grid(column=3, row=1)
		lbl = Label(self.window, text="Temp", font=("Calibri bold", 15))
		lbl.grid(column=4, row=1)

		self.window.mainloop()

	def clean_gui(self):
		for w in self.all_labels:
			w.destroy()

	def get_ilmeteo(self, city):
		self.clean_gui()

		url = "https://www.ilmeteo.it/meteo/"+ city
		page = requests.get(url)
		
		soup = BeautifulSoup(page.content, "html.parser")
		table = soup.find_all("table", class_="datatable", limit=1)

		rws = 2
		for rows in table:
			row = rows.find_all("tr", class_=['dark', 'light'])
			if row:
				for param in row:
					time = param.find("span", class_="ora")
					if time:
						lbltime = Label(self.window, text=(time.text).strip(), font=("Calibri", 15))
						lbltime.grid(column=0, row=rws)
						self.all_labels.append(lbltime)
						lbl = Label(self.window, text="|", font=("Calibri bold", 15))
						lbl.grid(column=1, row=rws)
						self.all_labels.append(lbl)

					weather = param.find("td", class_="col3")
					if weather:
						lblweather = Label(self.window, text=(weather.text).strip(), font=("Calibri", 15))
						lblweather.grid(column=2, row=rws)
						self.all_labels.append(lblweather)
						lbl = Label(self.window, text="|", font=("Calibri bold", 15))
						lbl.grid(column=3, row=rws)
						self.all_labels.append(lbl)

					temperature = param.find("td", class_="col4")
					if temperature:
						lbltemperature = Label(self.window, text=(temperature.text).strip(), font=("Calibri", 15))
						lbltemperature.grid(column=4, row=rws)
						self.all_labels.append(lbltemperature)
					rws += 1

	def get_3bmeteo(self, city):

		self.clean_gui()

		url = "https://www.3bmeteo.com/meteo/"+ city
		page = requests.get(url)

		soup = BeautifulSoup(page.content, "html.parser")
		table = soup.find_all("div", class_="row-table noPad")
		
		rws = 2
		for row in table:
			time = row.find_all("div", class_=['col-xs-1-4 big zoom_prv', 'col-xs-1-4 big'], limit=1)
			if time:
				lbltime = Label(self.window, text=(time[0].text).strip(), font=("Calibri", 15))
				lbltime.grid(column=0, row=rws)
				self.all_labels.append(lbltime)
				lbl = Label(self.window, text="|", font=("Calibri bold", 15))
				lbl.grid(column=1, row=rws)
				self.all_labels.append(lbl)
		
			weather = row.find_all("div", class_="col-xs-2-4", limit=1)
			if weather:
				lblweather = Label(self.window, text=(weather[0].text).strip(), font=("Calibri", 15))
				lblweather.grid(column=2, row=rws)
				self.all_labels.append(lblweather)
				lbl = Label(self.window, text="|", font=("Calibri bold", 15))
				lbl.grid(column=3, row=rws)
				self.all_labels.append(lbl)

			temperature = row.find_all("span", class_="switchcelsius switch-te active", limit=1)
			if temperature:
				lbltemperature = Label(self.window, text=(temperature[0].text).strip(), font=("Calibri", 15))
				lbltemperature.grid(column=4, row=rws)
				self.all_labels.append(lbltemperature)
			rws += 1

WeatherScrap()