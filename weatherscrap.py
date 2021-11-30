import requests
from tkinter import *
from bs4 import BeautifulSoup


class WeatherScrap:

	def __init__(self):
		self.window = Tk()
		self.window.title("WeatherScrap")
		self.all_labels = []

		self.add_label_to_gui("Città: ", 0, 0)
		e = Entry(self.window, font=("Calibri regular", 15))
		e.grid(column=2, row=0)
		b1 = Button(self.window, text ="IlMeteo", command = lambda: self.get_forecast(e.get(), "IlMeteo"))
		b1.grid(column=4, row=0)
		b2 = Button(self.window, text ="3Bmeteo", command = lambda: self.get_forecast(e.get(), "3Bmeteo"))
		b2.grid(column=5, row=0)

		self.add_label_to_gui("Ora", 0, 1)
		self.add_label_to_gui("Meteo", 2, 1)
		self.add_label_to_gui("Temp", 4, 1)

		self.window.mainloop()


	def clean_gui(self):
		for w in self.all_labels:
			w.destroy()
			

	def add_label_to_gui(self, value, col, rws):
		label = Label(self.window, text=value, font=("Calibri", 15))
		label.grid(column=col, row=rws)
		self.all_labels.append(label)
		lbl = Label(self.window, text="|", font=("Calibri bold", 15))
		lbl.grid(column=col+1, row=rws)
		self.all_labels.append(lbl)


	def get_forecast(self, city, source):
		self.clean_gui()

		if source == "IlMeteo":
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
							self.add_label_to_gui((time.text).strip(), 0, rws)
						weather = param.find("td", class_="col3")
						if weather:
							self.add_label_to_gui((weather.text).strip(), 2, rws)
						temperature = param.find("td", class_="col4")
						if temperature:
							self.add_label_to_gui((temperature.text).strip(), 4, rws)
						rws += 1

		elif source == "3Bmeteo":
			url = "https://www.3bmeteo.com/meteo/"+ city
			page = requests.get(url)
			soup = BeautifulSoup(page.content, "html.parser")
			table = soup.find_all("div", class_="row-table noPad")
			
			rws = 2
			for row in table:
				time = row.find_all("div", class_=['col-xs-1-4 big zoom_prv', 'col-xs-1-4 big'], limit=1)
				if time:
					self.add_label_to_gui((time[0].text).strip(), 0, rws)
				weather = row.find_all("div", class_="col-xs-2-4", limit=1)
				if weather:
					self.add_label_to_gui((weather[0].text).strip(), 2, rws)
				temperature = row.find_all("span", class_="switchcelsius switch-te active", limit=1)
				if temperature:
					self.add_label_to_gui((temperature[0].text).strip(), 4, rws)
				rws += 1


WeatherScrap()