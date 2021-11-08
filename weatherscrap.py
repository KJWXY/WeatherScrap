#Requests is needed to perform HTTPS connections
#Tkinter is needed to create the GUI
#BeautifulSoup is needed to perform HTML\CSS code parsing
import requests
from tkinter import *
from bs4 import BeautifulSoup

#Accepts a city name as input and performs webscrapping of forecasts from 3bmeteo.com 
def ThreeBMeteo(city):
	#Performing the HTTPS request for the selected city to 3bmeteo.com
	url = "https://www.3bmeteo.com/meteo/"+ city
	page = requests.get(url)

	#Parsing HTTPS's result page to extract the table containing forecasts
	soup = BeautifulSoup(page.content, "html.parser")
	table = soup.find_all("div", class_="row-table noPad")

	#Creating columns names on GUI
	lbl = Label(window, text="Ora", font=("Calibri bold", 15))
	lbl.grid(column=0, row=1)
	lbl = Label(window, text="|", font=("Calibri bold", 15))
	lbl.grid(column=1, row=1)
	lbl = Label(window, text="Meteo", font=("Calibri bold", 15))
	lbl.grid(column=2, row=1)
	lbl = Label(window, text="|", font=("Calibri bold", 15))
	lbl.grid(column=3, row=1)
	lbl = Label(window, text="Temp", font=("Calibri bold", 15))
	lbl.grid(column=4, row=1)
	
	#Looping on the extracted table to find forecast details for each hour (time, weather, temperature)
	rws = 2
	for row in table:
		#Searching the actual table row for the class containing the time value
		#3bmeteo.com uses both of the following div class for the time value so a doulbe search is needed
		time1 = row.find_all("div", class_="col-xs-1-4 big zoom_prv", limit=1)
		time2 = row.find_all("div", class_="col-xs-1-4 big", limit=1)
		#Since only find_all() returns an object with a .text function, was necessary to use it instead of find()
		#Fin_all() returns an object that needs to be looped in order to correctly print the contained text
		for ptime in time1:
			#The time value is added to a label showed on GUI
			#Also a | character is added to simulate columns on GUI
			lbltime = Label(window, text=(ptime.text).strip(), font=("Calibri", 15))
			lbltime.grid(column=0, row=rws)
			lbl = Label(window, text="|", font=("Calibri bold", 15))
			lbl.grid(column=1, row=rws)
		for ptime in time2:
			#The time value is added to a label showed on GUI
			#Also a | character is added to simulate columns on GUI
			lbltime = Label(window, text=(ptime.text).strip(), font=("Calibri", 15))
			lbltime.grid(column=0, row=rws)
			lbl = Label(window, text="|", font=("Calibri bold", 15))
			lbl.grid(column=1, row=rws)

		#Searching the actual table row for the class containing the weather value	
		weather = row.find_all("div", class_="col-xs-2-4", limit=1)
		for pweather in weather:
			#The weather value is added to a label showed on GUI
			#Also a | character is added to simulate columns on GUI
			lblweather = Label(window, text="		")
			lblweather.grid(column=2, row=rws)
			lblweather = Label(window, text=(pweather.text).strip(), font=("Calibri", 15))
			lblweather.grid(column=2, row=rws)
			lbl = Label(window, text="|", font=("Calibri bold", 15))
			lbl.grid(column=3, row=rws)

		#The temperature value is added to a label showed on GUI
		#Also a | character is added to simulate columns on GUI
		temperature = row.find_all("span", class_="switchcelsius switch-te active", limit=1)
		for ptemperature in temperature:
			lbltemperature = Label(window, text=(ptemperature.text).strip(), font=("Calibri", 15))
			lbltemperature.grid(column=4, row=rws)
		rws += 1

#GUI initialization
window = Tk()
window.title("WeatherScrap")

#Adding label,inputbox and button
lbl = Label(window, text="Città: ", font=("Calibri bold", 15))
lbl.grid(column=0, row=0)
e = Entry(window, font=("Calibri regular", 15))
e.grid(column=2, row=0)
b = Button(window, text ="OK", command = lambda: ThreeBMeteo(e.get()))
b.grid(column=4, row=0)

#Starting the GUI loop
window.mainloop()