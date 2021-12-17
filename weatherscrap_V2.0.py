import requests
from tkinter import *
from io import BytesIO
from datetime import datetime
from bs4 import BeautifulSoup
from PIL import ImageTk, Image

class WeatherScrapper:
	def __init__(self):
		self.window = Tk()
		self.window.title("WeatherScrapper")
		self.set_gui_icon('https://www.vhv.rs/dpng/d/459-4597100_windy-weather-clipart-at-getdrawings-windy-weather-icon.png')
		
		self.replaceable_labels = []
		self.forecast = { hours : [[],[]] for hours in range(1,25,1) }

		self.add_label_to_gui("Città: ", "Calibri 18 bold", True, False, 0, 0)
		self.e = Entry(self.window, font=("Calibri 15"))
		self.e.grid(column=2, row=0)
		self.add_button_to_gui("Average", 4, 0)
		self.add_label_to_gui("Ora", "Calibri 18 bold", True, False, 0, 1)
		self.add_label_to_gui("Meteo", "Calibri 18 bold", True, False, 2, 1)
		self.add_label_to_gui("Temp", "Calibri 18 bold", True, False, 4, 1)

		self.window.mainloop()


	def set_gui_icon(self, url):
		response = requests.get(url)
		icon_raw = response.content
		icon = ImageTk.PhotoImage(Image.open(BytesIO(icon_raw)))
		self.window.iconphoto(False, icon)


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
		b = Button(self.window, text=value, font="Calibri 12 bold", command=lambda:self.get_forecast(self.e.get()))
		b.grid(column=cl, row=rw)


	def get_forecast(self, city):
		self.clean_gui()
		self.clean_forecast()
		self.get_raw_data("https://www.ilmeteo.it/meteo/", city, "IlMeteo")
		self.get_raw_data("https://www.3bmeteo.com/meteo/", city, "3Bmeteo")
		self.get_raw_data("http://www.lamma.rete.toscana.it/meteo/meteo-", city, "LaMMA")
		self.get_raw_data("https://www.meteogiuliacci.it/meteo/", city, "MeteoGiu")
		self.print_average()


	def clean_gui(self):
		for l in self.replaceable_labels:
			l.destroy()


	def clean_forecast(self):
		self.forecast = { hours : [[],[]] for hours in range(1,25,1) }


	def get_raw_data(self, url, city, source):
		html_page = requests.get(url+city)
		soup_result = BeautifulSoup(html_page.content, "html.parser")

		if source == "IlMeteo":
			table = soup_result.find_all("table", class_="datatable", limit=1)
			for rows in table:
				row = rows.find_all("tr", class_=['dark', 'light'])
				for element in row:
					time = element.find("span", class_="ora")
					weather = element.find("td", class_="col3")
					temperature = element.find("td", class_="col4")
					if time:
						self.forecast[int((time.text).strip())][0] = [str.lower(((weather.text).strip()).replace("\xa0"," "))]
						self.forecast[int((time.text).strip())][1] = [float((temperature.text).strip().replace("°",""))]

		elif source == "3Bmeteo":
			table = soup_result.find_all("div", class_="row-table noPad")
			for row in table:
				time = row.find_all("div", class_=['col-xs-1-4 big zoom_prv', 'col-xs-1-4 big'], limit=1)
				weather = row.find_all("div", class_="col-xs-2-4", limit=1)
				temperature = row.find_all("span", class_="switchcelsius switch-te active", limit=1)
				if time:
					if(((((time[0].text).strip()).replace(":00",""))[0:1]) == "0"):
						self.forecast[int((((time[0].text).strip()).replace(":00",""))[1:])][0].append(str.lower((weather[0].text).strip()))
						self.forecast[int((((time[0].text).strip()).replace(":00",""))[1:])][1].append(float((temperature[0].text).strip().replace("°","")))
					else:
						self.forecast[int((((time[0].text).strip()).replace(":00","")))][0].append(str.lower((weather[0].text).strip()))
						self.forecast[int((((time[0].text).strip()).replace(":00","")))][1].append(float((temperature[0].text).strip().replace("°","")))

		elif source == "LaMMA":
			table = soup_result.find_all("div", class_="tab-pane active")
			rows = table[0].find_all("div", class_=['hourlyrowsea hidden-xs', 'hourlyrow hidden-xs'])
			for row in rows:
				time_class = row.find_all("div", class_="forecast", limit=1)
				weather_class = row.find_all("div", class_="forecast", limit=1)
				temperature_class = row.find_all("div", class_="treal", limit=1)
				for element in time_class:
					time = element.find_all("b", limit=1)
				for element in weather_class:
					weather_position = 0
					for sub_element in element:
						if(weather_position == 4):
							weather= (sub_element.text).strip()
						weather_position += 1
				for element in temperature_class:
					temperature = (element.text).strip()
				self.forecast[int(((time[0].text).strip()).replace(":00",""))][0].append(str.lower(weather))
				self.forecast[int(((time[0].text).strip()).replace(":00",""))][1].append(float(temperature.replace("°","")))

		elif source == "MeteoGiu":
			table = soup_result.find_all("tr", class_=['rigagrigia', 'rigabianca'])
			for row in table:
				time_class = row.find_all("td", class_="tab-comuni1")
				weather_class = row.find_all("script", limit=1)
				temperature_class = row.find_all("td", class_="tab-comuni3")
				for element in time_class:
					time = (element.text).strip()
				for element in weather_class:
					weather = (((element.text).replace('document.write("', '')).replace('");', '')).strip()
				for element in temperature_class:
					temperature = (element.text).strip()
				self.forecast[int((time).replace(".00",""))][0].append(str.lower(weather))
				self.forecast[int((time).replace(".00",""))][1].append(float(temperature.replace("°","")))


	def print_average(self):
		current_gui_row = 2
		for hour in self.forecast.keys():
			if(int(hour) > self.get_hour()):
				self.add_label_to_gui(hour, "Calibri 15", False, True, 0, current_gui_row)
				self.add_label_to_gui("/".join(self.remove_duplicates(self.forecast[hour][0])), "Calibri 15", False, True, 2, current_gui_row)
				self.add_label_to_gui(self.get_average(self.forecast[hour][1]), "Calibri 15", False, False, 4, current_gui_row)
			current_gui_row += 1

	
	def get_hour(self):
		time = datetime.now()
		return(int(time.strftime("%H")))


	def remove_duplicates(self, values):
		if not values:
			return []
		else:
			return(list(dict.fromkeys(self.replace_value(values, "parz. nuvoloso", "poco nuvoloso"))))


	def replace_value(self, values, current, new):
		for value in values:
			if value == current:
				values[values.index(value)] = new
		return values


	def get_average(self, values):
		if not values:
			return 0
		else:
			return (round((sum(values)/len(values)), 1))
	

	def print_forecast(self):
		for hour in self.forecast.keys():
			print(hour + " ", self.forecast[hour])

	
WeatherScrapper()