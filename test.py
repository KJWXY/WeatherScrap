import requests
from tkinter import *
from bs4 import BeautifulSoup


class WeatherScrap:
	def __init__(self):
		self.window = Tk()
		self.window.title("WeatherScrap")

		self.replaceable_labels = []

		self.add_label_to_gui("Città: ", "Calibri 18 bold", True, False, 0, 0)
		self.e = Entry(self.window, font=("Calibri 15"))
		self.e.grid(column=2, row=0)
		self.add_button_to_gui("IlMeteo", 4, 0)
		self.add_button_to_gui("3Bmeteo", 5, 0)
		self.add_button_to_gui("LaMMA", 6, 0)
		self.add_button_to_gui("MeteoGiu", 7, 0)
		self.add_label_to_gui("Ora", "Calibri 18 bold", True, False, 0, 1)
		self.add_label_to_gui("Meteo", "Calibri 18 bold", True, False, 2, 1)
		self.add_label_to_gui("Temp", "Calibri 18 bold", True, False, 4, 1)

		self.window.mainloop()


	def clean_gui(self):
		for l in self.replaceable_labels:
			l.destroy()
			

	def add_label_to_gui(self, value, tfont, static, separator, cl, rw):
		l = Label(self.window, text=value, font=(tfont))
		l.grid(column=cl, row=rw)
		if not static:
			self.replaceable_labels.append(l)
		if separator:
			s = Label(self.window, text="|", font=("Calibri 15 bold"))
			s.grid(column=cl+1, row=rw)
			self.replaceable_labels.append(s)


	def add_button_to_gui(self, value, cl, rw):
		b = Button(self.window, text=value, font="Calibri 12 bold", command=lambda:self.get_forecast(self.e.get(), value))
		b.grid(column=cl, row=rw)


	def get_forecast(self, city, source):
		self.clean_gui()

		if source == "IlMeteo":
			url = "https://www.ilmeteo.it/meteo/"+ city
			html_page = requests.get(url)

			soup_result = BeautifulSoup(html_page.content, "html.parser")
			table = soup_result.find_all("table", class_="datatable", limit=1)

			current_gui_row = 2

			for row in table:
				row_types = row.find_all("tr", class_=['dark', 'light'])
				for element in row_types:
					time = element.find("span", class_="ora")
					if time:
						self.add_label_to_gui((time.text).strip(), "Calibri 15", False, True, 0, current_gui_row)
					weather = element.find("td", class_="col3")
					if weather:
						self.add_label_to_gui((weather.text).strip(), "Calibri 15", False, True, 2, current_gui_row)
					temperature = element.find("td", class_="col4")
					if temperature:
						self.add_label_to_gui((temperature.text).strip(), "Calibri 15", False, False, 4, current_gui_row)
					current_gui_row += 1

		elif source == "3Bmeteo":
			url = "https://www.3bmeteo.com/meteo/"+ city
			html_page = requests.get(url)

			soup_result = BeautifulSoup(html_page.content, "html.parser")
			table = soup_result.find_all("div", class_="row-table noPad")
			
			current_gui_row = 2

			for row in table:
				time = row.find_all("div", class_=['col-xs-1-4 big zoom_prv', 'col-xs-1-4 big'], limit=1)
				if time:
					self.add_label_to_gui((time[0].text).strip(), "Calibri 15", False, True, 0, current_gui_row)
				weather = row.find_all("div", class_="col-xs-2-4", limit=1)
				if weather:
					self.add_label_to_gui((weather[0].text).strip(), "Calibri 15", False, True, 2, current_gui_row)
				temperature = row.find_all("span", class_="switchcelsius switch-te active", limit=1)
				if temperature:
					self.add_label_to_gui((temperature[0].text).strip(), "Calibri 15", False, False, 4, current_gui_row)
				current_gui_row += 1

		elif source == "LaMMA":
			url = "http://www.lamma.rete.toscana.it/meteo/meteo-"+ city
			html_page = requests.get(url)

			soup_result =  BeautifulSoup(html_page.content, "html.parser")
			table = soup_result.find_all("div", class_="tab-pane active")
			rows = table[0].find_all("div", class_=['hourlyrowsea hidden-xs', 'hourlyrow hidden-xs'])

			current_gui_row = 2

			for row in rows:
				time_class = row.find_all("div", class_="forecast", limit=1)
				for element in time_class:
					time = element.find_all("b", limit=1)
					self.add_label_to_gui((time[0].text).strip(), "Calibri 15", False, True, 0, current_gui_row)
				weather_class = row.find_all("div", class_="forecast", limit=1)
				for element in weather_class:
					weather_position = 0
					for weather in element:
						if(weather_position == 4):
							self.add_label_to_gui((weather.text).strip(), "Calibri 15", False, True, 2, current_gui_row)
						weather_position += 1
				temperature_class = row.find_all("div", class_="treal", limit=1)
				for temperature in temperature_class:
					self.add_label_to_gui((temperature.text).strip(), "Calibri 15", False, False, 4, current_gui_row)
				current_gui_row += 1

		elif source == "MeteoGiu":
			url = "https://www.meteogiuliacci.it/meteo/" + city
			html_page = requests.get(url)

			soup_result = BeautifulSoup(html_page.content, "html.parser")
			table = soup_result.find_all("tr", class_=['rigagrigia', 'rigabianca'])

			current_gui_row = 2

			for row in table:
				time_class = row.find_all("td", class_="tab-comuni1")
				for time in time_class:
					self.add_label_to_gui((time.text).strip(), "Calibri 15", False, True, 0, current_gui_row)
				weather_class = row.find_all("script", limit=1)
				for element in weather_class:
					element_clean = (element.text).replace('document.write("', '')
					weather = element_clean.replace('");', '')
					self.add_label_to_gui(weather.strip(), "Calibri 15", False, True, 2, current_gui_row)
				temperature_class = row.find_all("td", class_="tab-comuni3")
				for temperature in temperature_class:
					self.add_label_to_gui((temperature.text).strip(), "Calibri 15", False, False, 4, current_gui_row)
				current_gui_row += 1

		elif source == "Meteoam":
			url = "http://www.meteoam.it/ta/previsione/"+ city
			html_page = requests.get(url)

			soup_result =  BeautifulSoup(html_page.content, "html.parser")
			table = soup_result.find_all("tbody")
			rows = table[0].find_all("tr")

			current_gui_row = 2

			for row in rows:
				time_class = row.find_all("th")
				for time in time_class:
					self.add_label_to_gui((time.text).strip(), "Calibri 15", False, True, 0, current_gui_row)
				weather_class = row.find_all("img")
				for weather in weather_class:
					self.add_label_to_gui((weather.get('title')).strip(), "Calibri 15", False, True, 2, current_gui_row)
				temperature_class = row.find_all("td", limit=3)
				temperature_position = 0
				for temperature in temperature_class:
					if(temperature_position == 2):
						self.add_label_to_gui((temperature.text).strip(), "Calibri 15", False, False, 4, current_gui_row)
					temperature_position += 1
				current_gui_row += 1

WeatherScrap()