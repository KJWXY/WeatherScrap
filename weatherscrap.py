#Requests is needed to perform HTTPS connections
#Tkinter is needed to create the GUI
#BeautifulSoup is needed to perform HTML\CSS code parsing
import requests
from tkinter import *
from bs4 import BeautifulSoup

#List containing the labels that need to be updated with new text.
#They will be destroyed everytime the funtions start in order to avoid the text overlapping issue
AllLabels = []

#Accepts a city name as input and performs webscrapping of forecasts from 3bmeteo.com 
def ThreeBMeteo(city):

	#Destroy, if existing, all previous labels added on GUI and inserted in the list AllLabels
	for w in AllLabels:
		w.destroy()

	#Performing the HTTPS request for the selected city to 3bmeteo.com
	url = "https://www.3bmeteo.com/meteo/"+ city
	page = requests.get(url)

	#Parsing HTML result page to extract the table containing forecasts
	soup = BeautifulSoup(page.content, "html.parser")
	table = soup.find_all("div", class_="row-table noPad")
	
	#Looping on the extracted table to find forecast details for each hour (time, weather, temperature)
	#rws represents the starting row index following the first row containing columns names
	rws = 2
	for row in table:
		#Searching the actual table row for the class containing the time value
		#3bmeteo.com uses both of the following div class for the time value so a double search is needed
		time = row.find_all("div", class_=['col-xs-1-4 big zoom_prv', 'col-xs-1-4 big'], limit=1)
		if time:
			#The time value is added to a label showed on GUI
			#The label is also inserted in the AllLabels list
			#Also a | character is added to simulate columns on GUI
			lbltime = Label(window, text=(time[0].text).strip(), font=("Calibri", 15))
			lbltime.grid(column=0, row=rws)
			AllLabels.append(lbltime)
			lbl = Label(window, text="|", font=("Calibri bold", 15))
			lbl.grid(column=1, row=rws)
			AllLabels.append(lbl)

		#Searching the actual table row for the class containing the weather value	
		weather = row.find_all("div", class_="col-xs-2-4", limit=1)
		if weather:
			#The weather value is added to a label showed on GUI
			#The label is also inserted in the AllLabels list
			#Also a | character is added to simulate columns on GUI
			lblweather = Label(window, text=(weather[0].text).strip(), font=("Calibri", 15))
			lblweather.grid(column=2, row=rws)
			AllLabels.append(lblweather)
			lbl = Label(window, text="|", font=("Calibri bold", 15))
			lbl.grid(column=3, row=rws)
			AllLabels.append(lbl)

		#The temperature value is added to a label showed on GUI
		#The label is also inserted in the AllLabels list
		#Also a | character is added to simulate columns on GUI
		temperature = row.find_all("span", class_="switchcelsius switch-te active", limit=1)
		if temperature:
			lbltemperature = Label(window, text=(temperature[0].text).strip(), font=("Calibri", 15))
			lbltemperature.grid(column=4, row=rws)
			AllLabels.append(lbltemperature)
		rws += 1

#Accepts a city name as input and performs webscrapping of forecasts from ilmeteo.it
def IlMeteo(city):

	#Destroy, if existing, all previous labels added on GUI and inserted in the list AllLabels
	for w in AllLabels:
		w.destroy()

	#Performing the HTTPS request for the selected city to ilmeteo.it
	url = "https://www.ilmeteo.it/meteo/"+ city
	page = requests.get(url)
	
	#Parsing HTTPS's result page to extract the table containing forecasts
	soup = BeautifulSoup(page.content, "html.parser")
	table = soup.find_all("table", class_="datatable", limit=1)

	#Looping on the extracted table to find forecast details for each hour (time, weather, temperature)
	#rws represents the starting row index following the firt row containing columns names
	rws = 2
	for rows in table:
		#ilmeteo.it stores forecasts in a table using two classes, 'dark' and 'light'
		row = rows.find_all("tr", class_=['dark', 'light'])
		if row:
			#looping on each table row in order to find desired forecast data
			for param in row:
				#Finding the exact class containing the time data
				time = param.find("span", class_="ora")
				if time:
					#The time value is added to a label showed on GUI
					#The label is also inserted in the AllLabels list
					#Also a | character is added to simulate columns on GUI
					lbltime = Label(window, text=(time.text).strip(), font=("Calibri", 15))
					lbltime.grid(column=0, row=rws)
					AllLabels.append(lbltime)
					lbl = Label(window, text="|", font=("Calibri bold", 15))
					lbl.grid(column=1, row=rws)
					AllLabels.append(lbl)

				#Finding the exact class containing the weather data
				weather = param.find("td", class_="col3")
				if weather:
					#The weather value is added to a label showed on GUI
					#The label is also inserted in the AllLabels list
					#Also a | character is added to simulate columns on GUI
					lblweather = Label(window, text=(weather.text).strip(), font=("Calibri", 15))
					lblweather.grid(column=2, row=rws)
					AllLabels.append(lblweather)
					lbl = Label(window, text="|", font=("Calibri bold", 15))
					lbl.grid(column=3, row=rws)
					AllLabels.append(lbl)

				#Finding the exact class containing the temperature data
				temperature = param.find("td", class_="col4")
				if temperature:
					#The temperature value is added to a label showed on GUI
					#The label is also inserted in the AllLabels list
					#Also a | character is added to simulate columns on GUI
					lbltemperature = Label(window, text=(temperature.text).strip(), font=("Calibri", 15))
					lbltemperature.grid(column=4, row=rws)
					AllLabels.append(lbltemperature)
				rws += 1

def LaMMA(city):
	for w in AllLabels:
		w.destroy()

	url = "http://www.lamma.rete.toscana.it/meteo/meteo-"+ city
	page = requests.get(url)
	
	soup = BeautifulSoup(page.content, "html.parser")
	table = soup.find_all("div", class_="tab-pane active", limit=1)

	rws = 2
	for rows in table:
		row = rows.find_all("div", class_="hourlyrowsea hidden-xs")
		for param in row:
			time = param.find("b")
			lbltime = Label(window, text=(time.text).strip(), font=("Calibri", 15))
			lbltime.grid(column=0, row=rws)
			AllLabels.append(lbltime)
			lbl = Label(window, text="|", font=("Calibri bold", 15))
			lbl.grid(column=1, row=rws)
			AllLabels.append(lbl)

			weather = param.find("div", class_="forecast")
			lblweather = Label(window, text=(weather.text).strip(), font=("Calibri", 15))
			print((weather.text).strip())
			lblweather.grid(column=2, row=rws)
			AllLabels.append(lblweather)
			lbl = Label(window, text="|", font=("Calibri bold", 15))
			lbl.grid(column=3, row=rws)
			AllLabels.append(lbl)
			
			temperature = param.find("div", class_="tperc")
			lbltemperature = Label(window, text=(temperature.text).strip(), font=("Calibri", 15))
			lbltemperature.grid(column=4, row=rws)
			AllLabels.append(lbltemperature)
			rws += 1

#GUI initialization
window = Tk()
window.title("WeatherScrap")

#Adding label,inputbox and button
lbl = Label(window, text="Città: ", font=("Calibri bold", 15))
lbl.grid(column=0, row=0)
e = Entry(window, font=("Calibri regular", 15))
e.grid(column=2, row=0)
b1 = Button(window, text ="3Bmeteo", command = lambda: ThreeBMeteo(e.get()))
b1.grid(column=4, row=0)
b2 = Button(window, text ="IlMeteo", command = lambda: IlMeteo(e.get()))
b2.grid(column=5, row=0)
b3 = Button(window, text ="LaMMA", command = lambda: LaMMA(e.get()))
b3.grid(column=6, row=0)

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

#Starting the GUI loop
window.mainloop()