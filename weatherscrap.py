# The "requests" library is needed to perform an HTTP request to a website.
# The "tkinter" library is needed to create the GUI.
# The "BeautifulSoup" library is needed to parse the HTML page resulting from the HTTP request.
import requests
from tkinter import *
from bs4 import BeautifulSoup


class WeatherScrap:

	# Object constructor, creates the GUI and adds the starting labels, input box and buttons.
	def __init__(self):
		# Main GUI window creation.
		self.window = Tk()
		self.window.title("WeatherScrap")

		# A list where all the replaceable labels must be inserted in order to prevent the overlap issue.
		self.replaceable_labels = []

		# Adding the static labels to GUI. These ones must remain the in place, so they are not added to "replaceable_labels".
		l1 = Label(self.window, text="Città: ", font=("Calibri 18 bold"))
		l1.grid(column=0, row=0)
		l2 = Label(self.window, text="Ora", font=("Calibri 18 bold"))
		l2.grid(column=0, row=1)
		l3 = Label(self.window, text="Meteo", font=("Calibri 18 bold"))
		l3.grid(column=2, row=1)
		l4 = Label(self.window, text="Temp", font=("Calibri 18 bold"))
		l4.grid(column=4, row=1)
		e = Entry(self.window, font=("Calibri", 15))
		e.grid(column=2, row=0)
		b1 = Button(self.window, text ="IlMeteo", font="Calibri 12 bold", command = lambda: self.get_forecast(e.get(), "IlMeteo"))
		b1.grid(column=4, row=0)
		b2 = Button(self.window, text ="3Bmeteo", font="Calibri 12 bold", command = lambda: self.get_forecast(e.get(), "3Bmeteo"))
		b2.grid(column=5, row=0)

		# Starting the GUI event loop.
		self.window.mainloop()


	# Destroys all the replaceable labels previously added to GUI and that were inserted in the "replaceable_labels" list.
	# This prevents the label overlap issue resulting from adding new labels over old ones.
	def clean_gui(self):
		for l in self.replaceable_labels:
			l.destroy()
			

	# Adds a new replaceable label to GUI. If specified, another label with " | " separator character is added after the one created.
	# This is done to simulate table rows\columns in GUI.
	def add_label_to_gui(self, value, separator, cl, rw):
		if separator:
			l = Label(self.window, text=value, font=("Calibri 15"))
			l.grid(column=cl, row=rw)
			self.replaceable_labels.append(l)
			s = Label(self.window, text="|", font=("Calibri 15 bold"))
			s.grid(column=cl+1, row=rw)
			self.replaceable_labels.append(s)
		else:
			l = Label(self.window, text=value, font=("Calibri 15"))
			l.grid(column=cl, row=rw)
			self.replaceable_labels.append(l)


	# Performs webscrapping from forecast websites for a given city.
	# Two forecast website are currently supported: "www.ilmeteo.it" (source="IlMeteo") and "www.3bmeteo.com" (source="3Bmeteo").
	def get_forecast(self, city, source):

		# Cleaning the GUI from old labels to avoid the overlap issue.
		self.clean_gui()

		# If "www.ilmeteo.it" is selected, performs a custom scrap of it's specific HTML\CSS structure.
		if source == "IlMeteo":
			# Composing the URL with the chosen city and performing HTTP request.
			url = "https://www.ilmeteo.it/meteo/"+ city
			html_page = requests.get(url)

			# Using the "BeautifulSoup" library to create a searchable object.
			# Extracting a target part from from that object, it contains the desired forecast data..
			soup_result = BeautifulSoup(html_page.content, "html.parser")
			table = soup_result.find_all("table", class_="datatable", limit=1)

			# Index used to start position labels on GUI after the static ones previously added.
			current_gui_row = 2

			# Looping on the extracted part, looking for time, weather and temperature values and adding them to GUI.
			# Since "www.ilmeteo.it" assigns two different classes ('dark' and 'light') to it's forecast's table rows, an additional loop is needed.
			for row in table:
				row_types = row.find_all("tr", class_=['dark', 'light'])
				for element in row_types:
					time = element.find("span", class_="ora")
					if time:
						self.add_label_to_gui((time.text).strip(), True, 0, current_gui_row)
					weather = element.find("td", class_="col3")
					if weather:
						self.add_label_to_gui((weather.text).strip(), True, 2, current_gui_row)
					temperature = element.find("td", class_="col4")
					if temperature:
						self.add_label_to_gui((temperature.text).strip(), False, 4, current_gui_row)
					current_gui_row += 1

		# If "www.3bmeteo.com" is selected, performs a custom scrap of it's specific HTML\CSS structure.
		elif source == "3Bmeteo":
			# Composing the URL with the chosen city and performing HTTP request.
			url = "https://www.3bmeteo.com/meteo/"+ city
			html_page = requests.get(url)

			# Using the "BeautifulSoup" library to create a searchable object.
			# Extracting a target part from from that object, it contains the desired forecast data.
			soup_result = BeautifulSoup(html_page.content, "html.parser")
			table = soup_result.find_all("div", class_="row-table noPad")
			
			# Index used to start position labels on GUI after the static ones previously added.
			current_gui_row = 2

			# Looping on the extracted part, looking for time, weather and temperature values and adding them to GUI.
			for row in table:
				time = row.find_all("div", class_=['col-xs-1-4 big zoom_prv', 'col-xs-1-4 big'], limit=1)
				if time:
					self.add_label_to_gui((time[0].text).strip(), True, 0, current_gui_row)
				weather = row.find_all("div", class_="col-xs-2-4", limit=1)
				if weather:
					self.add_label_to_gui((weather[0].text).strip(), True, 2, current_gui_row)
				temperature = row.find_all("span", class_="switchcelsius switch-te active", limit=1)
				if temperature:
					self.add_label_to_gui((temperature[0].text).strip(), False, 4, current_gui_row)
				current_gui_row += 1


# Creating the object, then the constructor will start the main loop.
WeatherScrap()